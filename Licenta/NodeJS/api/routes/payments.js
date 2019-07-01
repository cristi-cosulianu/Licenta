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

router.get('/person/:personId', (req, res, next) => {
    const personId = req.params.personId;
    Person.findById(personId).exec()
    .then(person => {
        console.log(person);
        Payment.find({ payerId: personId }).exec()
        .then(payments => {
            console.log(payments);
            let billsIdsSet = new Set([]);
            for (let i = 0; i < payments.length; i++) {
                billsIdsSet.add("" + payments[i].billId);
            }
            const billsIdsList = Array.from(billsIdsSet);
            console.log(billsIdsList);
            let personsIdsSet = new Set([]);
            for (let i = 0; i < payments.length; i++) {
                personsIdsSet.add("" + payments[i].payerId);
            }
            const personsIdsList = Array.from(personsIdsSet);
            Person.find( {_id: { $in: personsIdsList} } ).exec()
            .then(persons => {
                console.log(billsIdsList);
                Bill.find({_id: { $in: billsIdsList} })
                .populate("initiator", "name")
                .exec()
                .then(bills => {
                    console.log(bills);
                    const responseBillsList = bills.map(bill => {
                        const selectedPayments = selectPayments(payments, bill._id);
                        const result = selectPersons(selectedPayments, persons);
                        const selectedPersons = Array.from(new Set(result[0]));
                        const paymentToPersonList = result[1];
                        return {
                            billId: bill._id,
                            billTitle: bill.title,
                            initiator: mapPerson(bill.initiator),
                            paymentToPersonList: paymentToPersonList,
                            paymentsList: mapPayments(selectedPayments),
                            personsList: mapPersons(selectedPersons)
                        }
                    });

                    res.status(200).json({
                        bills: responseBillsList,
                    });
                })
                .catch(err => {
                    respondWithError(err, res);
                });
            })
            .catch(err => {
                respondWithError(err, res);
            });
        })
        .catch(err => {
            respondWithError(err, res);
        })
    })
    .catch(err => {
        respondWithError(err, res);
    });
});

router.get('/payment/:paymentId', (req, res, next) => {
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
    const initiator = req.body.initiator;

    // Check if the initiator exist.
    Person.findById(initiator)
        .then(person => {
        const bill = new Bill({
            initiator: person,
            title: req.body.title,
            date: req.body.date
        });

        console.log(req.body.paymentsList);

        return bill.save()
        .then(result => {
            console.log(result);
            res.status(201).json({
                billId: result._id,
                billTitle: result.title,
                initiator: result.initiator,
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

router.put('/payer', (req, res, next) => {
    console.log("AJUNG AICI");
    const paymentToPersonList = req.body;
    const payerId = paymentToPersonList[0].person.id;
    const payerName = paymentToPersonList[0].person.name;


    let paymentIdsList = []
    for (let i = 0; i < paymentToPersonList.length; i++) {
        const payment = paymentToPersonList[i].payment;
        paymentIdsList.push(payment.paymentId);
    }


    Payment.updateMany({_id: { $in: paymentIdsList} }, { $set: {"payerId": payerId} }).exec()
    .then(result => {
        Payment.findById(paymentIdsList[0]).exec()
        .then(payment => {
            Bill.findById(payment.billId)
            .populate("initiator", "name")
            .exec()
            .then(bill => {
                // console.log("From database:", bill);
                // If bill exist and is not null.
                if (bill) {
                    // Find payments that are assigned to this bill.
                    Payment.find( {billId: bill._id} ).exec()
                    .then(payments => {
                        // Map payments without billId.
                        responsePaymentsList = mapPayments(payments);
        
                        // Select person id from payments.
                        let personsIdsList = []
                        for (let i = 0; i < responsePaymentsList.length; i++) {
                            personsIdsList.push(responsePaymentsList[i].payerId);
                        }
        
                        console.log(personsIdsList);
        
                        Person.find( {_id: { $in: personsIdsList} } ).exec()
                        .then(persons => {
        
                            responsePersonsList = mapPersons(persons);
        
                            const bills = [bill];
                            const responseBillsList = bills.map(bill => {
                                const selectedPayments = selectPayments(payments, bill._id);
                                const result = selectPersons(selectedPayments, persons);
                                const selectedPersons = Array.from(new Set(result[0]));
                                const paymentToPersonList = result[1];
                                console.log("Payment to person list: \n" + paymentToPersonList);
                                return {
                                    billId: bill._id,
                                    billTitle: bill.title,
                                    initiator: bill.initiator,
                                    paymentToPersonList: paymentToPersonList,
                                    paymentsList: mapPayments(selectedPayments),
                                    personsList: mapPersons(selectedPersons)
                                }
                            });
            
                            res.status(200).json(responseBillsList[0]);
                        })
                        .catch(err => {
                            res.status(500).json({
                                message: "Internal error" + err
                            });
                        });
                    })
                    .catch(err => {
                        respondWithError(err, res);
                    });
                } else {
                    res.status(404).json({
                        message: "No valid entry for provided ID:" + id
                    });
                }
            })
            .catch(err => {
                respondWithError(err, res);
            });
        })
        .catch(err => {
            respondWithError(err, res);
        });
    })
    .catch(err => {
        respondWithError(err, res);
    });
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





function respondWithError(err, res) {
    console.log(err);
    res.status(500).json({
        error: err
    });
}

function selectPayments(payments, billId) {

    let selectedPayments = [];
    for (let i = 0; i < payments.length; i++) {
        if ("" + payments[i].billId == "" + billId) {
            selectedPayments.push(payments[i]);
        }
    }
    return selectedPayments;
} 

function selectPersons(payments, persons) {
    let selectedPersons = [];
    let paymentsToPersons = [];
    for (let i = 0; i < payments.length; i++) {
        for (let j = 0; j < persons.length; j++) {
            if ("" + persons[j]._id == "" + payments[i].payerId) {
                selectedPersons.push(persons[j]);
                paymentsToPersons.push({
                    payment: mapPayment(payments[i]),
                    person: mapPerson(persons[j])
                })
            }
        }
    }
    return [selectedPersons, paymentsToPersons];
}

function mapPayments(payments) {
    const mapedPayments =  payments.map(payment => {
       return mapPayment(payment);
    });
    return mapedPayments;
}

function mapPersons(persons) {
    return persons.map(person => {
        return mapPerson(person);
    });
}

function mapPayment(payment) {
    if (payment) {
        return {
            paymentId: payment._id,
            productName: payment.productName,
            productPrice: payment.productPrice,
            payerId: payment.payerId
        }
    }
}

function mapPerson(person) {
    if (person) {
        return {
            id: person._id,
            name: person.name
        }
    }
}