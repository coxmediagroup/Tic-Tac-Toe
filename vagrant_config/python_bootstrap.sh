#python_bootstrap.sh

apt-get update
apt-get -y install python-pip
apt-get install -y python-dev
pip install -i https://restricted.crate.io/ virtualenv

mkdir /home/vagrant/.virtualenv
sudo virtualenv -v --distribute /home/vagrant/.virtualenv/tic_tac_toe

source /home/vagrant/.virtualenv/tic_tac_toe/bin/activate
pip install -i https://restricted.crate.io/ django==1.4.5
pip install -i https://restricted.crate.io/ psycopg2
pip install -i https://restricted.crate.io/ django-tastypie
pip install -i https://restricted.crate.io/ south
pip install -i https://restricted.crate.io/ unipath
pip install -i https://restricted.crate.io/ dj_database_url