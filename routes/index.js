var express = require('express');
var game = require('./../server/game');
var router = express.Router();

// select a tile
router.get('/select/:tile/:player', function(req, res) {
	var tile = req.params.tile;
	var player = req.params.player;

	var response = game.selectTile(tile, player);
	res.json(response);
});

router.get('/reset', function(req, res) {
	game.reset();
	res.end()
});

module.exports = router;
