<?php

	$return["action"] = $_POST['action'];
	$return["square"] = $_POST['square'];
	$return["sessionId"] = $_POST['sessionId'];
	$return["sessionId2"] = session_id ();
	echo json_encode($return);

?>