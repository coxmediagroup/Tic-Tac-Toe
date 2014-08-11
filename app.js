var express = require('express');
var env = process.env.NODE_ENV = process.env.NODE_ENV || 'development';
var app = express();
var config = require('./server/config/config')[env];

require('./server/config/express')(app, config);
require('./server/routes/default')(app);
require('./server/routes/gameroutes')(app);
module.exports = app;
