#!/bin/bash
# Create a new user and database for a project

USER=$1
PASS=$2
WEBDIR=/var/www
USCRIPT=userscript.sql;

if [ "${PASS}" == "" ]; then
  echo "Missing parameter!"
  echo "Usage: $0 username password"
  exit 1
fi

if [ ! -d "/home/${USER}" ]; then
  echo "User ${USER} is to be created"
  adduser "${USER}"
fi

echo "Adding ${USER} to group wheel"
adduser "${USER}" wheel

echo "
cd /var/www/${USER} && source bin/activate
" >> /home/${USER}/.profile

echo "Creating website directory ${WEBDIR}/${USER}"
# already in fabfile
mkdir "${WEBDIR}/${USER}"
chown -R "${USER}:${USER}" "${WEBDIR}/${USER}"
echo "Creating symlink in user's home"
# already in fabfile
ln -s "${WEBDIR}/${USER}" "/home/${USER}/www"
chown -R "${USER}:${USER}" "/home/${USER}"

echo "
create user '${USER}'@'localhost' identified by '${PASS}';
create database ${USER} character set 'utf8';
grant all privileges on ${USER}.* to '${USER}'@'localhost';
flush privileges;
" > ${USCRIPT}

echo "Setting up ${USER} in MySQL. Please enter password for root:"
mysql -u root -p -D mysql < ${USCRIPT}
rm ${USCRIPT}
