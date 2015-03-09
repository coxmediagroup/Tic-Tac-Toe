var log4js = require('log4js');

log4js.configure({
    appenders : [ {
        type : 'console'
    } ]
});

/**
 * log4js.configure({ appenders : [ { type : 'console' }, { type : 'file',
 * filename : "app.log", category : 'app' } ] });
 */

var logger = log4js.getLogger('tictactoeapp');
logger.setLevel('DEBUG');

Object.defineProperty(exports, "LOG", {
    value : logger
});
