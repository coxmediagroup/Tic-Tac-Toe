<?php
	
?>
<?php
if($_request['base']==='winner'){
	$json  = json_decode(file_get_contents('record.json'),true);
	$total = $json['total'];
	if($_request['panel']==="0"){
		$total[2] = $total[2] + 1;
	}else if($_request['panel']==="o"){
		$total[0] = $total[0] + 1;
	}else if($_request['panel']==="x"){
		$total[1] = $total[1] + 1;
	}
	file_put_contents('record.json','{"total":['.$total[0].','.$total[1].','.$total[2].']}')
?>{ "winner" : "<?php echo $_request['panel'];?>" }<?php
}else if($_request['base']==='results'){
echo file_get_contents('record.json');
}
?>