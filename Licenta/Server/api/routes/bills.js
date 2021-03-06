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
const Payment = require("../models/payment");


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

router.get('/initiator/:initiatorId', (req, res, next) => {
    // Select the initiator id from url parameters.
    const initiatorId = req.params.initiatorId;
    Bill.find({ initiator: initiatorId })
    .populate("initiator", "name")
    .exec()
    .then(bills => {
        let billsIdsList = [];
        for (let i = 0; i < bills.length; i++) {
            billsIdsList.push(bills[i]._id);
        }
        Payment.find({billId: { $in: billsIdsList} }).exec()
        .then(payments => {
            let personsIdsList = [];
            for (let i = 0; i < payments.length; i++) {
                personsIdsList.push(payments[i].payerId);
            }
            Person.find( {_id: { $in: personsIdsList} } ).exec()
            .then(persons => {

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
    });
});

router.get('/:billId', (req, res, next) => {
    // Select the bill id from url parameters.
    const id = req.params.billId;
    // Find bill by id if it exists in database.
    Bill.findById(id)
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
                responsePaymentsList = payments.map(payment => {
                    return {
                        paymentId: payment._id,
                        productName: payment.productName,
                        productPrice: payment.productPrice,
                        payerId: payment.payerId
                    }
                });

                // Select person id from payments.
                let personsIdsList = []
                for (let i = 0; i < responsePaymentsList.length; i++) {
                    personsIdsList.push(responsePaymentsList[i].payerId);
                }

                console.log(personsIdsList);

                Person.find( {_id: { $in: personsIdsList} } ).exec()
                .then(persons => {

                    responsePersonsList = persons.map(person => {
                        return {
                            id: person._id,
                            name: person.name
                        }
                    });

                    // Create bill objects for response.
                    const responseBill = {
                        billId: bill._id,
                        billTitle: bill.title,
                        initiator: mapPerson(bill.initiator),
                        paymentToPersonList: [],
                        paymentsList: responsePaymentsList,
                        personsList: responsePersonsList
                    }
                    res.status(200).json(responseBill);
                })
                .catch(err => {
                    res.status(500).json({
                        message: "Internal error" + err
                    });
                });
            })
            .catch(err => {
                console.log(err);
                res.status(500).json({
                    message: "Internal error" + err
                });
            });
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
    console.log("initiatorId: " + req.body.initiator + '\n');

    // Check if the initiator exist.
    Person.findById(initiator.id)
    .then(person => {
        const bill = new Bill({
            initiator: req.body.initiator.id,
            title: req.body.billTitle,
        });
        console.log("bill: " + bill.title + '\n');
        console.log("initiator: " + bill.initiator + '\n');

        // Save new bill in database.
        return bill.save()
        .then(billResult => {
            console.log("billResult: " + billResult + '\n');
            
            // Create payments for current bill.
            const paymentsList = [];
            for (let i = 0; i < req.body.paymentsList.length; i++) {
                const payment = new Payment({
                    billId: billResult._id,
                    productName: req.body.paymentsList[i].productName,
                    productPrice: req.body.paymentsList[i].productPrice
                });
                paymentsList.push(payment);
            }
            
            Payment.insertMany(paymentsList)
            .then(results => {

                resultPaymentsList = results.map(result => {
                    return {
                        paymentId: result._id,
                        productName: result.productName,
                        productPrice: result.productPrice,
                        payerId: result.payerId
                    }
                })

                Bill.findById(billResult._id)
                .populate("initiator", "name")
                .exec()
                .then(newBill => {
                    console.log("NewBill: " + newBill);
                    const responseBill = {
                        billId: newBill._id,
                        billTitle: newBill.title,
                        initiator: mapPerson(newBill.initiator),
                        paymentToPersonList: [],
                        paymentsList: resultPaymentsList,
                        personsList: req.body.personsList
                    }
    
                    res.status(201).json(responseBill);
                    console.log("responseBill: " + responseBill + '\n');
                })
                .catch(err => {
                    respondWithError(err, res);
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
            console.log(err);
            res.status(500).json({
                error: err
            });
        });
    })
    .catch(err => {
        console.log(err);
        res.status(404).json({
            message: "No initiator with id: " + initiator.id,
            error: err
        });
    })
});


router.delete('/all', (req, res, next) => {
    Bill.find()
    .populate("initiator", "name")
    .exec()
    .then(docs => {
        console.log(docs);
        Bill.deleteMany({}).exec().then(result => {
            res.status(200).json(result);
        }).catch(err => {
            console.log(err);
            res.status(500).json({
                error: err
            })
        });
    })
    .catch(err => {
        console.log(err);
        res.status(500).json({
            error: err
        })
    });
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
