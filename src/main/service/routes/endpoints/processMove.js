var express = require('express');
var router = express.Router();
var appLogger = require('../logger/logger');
var logger = appLogger.LOG;
var middleware = require('../middleware/middleware');

'use strict';

module.exports = {

    '/ping' : {
        methods : [ 'get' ],
        fn : function(req, res) {
            logger.debug("Ping Check");

            middleware.doit();

            res.json({
                currentTimeMs : new Date().getTime() / 1000
            });
        }
    },
    '/checkboard' : {
        methods : [ 'post' ],
        fn : function(req, res) {

            logger.debug("-- Checking board endpoint --\n" + req.body);
            var win = middleware.checkwin(JSON.stringify(req.body));
            logger.debug("Win? " + win);
            res.send(win);
        }
    },
    '/automate' : {
        methods : [ 'post' ],
        fn : function(req, res) {

            logger.debug("-- Automating move for O --\n" + req.body);

            var newBoard = middleware.makeMove(req.body);

            res.send(newBoard);
        }
    }

};
