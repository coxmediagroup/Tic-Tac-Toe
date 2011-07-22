Setup for a new server
======================

These are just some hints, not a complete list or tutorial!
Probably you won’t need all of these.

* user setup
  
  - create group wheel::
  
      adduser --group wheel
  
  - visudo::
  
      Defaults targetpw # ask for root password - makes sense?
      %wheel ALL=(ALL) ALL
  
  - set root password for MySQL::
  
      mysqladmin -u root password 'ROOTPW'

* install packages

  - add repo for RabbitMQ::
  
      echo "
      deb http://www.rabbitmq.com/debian/ testing main
      " >> /etc/apt/sources.list

  - see `package.list`

* install ConTeXt (alternative for LaTeX, if you need PDFs)

  - see http://wiki.contextgarden.net/ConTeXt_Minimals::
    
      mkdir /var/opt/context
      cd /var/opt/context
      rsync -av rsync://contextgarden.net/minimals/setup/first-setup.sh .
      sh ./first-setup.sh

  - edit PATH in `.bashrc` or `.profile`::
    
      export PATH=$PATH:/var/opt/context/tex/texmf-linux-64/bin
      . /var/opt/context/tex/setuptex

* TODO: SSH setup

  - copy authenticated_hosts to `/etc/skel/.ssh`

* Nginx setup

  - replace `/etc/nginx/fastcgi_params`
  - change `nginx.conf` according to my comments (or replace it)
  - add `/etc/nginx/proxy.conf` (my generic `nginx.conf` relies on it)

* startup / process management

  - start services::
  
      update-rc.d some_script defaults 09
  
  - delete apache start scripts::
  
      update-rc.d -f apache2 remove
  
  - adapt `/etc/supervisord.conf`::
    
      [include]
      files=/etc/supervisor/*.ini
     
