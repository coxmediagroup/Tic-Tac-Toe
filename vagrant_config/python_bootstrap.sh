#python_bootstrap.sh

apt-get update
apt-get -y install python-pip
pip install -i https://restricted.crate.io/ virtualenv

mkdir /home/vagrant/.virtualenv
sudo virtualenv -v --distribute /home/vagrant/.virtualenv/tic_tac_toe

source /home/vagrant/.virtualenv/tic_tac_toe/bin/activate
pip install -i https://restricted.crate.io/ django==1.4.5. django-tastypie south