const mongoose = require('mongoose');

const paymentSchema = mongoose.Schema({
    _id: { type: mongoose.Schema.Types.ObjectId, auto: true },
    billId: { type: mongoose.Schema.Types.ObjectId, ref: 'Bill', required: true },
    payerId: { type: mongoose.Schema.Types.ObjectId, ref: 'Person', required: false },
    productName: { type: String, require: true },
    productPrice: { type: String, require: true },
});

module.exports = mongoose.model('Payment', paymentSchema);