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

router.post('/', upload.single('billImage'), (req, res, next) => {
    // Mock for products and prices.
    // Here we should look for existance of payments for this bill.
    const payments = [{
        productName: "product1",
        productPrice: 12.33
    }, {
        productName: "product2",
        productPrice: 1.50
    }, {
        productName: "product3",
        productPrice: 1
    }, {
        productName: "product4",
        productPrice: 4
    }, {
        productName: "product5",
        productPrice: 10
    }, {
        productName: "product6",
        productPrice: 0.75
    }, {
        productName: "product7",
        productPrice: 5
    }, {
        productName: "product8",
        productPrice: 20
    }, {
        productName: "product9",
        productPrice: 29
    }, {
        productName: "product10",
        productPrice: 11
    }, {
        productName: "product11",
        productPrice: 56
    }];
    res.status(200).json(payments);
});

module.exports = router;