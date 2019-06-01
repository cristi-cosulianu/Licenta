const express = require('express');
const router = express.Router();

const multer = require('multer');
const storage = multer.diskStorage({
    destination: function(req, file, cb){
        cb(null, 'uploads/');
    },
    filename: function(req, file, cb){
        const currDate = new Date().toDateString();
        const filename = currDate + "_" + file.originalname;
        cb(null, filename);
    }
});
const upload = multer({ storage: storage });


const Bill = require("../models/bill");
const Person = require("../models/person");


router.get('/', (req, res, next) => {
    Bill.find()
    .populate('initiator', 'name') // populate with info of the initiator
    .exec()
    .then(docs => {
        const response = {
            count: docs.length,
            bills: docs.map(doc => {
                return {
                    _id: doc._id,
                    initiator: doc.initiator,
                    title: doc.title,
                    date: doc.date
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

router.get('/:billId', (req, res, next) => {
    const id = req.params.billId;
    Bill.findById(id).exec()
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
    const initiatorId = req.body.initiator;
    // Check if the initiator exist.
    Person.findById(initiatorId)
    .then(person => {
        const bill = new Bill({
            initiator: initiatorId,
            title: req.body.title,
            date: req.body.date
        });
    
        return bill.save()
        .then(result => {
            console.log(result);
            res.status(201).json({
                _id: result._id,
                initiator: result.initiator
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


router.delete('/:billId', (req, res, next) => {
    const id = req.params.billId;
    Bill.remove({ _id: id}).exec()
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