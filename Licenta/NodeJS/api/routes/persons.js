const express = require('express');
const router = express.Router();

// Models.
const Person = require('../models/person');

router.get('/', (req, res, next) => {
    // find().where for query, .limit to limit persons.
    Person.find()
    .select('name _id') // select this fields from objects
    .exec()
    .then(docs => {
        res.status(200).json(docs);
    })
    .catch(err => {
        console.log(err);
        res.status(500).json({
            error: err
        });
    });
});

router.get('/name/:personName', (req, res, next) => {
    const personName = req.params.personName;
    Person.findOne({ name:personName })
    .select("_id name")
    .exec()
    .then(doc => {
        console.log("From database:", doc);
        if (doc) {
            res.status(200).json(doc);
        } else {
            res.status(404).json({ message: "No person found!" });
        }
    })
    .catch(err => {
        console.log(err);
        res.status(404).json({ error: err });
    });
});

router.get('/id/:personId', (req, res, next) => {
    const personId = req.params.personId;
    Person.findById(personId)
    .select("_id name")
    .exec()
    .then(doc => {
        console.log("From database:", doc);
        if (doc) {
            res.status(200).json(doc);
        } else {
            res.status(404).json({ message: "No person found!" });
        }
    })
    .catch(err => {
        console.log(err);
        res.status(404).json({ error: err });
    });
});


router.post("/name/:personName", (req, res, next) => {

    const proposedName = req.params.personName;
    console.log(proposedName)
    Person.findOne({ name:proposedName })
    .select("_id name")
    .exec()
    .then(doc => {
        console.log("From database:", doc);
        if (doc) {
            res.status(403).json({ message: "Username already used!" });
        } else {
            // Create a person object and extract body params.
            let person = new Person({
                name: proposedName
            });
            // Store person and respond with person object created.
            person.save()
            .then(result => {
                console.log(result);
                res.status(201).json({
                    name: result.name,
                    id: result._id,
                });
            })
            .catch(err => {
                console.log(err);
                res.status(500).json({ message: "Could not save!" });
            });
        }
    })
    .catch(err => {
        console.log(err);
        res.status(404).json({ error: err });
    });

        
});


router.put('/:personId', (req, res, next) => {
    const id = req.params.personId;

    // Create object with fields to update.
    const updateOps = {};
    for (const ops of req.body) {
        updateOps[ops.propName] = ops.value;
    }

    // Update object.
    Person.update({ _id: id}, { $set: updateOps })
    .exec()
    .then(result => {
        res.status(200).json({
            message: 'Person updated!',
            request: {
                type: "GET",
                url: 'http://localhost:8080/persons/' + id
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
    Person.find()
    .exec()
    .then(docs => {
        console.log(docs);
        Person.deleteMany({}).exec().then(result => {
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

router.delete('/name/:personName', (req, res, next) => {
    const personName = req.params.personName;
    Person.deleteOne({ name: personName })
    .exec()
    .then(result => {
        console.log(result);
        if (result.n > 0) {
            res.status(200).json({
                message: "Succesfully deleted!"
            });
        } else {
            res.status(404).json({
                message: "User not found!"
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

router.delete('/id/:personId', (req, res, next) => {
    const personId = req.params.personId;
    Person.deleteOne({ _id: personId })
    .exec()
    .then(result => {
        console.log(result);
        if (result.n > 0) {
            res.status(200).json({
                message: "Succesfully deleted!"
            });
        } else {
            res.status(404).json({
                message: "User not found!"
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

module.exports = router;