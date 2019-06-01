const mongoose = require('mongoose');

const personSchema = mongoose.Schema({
    _id: {type: mongoose.Schema.Types.ObjectId, auto: true },
    initiator: { type: mongoose.Schema.Types.ObjectId, ref: 'Person', required: false },
    title: { type: String, require: false },
    date: { type: String, require: false },
});

module.exports = mongoose.model('Bill', personSchema);