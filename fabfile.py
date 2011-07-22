#!/usr/bin/env python
# -*- coding: utf-8 -*-
# fabfile for Django:
# http://morethanseven.net/2009/07/27/fabric-django-git-apache-mod_wsgi-virtualenv-and-p/
# modified for fabric 0.9/1.0
from __future__ import with_statement # needed for python 2.5
from fabric.api import *
import time

# globals
env.prj_name = 'project_name' # no spaces!
env.use_photologue = False # django-photologue gallery module
env.use_daemontools = False
env.use_supervisor = True
env.use_celery = False
env.webserver = 'nginx' # nginx or apache2 (directory name below /etc!)
env.dbserver = 'mysql' # mysql or postgresql
# TODO: database and SSH setup, see tools/makeuser.sh

# environments

def localhost():
    "Use the local virtual server"
    env.hosts = ['localhost']
    env.user = 'adriannye' # You must create and sudo-enable the user first!
    env.path = '/Users/%(user)s/workspace/%(prj_name)s' % env # User home on OSX, TODO: check local OS
    env.virtualhost_path = env.path
    env.pysp = '%(virtualhost_path)s/lib/python2.6/site-packages' % env
    env.tmppath = '/var/tmp/django_cache/%(prj_name)s' % env

def webserver():
    "Use the actual webserver"
    env.hosts = ['tictactoe.zoomflip.com'] # Change to your server name!
    env.user = env.prj_name
    env.path = '/var/www/%(prj_name)s' % env
    env.virtualhost_path = env.path
    env.pysp = '%(virtualhost_path)s/lib/python2.5/site-packages' % env
    env.tmppath = '/var/tmp/django_cache/%(prj_name)s' % env
   
# tasks

def test():
    "Run the test suite and bail out if it fails"
    local("cd %(path)s; python manage.py test" % env) #, fail="abort")
    
    
def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    require('hosts', provided_by=[localhost,webserver])
    require('path')
    # install Python environment
    sudo('apt-get install -y build-essential python-dev python-setuptools python-imaging python-virtualenv python-yaml')
    # install some version control systems, since we need Django modules in development
    sudo('apt-get install -y git-core') # subversion git-core mercurial
        
    # install more Python stuff
    # Don't install setuptools or virtualenv on Ubuntu with easy_install or pip! Only Ubuntu packages work!
    sudo('easy_install pip')

    if env.use_daemontools:
        sudo('apt-get install -y daemontools daemontools-run')
        sudo('mkdir -p /etc/service/%(prj_name)s' % env, pty=True)
    if env.use_supervisor:
        sudo('pip install supervisor')
        sudo('echo; if [ ! -f /etc/supervisord.conf ]; then echo_supervisord_conf > /etc/supervisord.conf; fi', pty=True) # configure that!
        sudo('echo; if [ ! -d /etc/supervisor ]; then mkdir /etc/supervisor; fi', pty=True)
    if env.use_celery:
        sudo('apt-get install -y rabbitmq-server') # needs additional deb-repository!
        if env.use_daemontools:
            sudo('mkdir -p /etc/service/%(prj_name)s-celery' % env, pty=True)
        # for supervisor, put celery's "program" block into supervisor.ini!
    
    # install webserver and database server
    sudo('apt-get remove -y apache2 apache2-mpm-prefork apache2-utils') # is mostly pre-installed
    if env.webserver=='nginx':
        sudo('apt-get install -y nginx')
    else:
        sudo('apt-get install -y apache2-mpm-worker apache2-utils') # apache2-threaded
        sudo('apt-get install -y libapache2-mod-wsgi') # outdated on hardy!
    if env.dbserver=='mysql':
        sudo('apt-get install -y mysql-server python-mysqldb')
    elif env.dbserver=='postgresql':
        sudo('apt-get install -y postgresql python-psycopg2')
        
    # disable default site
    with settings(warn_only=True):
        sudo('cd /etc/%(webserver)s/sites-enabled/; rm default;' % env, pty=True)
    
    # new project setup
    sudo('mkdir -p %(path)s; chown %(user)s:%(user)s %(path)s;' % env, pty=True)
    sudo('mkdir -p %(tmppath)s; chown %(user)s:%(user)s %(tmppath)s;' % env, pty=True)
    with settings(warn_only=True):
        run('cd ~; ln -s %(path)s www;' % env, pty=True) # symlink web dir in home
    with cd(env.path):
        run('virtualenv .') # activate with 'source ~/www/bin/activate'
        with settings(warn_only=True):
            run('mkdir -m a+w logs; mkdir releases; mkdir shared; mkdir packages; mkdir backup;', pty=True)
            if env.use_photologue:
                run('mkdir photologue', pty=True)
                #run('pip install -E . -U django-photologue' % env, pty=True)
            if env.use_medialibrary:
                run('mkdir medialibrary', pty=True)
            run('cd releases; ln -s . current; ln -s . previous;', pty=True)
    deploy('first')
    
def deploy(param=''):
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and 
    then restart the webserver
    """
    require('hosts', provided_by=[localhost,webserver])
    require('path')
    env.release = time.strftime('%Y%m%d%H%M%S')
    upload_tar_from_git()
    install_requirements()
    install_site()
    symlink_current_release()
    migrate(param)
    restart_webserver()
    
def deploy_version(version):
    "Specify a specific version to be made live"
    require('hosts', provided_by=[localhost,webserver])
    require('path')
    env.version = version
    with cd(env.path):
        run('rm -rf releases/previous; mv releases/current releases/previous;', pty=True)
        run('ln -s %(version)s releases/current' % env, pty=True)
    restart_webserver()
    
def rollback():
    """
    Limited rollback capability. Simply loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    require('hosts', provided_by=[localhost,webserver])
    require('path')
    with cd(env.path):
        run('mv releases/current releases/_previous;', pty=True)
        run('mv releases/previous releases/current;', pty=True)
        run('mv releases/_previous releases/previous;', pty=True)
        # TODO: use South to migrate back
    restart_webserver()    
    
