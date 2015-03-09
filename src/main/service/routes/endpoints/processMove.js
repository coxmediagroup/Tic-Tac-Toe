var express = require('express');
var router = express.Router();
var appLogger = require('../logger/logger');
var logger = appLogger.LOG;
var doSomething = require('../middleware/middleware');

'use strict';

module.exports = {

    '/ping' : {
        methods : [ 'get' ],
        fn : function(req, res) {
            logger.debug("Ping Check");

            doSomething.doit();

            res.json({
                currentTimeMs : new Date().getTime() / 1000
            })
        };
    },
    '/more' : {
        methods : [ 'get' ],
        fn : function(req, res) {

        }
    }
};
