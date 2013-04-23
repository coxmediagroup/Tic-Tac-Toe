#python_bootstrap.sh

apt-get update
apt-get -y install python-pip
pip install virtualenv

mkdir /home/vagrant/.virtualenv
virtualenv -v --distribute /home/vagrant/.virtualenv/tic_tac_toe
