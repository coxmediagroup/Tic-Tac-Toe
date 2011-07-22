Tools for Django/Nginx
======================

Server management helpers for my setup:

* setup

  - server-setup.rst_: some hints what to do with a new (virtual) server
  - makeuser.sh_: create user, database and web directory for a new project
  - package.list_: my selection of installed packages on a new virtual server with Debian 5.0 (Lenny)
  - copysite.sh_: copy a complete site from another server (use for server migrations)

* process management with fcgi (obsolete with gunicorn)

  - nginxsite.sh_: start/stop one Django site running on fcgi behind Nginx
  - websites-init.sh_: start/stop/restart all Django sites (use e.g. as startup script)

Some of these functions will migrate to the fabfile sometime...

.. _server-setup.rst: ../../blob/master/tools/server-setup.rst
.. _makeuser.sh: ../../blob/master/tools/makeuser.sh
.. _package.list: ../../blob/master/tools/package.list
.. _copysite.sh: ../../blob/master/tools/copysite.sh
.. _nginxsite.sh: ../../blob/master/tools/nginxsite.sh
.. _websites-init.sh: ../../blob/master/tools/websites-init.sh
