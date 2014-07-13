# -*- coding: utf-8 -*-
"""
==============
Flask Settings
==============

``TESTING``
	enable/disable testing mode

``PROPAGATE_EXCEPTIONS``
	explicitly enable or disable the propagation of exceptions.
	If not set or explicitly set to None this is implicitly true
	if either TESTING or DEBUG is true.

``PRESERVE_CONTEXT_ON_EXCEPTION``
	By default if the application is in debug mode the request context
	is not popped on exceptions to enable debuggers to introspect the data.
	This can be disabled by this key. You can also use this setting to
	force-enable it for non debug execution which might be useful to debug
	production applications (but also very risky).

``SECRET_KEY``
	the secret key

``SESSION_COOKIE_NAME``
	the name of the session cookie

``SESSION_COOKIE_DOMAIN``
	the domain for the session cookie. If this is not set, the cookie will be
	alid for all subdomains of SERVER_NAME.

``SESSION_COOKIE_PATH``
	the path for the session cookie. If this is not set the cookie will be
	valid for all of APPLICATION_ROOT or if that is not set for '/'.

``SESSION_COOKIE_HTTPONLY``
	controls if the cookie should be set with the httponly flag.
	Defaults to True.

``SESSION_COOKIE_SECURE``
	controls if the cookie should be set with the secure flag.
	Defaults to False.

``PERMANENT_SESSION_LIFETIME``
	the lifetime of a permanent session as datetime.timedelta object.
	Starting with Flask 0.8 this can also be an integer representing seconds.

``SESSION_REFRESH_EACH_REQUEST``
	this flag controls how permanent sessions are refreshed.
	If set to True (which is the default) then the cookie is refreshed
	each request which automatically bumps the lifetime.
	If set to False a set-cookie header is only sent if the session is modified.
	Non permanent sessions are not affected by this.

``USE_X_SENDFILE``
	enable/disable x-sendfile

``LOGGER_NAME``
	the name of the logger

``SERVER_NAME``
	the name and port number of the server.
	Required for subdomain support (e.g.: 'myapp.dev:5000')
	Note that localhost does not support subdomains so setting this to
	“localhost” does not help. Setting a SERVER_NAME also by default enables
	URL generation without a request context but with an application context.

``APPLICATION_ROOT``
	If the application does not occupy a whole domain or subdomain this can be
	set to the path where the application is configured to live. This is for
	session cookie as path value. If domains are used, this should be None.

``MAX_CONTENT_LENGTH``
	If set to a value in bytes, Flask will reject incoming requests with a
	content length greater than this by returning a 413 status code.

``SEND_FILE_MAX_AGE_DEFAULT:``
	Default cache control max age to use with send_static_file() (the default
	 static file handler) and send_file(), in seconds. Override this value on
	 a per-file basis using the get_send_file_max_age() hook on Flask or
	 Blueprint, respectively. Defaults to 43200 (12 hours).

``TRAP_HTTP_EXCEPTIONS``
	If this is set to True Flask will not execute the error handlers of
	HTTP exceptions but instead treat the exception like any other and
	bubble it through the exception stack. This is helpful for hairy
	debugging situations where you have to find out where an HTTP exception
	is coming from.

``TRAP_BAD_REQUEST_ERRORS``
	Werkzeug’s internal data structures that deal with request specific data
	will raise special key errors that are also bad request exceptions.
	Likewise many operations can implicitly fail with a BadRequest exception
	for consistency. Since it’s nice for debugging to know why exactly it
	failed this flag can be used to debug those situations. If this config is
	set to True you will get a regular traceback instead.

``PREFERRED_URL_SCHEME``
	The URL scheme that should be used for URL generation if no URL scheme is
	available. This defaults to http.

``JSON_AS_ASCII``
	By default Flask serialize object to ascii-encoded JSON. If this is set to
	False Flask will not encode to ASCII and output strings as-is and return
	unicode strings. jsonify will automatically encode it in utf-8 then for
	transport for instance.

``JSON_SORT_KEYS``
	By default Flask will serialize JSON objects in a way that the keys are
	ordered. This is done in order to ensure that independent of the hash seed
	of the dictionary the return value will be consistent to not trash
	external HTTP caches. You can override the default behavior by changing
	this variable. This is not recommended but might give you a performance
	improvement on the cost of cachability.

``JSONIFY_PRETTYPRINT_REGULAR``
	If this is set to True (the default) jsonify responses will be pretty
	printed if they are not requested by an XMLHttpRequest object (controlled
	by the X-Requested-With header)
"""
from os.path import join as joinpath, abspath, dirname


DEBUG = True
TESTING = False
SECRET_KEY = '5610b66b69aa4e238b255fa1df340e50fc593a32222d602e65be2c4a4007ee44'


# Do last so options in the files below will override any defaults set above
from tictac.settings.flask.kvsession import *
