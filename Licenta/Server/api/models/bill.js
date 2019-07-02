const mongoose = require('mongoose');

const Person = require("../models/person");

const billSchema = mongoose.Schema({
    _id: {type: mongoose.Schema.Types.ObjectId, auto: true },
    initiator: { type: mongoose.Schema.Types.ObjectId, ref: 'Person',
        required: true },
    title: { type: String, require: true },
    date: { type: String, require: false },
    persons: { type: [{
        id: String,
        name: String,
        status: Boolean
    }], require: false}
});

module.exports = mongoose.model('Bill', billSchema);