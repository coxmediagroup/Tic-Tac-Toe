Musings on the design
=====================

Dependencies
------------
Some of the implementation details such as using DictStore for the key/value
store backend, were not my first choice, but were chosen in order to keep
dependencies light. If the change was desired, it is trivial to use a different
back-end without having to make any code changes, other than in the imports and
`kvstore` instantiation. KVSession is capable of using the filesystem,
SQLAlchemy, MongoDB, Redis, memcached, Amazon S3, and Google Storage.

I originally really wanted to have everything be asynchronous. I began
work on prototyping a gevent based, RabbitMQ publish/consume service which
communicated with the browser using RabbitMQ's STOMP-over-WebSockets service
and SockJS. It would have had a REST API exposed through Flask and event
driven dispatchers to call into another REST API on the Django side.

However, I started to feel like the stack was doing too much of the heavy
lifting; which isn't normally a bad thing, but it was kind of defeating the
purpose of the exercise. Additionally, all the service dependencies were making
the deployment process a bit too involved. I briefly considered doing something
similar with 0MQ, however, I eventually settled on a much simpler design:
I love Postgres, but went for SQLite3 instead. Memcached or Redis would have
been solid choices for handling the KVSession key/value store stuff, but I
went with DictStore.

I guess what I am really trying to get at is: I know there are better options,
which I would use in a real-world application, but I didn't want you to have to
pull someone in from DevOps just to bootstrap my project. ;)

Flask-SocketIO
--------------
For a project of this size, I think that it is a good fit. Flask's
`session` worked well for storing state. However, using the @socketio decorator
on function views can get unwieldy quick. I would insist upon class-based views
if the application was any larger that it is.
