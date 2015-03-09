var express = require('express');
var router = express.Router();
var appLogger = require('../logger/logger');
var logger = appLogger.LOG;

/*
 * PLACEHOLDER FOR DELETION
 */

var Obj = {

    doit : function() {
        logger.debug("Done!");
    }
};

module.exports = Obj;
