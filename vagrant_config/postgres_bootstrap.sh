apt-get update
apt-get install -y postgresql-9.1
apt-get install -y postgresql-server-dev-9.1

sudo -u postgres psql -c "CREATE ROLE tic_tac_toe SUPERUSER LOGIN PASSWORD 'tic_tac_toe'"
sudo -u postgres psql -c 'CREATE DATABASE tic_tac_toe OWNER = tic_tac_toe'

echo "listen_addresses = '*'" >> /etc/postgresql/9.1/main/postgresql.conf 
echo "host    all             all             10.0.2.2/32             md5" >> /etc/postgresql/9.1/main/pg_hba.conf

sudo -u postgres /etc/init.d/postgresql restart