var express = require('express');
var game = require('./../server/game');
var router = express.Router();

// select a tile
router.get('/select/:tile/:player', function(req, res) {
	var tile = req.params.tile,
		player = req.params.player;
	console.log('tile: ' + tile + ', player: ' + player)
	var success = game.selectTile(tile, player);
	console.log('success: ' + success);
	res.json({success: success});
});

module.exports = router;
