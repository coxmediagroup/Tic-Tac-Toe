<?php

$globalLogFileName = 'application.log';

error_reporting(E_ALL ^ E_WARNING ^ E_NOTICE);

// these MUST match the values inside JsonResponse class in
// the client iOS application code
define('RC_OK',			              0);
define('RC_NO_VERSIONS',              -102);
define('RC_LOCK_FAILED',		      -103);
define('RC_SQL_FAILED',	              -104);
define('RC_CONNECTION_FAILED',        -106);
define('RC_BAD_INPUT',			      -108);
define('RC_EXCEPTION',			      -109);
define('RC_ERROR',				      -110);
define('RC_OBJECT_NOT_FOUND',		  -111);
define('RC_TEST_ERROR',			      -2000);
define('RC_NO_DATA',                  -9999);

// these MUST match the values inside CommittablObject class in
// the client side iOS application code
define('COMMIT_NONE',   0);
define('COMMIT_ADD',    1);
define('COMMIT_MODIFY', 2);
define('COMMIT_DELETE', 3);


// Helper method to get a string description for an HTTP status code
// From http://www.gen-x-design.com/archives/create-a-rest-api-with-php/ 
function getStatusCodeMessage($status)
{
    // these could be stored in a .ini file and loaded
    // via parse_ini_file()... however, this will suffice
    // for an example
    $codes = Array(
        100 => 'Continue',
        101 => 'Switching Protocols',
        200 => 'OK',
        201 => 'Created',
        202 => 'Accepted',
        203 => 'Non-Authoritative Information',
        204 => 'No Content',
        205 => 'Reset Content',
        206 => 'Partial Content',
        300 => 'Multiple Choices',
        301 => 'Moved Permanently',
        302 => 'Found',
        303 => 'See Other',
        304 => 'Not Modified',
        305 => 'Use Proxy',
        306 => '(Unused)',
        307 => 'Temporary Redirect',
        400 => 'Bad Request',
        401 => 'Unauthorized',
        402 => 'Payment Required',
        403 => 'Forbidden',
        404 => 'Not Found',
        405 => 'Method Not Allowed',
        406 => 'Not Acceptable',
        407 => 'Proxy Authentication Required',
        408 => 'Request Timeout',
        409 => 'Conflict',
        410 => 'Gone',
        411 => 'Length Required',
        412 => 'Precondition Failed',
        413 => 'Request Entity Too Large',
        414 => 'Request-URI Too Long',
        415 => 'Unsupported Media Type',
        416 => 'Requested Range Not Satisfiable',
        417 => 'Expectation Failed',
        500 => 'Internal Server Error',
        501 => 'Not Implemented',
        502 => 'Bad Gateway',
        503 => 'Service Unavailable',
        504 => 'Gateway Timeout',
        505 => 'HTTP Version Not Supported'
    );
 
    return (isset($codes[$status])) ? $codes[$status] : '';
}

function sendJsonResponse($result)
{
	if (isError($result))
	{
		logError('Sending error (rc = ' . $result['rc'] . '): ' . $result['message']);
	}
	
    header('HTTP/1.1 200 OK');
    header('Content-type: text/json');
    $body = json_encode($result);
    echo $body;
}


function getUserIdHeader()
{
	return $_SERVER['HTTP_X_INFINITURE_USERID'];
}


function configLogFileName($fileName)
{
	global $globalLogFileName;
	$globalLogFileName = $fileName;
}


function logInfo($message)
{
	if (func_num_args() > 1)
	{
		$args = func_get_args();
	    $message = vsprintf($message, array_slice($args, 1));
	}

	global $globalLogFileName;
	$dateTime = new DateTime("now", new DateTimeZone('America/New_York'));
	$timestamp = $dateTime->format("Y-m-d H:i:s");
    error_log("[$timestamp] INFO: ".$message."\n", 3, APP_DIR.'/logs/' . $globalLogFileName);
}


function logWarn($message)
{
	if (func_num_args() > 1)
	{
		$args = func_get_args();
	    $message = vsprintf($message, array_slice($args, 1));
	}

	global $globalLogFileName;
	$dateTime = new DateTime("now", new DateTimeZone('America/New_York'));
	$timestamp = $dateTime->format("Y-m-d H:i:s");
    error_log("[$timestamp] WARN: ".$message."\n", 3, APP_DIR.'/logs/' . $globalLogFileName);
}


function logError($message)
{
	if (func_num_args() > 1)
	{
		$args = func_get_args();
	    $message = vsprintf($message, array_slice($args, 1));
	}

	global $globalLogFileName;
	$dateTime = new DateTime("now", new DateTimeZone('America/New_York'));
	$timestamp = $dateTime->format("Y-m-d H:i:s");
    error_log("[$timestamp] ERROR: ".$message."\n", 3, APP_DIR.'/logs/' . $globalLogFileName);
}

