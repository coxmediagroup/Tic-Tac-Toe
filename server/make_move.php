<?php

define('APP_DIR', realpath('./'));

include_once APP_DIR."/utils/http_utils.php";
include_once APP_DIR."/commands/make_move_command.php";

configLogFileName("tictactoe_app.log");

// parse input
$jsonRequest = file_get_contents('php://input');
$tictactoeMoves = json_decode( $jsonRequest, TRUE );

// run command against input
$cmd = new MakeMoveCommand();
$result = $cmd->run($tictactoeMoves);

// return command result
sendJsonResponse($result)

?>