# Helpers. These are called by other functions rather than directly

def upload_tar_from_git():
    "Create an archive from the current Git master branch and upload it"
    require('release', provided_by=[deploy, setup])
    local('git archive --format=tar master | gzip > %(release)s.tar.gz' % env)
    run('mkdir -p %(path)s/releases/%(release)s' % env, pty=True)
    put('%(release)s.tar.gz' % env, '%(path)s/packages/' % env)
    run('cd %(path)s/releases/%(release)s && tar zxf ../../packages/%(release)s.tar.gz' % env, pty=True)
    local('rm %(release)s.tar.gz' % env)
    
def install_site():
    "Add the virtualhost config file to the webserver's config, activate logrotate"
    require('release', provided_by=[deploy, setup])
    with cd('%(path)s/releases/%(release)s' % env):
        sudo('cp %(webserver)s.conf /etc/%(webserver)s/sites-available/%(prj_name)s' % env, pty=True)
        if env.use_daemontools: # activate new service runner
            sudo('cp service-run.sh /etc/service/%(prj_name)s/run; chmod a+x /etc/service/%(prj_name)s/run;' % env, pty=True)
        else: # delete old service dir
            sudo('echo; if [ -d /etc/service/%(prj_name)s ]; then rm -rf /etc/service/%(prj_name)s; fi' % env, pty=True)
        if env.use_supervisor: # activate new supervisor.ini
            sudo('cp supervisor.ini /etc/supervisor/%(prj_name)s.ini' % env, pty=True)
        else: # delete old config file
            sudo('echo; if [ -f /etc/supervisor/%(prj_name)s.ini ]; then supervisorctl %(prj_name)s:appserver stop rm /etc/supervisor/%(prj_name)s.ini; fi' % env, pty=True)
        if env.use_celery:
            sudo('cp service-run-celeryd.sh /etc/service/%(prj_name)s-celery/run; chmod a+x /etc/service/%(prj_name)s-celery/run;' % env, pty=True)
        # try logrotate
        with settings(warn_only=True):        
            sudo('cp logrotate.conf /etc/logrotate.d/website-%(prj_name)s' % env, pty=True)
    with settings(warn_only=True):        
        sudo('cd /etc/%(webserver)s/sites-enabled/; ln -s ../sites-available/%(prj_name)s %(prj_name)s' % env, pty=True)
    
def install_requirements():
    "Install the required packages from the requirements file using pip"
    require('release', provided_by=[deploy, setup])
    run('cd %(path)s; pip install -E . -r ./releases/%(release)s/requirements.txt' % env, pty=True)
    
def symlink_current_release():
    "Symlink our current release"
    require('release', provided_by=[deploy, setup])
    with cd(env.path):
        run('rm releases/previous; mv releases/current releases/previous;', pty=True)
        run('ln -s %(release)s releases/current' % env, pty=True)
        # copy South migrations from previous release, if there are any
        run('cd releases/previous/%(prj_name)s; if [ -d migrations ]; then cp -r migrations ../../current/%(prj_name)s/; fi' % env, pty=True)
        # collect static files
        with cd('releases/current/%(prj_name)s' % env):
            run('%(path)s/bin/python manage.py collectstatic -v0 --noinput' % env, pty=True)
            if env.use_photologue:
                run('cd static; rm -rf photologue; ln -s %(path)s/photologue photologue;' % env, pty=True)
    
def migrate(param=''):
    "Update the database"
    require('prj_name')
    require('path')
    env.southparam = '--auto'
    if param=='first':
        run('cd %(path)s/releases/current/%(prj_name)s; %(path)s/bin/python manage.py syncdb --noinput' % env, pty=True)
        env.southparam = '--initial'
    #with cd('%(path)s/releases/current/%(prj_name)s' % env):
    #    run('%(path)s/bin/python manage.py schemamigration %(prj_name)s %(southparam)s && %(path)s/bin/python manage.py migrate %(prj_name)s' % env)
    #    # TODO: should also migrate other apps! get migrations from previous releases
    
def restart_webserver():
    "Restart the web server"
    require('webserver')
    env.port = '8'+run('id -u', pty=True)[1:]
    with settings(warn_only=True):
        if env.webserver=='nginx':
            require('path')
            if env.use_daemontools:
                sudo('kill `cat %(path)s/logs/django.pid`' % env, pty=True) # kill process, daemontools will start it again, see service-run.sh
            if env.use_supervisor:
                sudo('supervisorctl restart %(prj_name)s:appserver' % env, pty=True)
                if env.use_celery:
                    sudo('supervisorctl restart %(prj_name)s:celery' % env, pty=True)
            #require('prj_name')
            #run('cd %(path)s; bin/python releases/current/%(prj_name)s/manage.py runfcgi method=threaded maxchildren=6 maxspare=4 minspare=2 host=127.0.0.1 port=%(port)s pidfile=./logs/django.pid' % env)
        sudo('/etc/init.d/%(webserver)s reload' % env, pty=True)