function isProdEnvironment()
{
	static $isProd = null;
	
	// determine this property only once
	if ($isProd === null)
	{
		$isProd = (strrpos(getDatabaseName(), '_prod') > 0);
		logInfo('Production environment flag is set to: ' . ($isProd ? 'YES' : 'NO'));
	}

	return $isProd;
}

function isValetIdValid($valetId, $mysqli)
{	
	return isUserIdValid($driverId, $mysqli, 'valet');
}

function isDriverIdValid($driverId, $mysqli)
{
	return isUserIdValid($driverId, $mysqli, 'driver');
}

function isUserIdValid($userId, $mysqli, $tableName)
{
	// validate inputs
	if (!isset($userId) ||
		strlen($userId) == 0 ||
    	!isset($tableName) ||
    	strlen($tableName == 0))
	{
		return makeError(RC_BAD_INPUT, 'Bad or insufficient input');
	}
	
	// connect to DB if a connection was not provided
	if (!isset($mysqli))
	{
		$mysqli = createDbConnection();
		if ($mysqli->connect_errno)
		{
			return makeError(RC_CONNECTION_FAILED, "Failed to connect to MySQL: " . $mysqli->connect_error);
		}
	}
	
	$query = "SELECT objectId" .
			 " FROM ?" . 
			 " WHERE objectId = ?" .
			 " AND status = 1";

	// prepare the statement
	$stmt = $mysqli->stmt_init();
	if (!$stmt->prepare($query))
	{
		return makeError(RC_SQL_FAILED, 'Failed to prepare statement: ' . $stmt->error);
	}

	// bind and execute the statement
	$stmt->bind_param('ss', $tableName, $userId);
	$stmt->execute();
	$stmt->bind_result($userId);
	if (!$stmt->fetch())
	{
		return makeError(RC_OBJECT_NOT_FOUND, 'Specified user does not exist in table: ' . $tableName);
	}
	
	return makeSuccess();
}


function acquireLock($name, $timeoutSeconds = 10)
{
	// validate the inputs
	if (strlen($name) == 0)
	{
		logError("Failed to acquire lock because its name is empty.");
		return NULL;
	}
	else if (!preg_match('/^[a-zA-Z0-9-_]+$/', $name))
	{
		logError("Failed to acquire lock ($name) because its name contains invalid characters.");
		return NULL;
	}
	
	$totalSlept = 0;	
	while (true)
	{
		$fp = fopen(APP_DIR."/mutexes/mutex_$name.lock", "w");
		if (flock($fp, LOCK_EX | LOCK_NB))
		{
			logInfo("Acquired lock: $name");
			$lock = array();
			$lock['name'] = $name;
			$lock['fp'] = $fp;
			return $lock;
		}
		
		// break the loop if timeout has been hit
		if ($totalSlept >= $timeoutSeconds)
		{
			break;
		}
		
		logError("Failed to acquire lock ($name), sleeping for one second");
		sleep(1);
		
		$totalSlept += 1;
	}
	
	logInfo("Failed to acquire lock ($name), timeout expired");
	return NULL;
}


function releaseLock($lock)
{
	if ($lock != NULL &&
		is_array($lock) &&
		array_key_exists('fp', $lock))
	{
		flock($lock['fp'], LOCK_UN);
		logInfo("Released lock: " . $lock['name']);
		
		return true;
	}
	
	return false;
}

function generateCurrentDateString()
{
	$currentDate = new DateTime("now", new DateTimeZone('UTC'));
	$currentDateStr = $currentDate->format('Y-m-d H:i:s');
	return $currentDateStr;
}

function generateUuid()
{
	mt_srand((double)microtime()*10000);//optional for php 4.2.0 and up.
	$charid = strtoupper(md5(uniqid(rand(), true)));
	$hyphen = chr(45);// "-"
	$uuid = substr($charid, 0, 8).$hyphen .
			substr($charid, 8, 4).$hyphen .
			substr($charid,12, 4).$hyphen .
			substr($charid,16, 4).$hyphen .
			substr($charid,20,12);
	return $uuid;
}

function makeError($rc, $message)
{
	$result = array();
	$result['rc'] = $rc;
	$result['message'] = $message;
	return $result;
}

function makeSuccess($payload, $message)
{
	$result = array();
	$result['rc'] = RC_OK;
	$result['message'] = (isset($message) ? $message : '');
	$result['payload'] = $payload; // null allowed
	return $result;
}

function isError($error)
{
	return ($error['rc'] != RC_OK);
}

?>
