/*
 * Create a simple web server to display files
 */

var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname + '/client')).listen(8000);