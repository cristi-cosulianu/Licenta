const express = require('express');
const app = express();
const morgan = require('morgan');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const personsRoutes = require('./api/routes/persons');
const billsRoutes = require('./api/routes/bills');
const scriptRoutes = require('./api/routes/runscript');

mongoose.connect('mongodb+srv://admin:admin@mbsdatabase-iowya.mongodb.net/test?retryWrites=true', {
    useNewUrlParser: true
});

// For logging.
app.use(morgan('dev'));

// For body parsing.
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

// Add headers for Cross-Origin.
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header(
        'Access-Control-Allow-Headers', 
        'Origin, X-Requested, Content-Type, Accept, Authorization'
    );

    if (req.method === 'OPTIONS') {
        res.header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE');
        return res.status(200).json({});
    }
    next();
});


// Routes which should handle requests.
app.use('/persons', personsRoutes);
app.use('/bills', billsRoutes);
app.use('/runscript', scriptRoutes);


// Catch all other routes.
app.use((req, res, next) => {
    const error = new Error('Route not found!');
    error.status = 404;
    next(error);
});

// Catch all errors from application.
app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
        error: {
            message: error.message,
            request: req.body
        }
    });
    console.log({
        request: new Date().toISOString()
    });
});

module.exports = app;