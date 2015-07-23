<?php
define('APPLICATION_ENV', $_SERVER['APPLICATION_ENV']);

$allow_admin = false;
if(APPLICATION_ENV==='golden'){
	$site_root   = "http://golden/langblos/";
	$node_root   = "http://golden/node/";
	$media_root  = "http://golden/media/";
	$allow_admin = true;
}else if(APPLICATION_ENV==='copper'){
	$site_root   = "http://copper/app/";
	$node_root   = "http://copper/node/";
	$media_root  = "http://copper/media/";
	$allow_admin = false;
}else if($_SERVER['SERVER_NAME']==='www.decumanus.com' || $_SERVER['SERVER_NAME']){
	$site_root   = "http://www.decumanus.com/app/";
	$node_root   = "http://www.decumanus.com/node/";
	$media_root  = "http://www.decumanus.com/media/";
	$allow_admin = false;
}

$application = array(

		'php'         => array('params'   => array('backend','php'),
								  'pathvars' => array('base','panel','item','entry'),
								  'requireadmin' =>  FALSE,),


);





//if (class_exists('Mongo')) { }else { 
   // error_log('Mongo not installed');
   // MongoDB is not installed
//}
$basepath = dirname($_SERVER['SCRIPT_NAME']);
if($basepath==='/'){
	$basepath='';
}
$extrapath_vars       = explode("/",substr($_SERVER['REQUEST_URI'],strlen($basepath)+1));

error_log(">>>>> REQUEST [".APPLICATION_ENV."] ".$_SERVER['REQUEST_URI']);

function parse_request($_extrapath_vars,$_keys){
			$_num_extrapath_vars = count($_extrapath_vars);
			$_request = array();
			foreach($_keys as $_key){
				$_request[$_key] = null;
			}
			if($_num_extrapath_vars>1){
				$_first          = $_extrapath_vars[1]; 
				$_request[$_keys[0]] = $_first;
				if($_num_extrapath_vars>2){
					$_request[$_keys[1]]  = $_extrapath_vars[2];	
					if($_num_extrapath_vars>3){
						$_item              = urldecode($_extrapath_vars[3]);
						$_request[$_keys[2]]   = str_replace('_', ' ', $_item);					
						if($_num_extrapath_vars>4){							
							for($_ie=4;$_ie<$_num_extrapath_vars;$_ie++){									
								if($_ie % 2 == 0){
									$_key = $_extrapath_vars[$_ie];
									$_request['options'][$_key] = "1";
								}							
							} 							
						}
					}
				}
			}
			return $_request;
}
$_debug   = false;

$app_script_map     = array();

foreach($application as $_app_script => $_props){
	foreach($_props['params'] as $_param){
		$app_script_map[$_param] = $_app_script;
	}
}
$_template          = "_index.php"; //default

if($extrapath_vars){
	$num_extrapath_vars = count($extrapath_vars);
	if($num_extrapath_vars>0){
		$_app_script        = $app_script_map[$extrapath_vars[0]];
				
		if(isset($application[$_app_script])  && (!$application[$_app_script]['requireadmin'] || $allow_admin) ){
			$app_path           = "apps/".$_app_script."/";
			$app_root           = $site_root.$app_path;
			if(isset($application[$_app_script]['template'])){
				$_template          = $app_path.$application[$_app_script]['template'];	
			}
			
			$_request           = parse_request($extrapath_vars,$application[$_app_script]['pathvars']);
			if(isset($application[$_app_script]['require'])){
				foreach($application[$_app_script]['require'] as $_require){
					require($_require);
				}	
			}
			
			if(isset($_request)){
				if(!isset($_request['options'])){
        			$_request['options'] = array();
      			}
     			if(!isset($_request['debug'])){
        			$_request['debug'] = FALSE;
      			}
			}
		}	
	}
}
	  

require $_template;



?>

