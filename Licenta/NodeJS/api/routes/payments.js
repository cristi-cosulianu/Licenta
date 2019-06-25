const express = require('express');
const router = express.Router();

const multer = require('multer');

const Bill = require("../models/bill");
const Person = require("../models/person");
const Payment = require("../models/payment");

router.get('/', (req, res, next) => {
    Payment.find()
    .populate('initiator', 'name') // populate with info of the initiator
    .exec()
    .then(docs => {
        const response = {
            count: docs.length,
            payments: docs.map(doc => {
                return {
                    _id: doc._id,
                    billId: doc.billId,
                    payerId: doc.payerId,
                    productName: doc.productName,
                    productPrice: doc.productPrice
                }
            })
        }
        res.status(200).json(response);
    })
    .catch(err => {
        res.status(500).json({
            error: err
        });
    });
});

router.get('/:paymentId', (req, res, next) => {
    const id = req.params.paymentId;
    Payment.findById(id).exec()
    .then(doc => {
        console.log("From database:", doc);
        if (doc) {
            res.status(200).json(doc);
        } else {
            res.status(404).json({
                message: "No valid entry for provided ID:" + id
            });
        }
    })
    .catch(err => {
        console.log(err);
        res.status(500).json({
            error: err
        });
    });
});


router.post('/', (req, res, next) => {
    const initiatorId = req.body.initiatorId;

    // Check if the initiator exist.
    Person.findById(initiatorId)
        .then(person => {
        const bill = new Bill({
            initiator: person._id,
            title: req.body.title,
            date: req.body.date
        });

        console.log(req.body.paymentsList);
        // for (payment in paymentsList) {
        //     const 
        // }

        return bill.save()
        .then(result => {
            console.log(result);
            res.status(201).json({
                billId: result._id,
                billTitle: result.title,
                initiatorName: initiatorId,
                paymentToPersonsList: [],
                paymentsList: [],
                personsList: []
            });
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({
                error: err
            });
        });
    })
    .catch(err => {
        res.status(500).json({
            message: "No initiator with id: " + initiatorId,
            error: err
        });
    })
});

router.put('/:paymentId', (req, res, next) => {
    const id = req.params.paymentId;

    // Create object with fields to update.
    const updateOps = {};
    for (const ops of req.body) {
        updateOps[ops.propName] = ops.value;
    }

    // Update object.
    Payment.update({ _id: id}, { $set: updateOps })
    .exec()
    .then(result => {
        res.status(200).json({
            message: 'Payment updated!',
            request: {
                type: "GET",
                url: 'http://localhost:8080/payments/' + id
            }
        });
    })
    .catch(err =>  {
        console.log(err);
        res.status(500).json({
            error: err
        });
    });
});

router.delete('/all', (req, res, next) => {
    Payment.deleteMany({}).exec()
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        console.log(err);
        res.status(500).json({
            error: err
        })
    });
});

router.delete('/:paymentId', (req, res, next) => {
    const id = req.params.paymentId;
    Payment.deleteOne({ _id: id}).exec()
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        console.log(err);
        res.status(500).json({
            error: err
        })
    });
});

module.exports = router;