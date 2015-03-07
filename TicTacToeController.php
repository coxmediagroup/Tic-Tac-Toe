<?php

$data = 'hello world';



$return["json"] = json_encode($data);
$return["action"] = $_POST['action'];
$return["square"] = $_POST['square'];
echo json_encode($return);



?>