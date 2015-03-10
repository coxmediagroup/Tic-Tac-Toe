/**
 * Prod vs Debug (move later for production configuration)
 */
process.env.NODE_ENV = 'development';

/**
 * Logging Configuration
 */
var log4js = require('log4js');
var appLogger = require('./service/routes/logger/logger');
var logger = appLogger.LOG;
logger.info("Starting Application...");

/**
 * EXPRESS CONFIGURATIONS
 */
var path = require('path');
var favicon = require('static-favicon');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var expressSession = require('express-session');
var express = require('express');

var tictactoeapp = express();

tictactoeapp.use(favicon());
tictactoeapp.use(bodyParser.json());
tictactoeapp.use(bodyParser.urlencoded());
tictactoeapp.use(cookieParser());
tictactoeapp.use(express.static(path.join(__dirname, 'webapp')));
tictactoeapp.use(express.static(path.join(__dirname, 'service')));

tictactoeapp.set('views', path.join(__dirname, 'webapp'));
tictactoeapp.engine('.html', require('ejs').renderFile);
tictactoeapp.set('view engine', 'html');

/**
 * DEBUGGING
 */
tictactoeapp.use(log4js.connectLogger(logger, {
    level : log4js.levels.DEBUG
}));

/**
 * Route Configurations for Middleware and API exposure
 */
var routescan = require('express-routescan');
routescan(tictactoeapp, {
    directory : [ path.join(__dirname, 'service/routes/endpoints') ],
    ext : [ '.rt', '.js' ],
    ignoreInvalid : true,
    verbose : true,
    strictMode : true
});

/**
 * ERROR HANDLERS
 * 
 * development error handler will print stacktrace
 */
// catch 404 and forward to error handler
tictactoeapp.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// Development error middleware handlers
if (tictactoeapp.get('env') === 'development') {

    tictactoeapp.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message : err.message,
            error : err
        });
    });

} else {

    // production error handler
    // no stacktraces leaked to user
    tictactoeapp.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message : "HTTP/" + err.status + " " + err.message,
            error : {}
        });
    });

}

/**
 * route to Angular homepage
 */
tictactoeapp.get('*', function(req, res) {
    res.sendfile('index.html');
});

/**
 * Modules
 */
module.exports = tictactoeapp;
