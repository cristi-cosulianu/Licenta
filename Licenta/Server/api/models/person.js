const mongoose = require('mongoose');

const personSchema = mongoose.Schema({
    _id: {type: mongoose.Schema.Types.ObjectId, auto: true },
    name: {type: String, required: true}
});

module.exports = mongoose.model('Person', personSchema);