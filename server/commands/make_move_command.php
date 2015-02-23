<?php

include_once APP_DIR."/utils/http_utils.php";

class MakeMoveCommand
{
	function __construct()
	{
		//
	}
	
	function run($tictactoeMoves)
	{
		logInfo("Make move command called.");
		
		$result = $tictactoeMoves;

		return $result;
	}
}