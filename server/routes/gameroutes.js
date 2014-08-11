var game = require('../controllers/gamecontroller');

module.exports = function(app) { 
    app.put('/api/game',game.makeMove);
};