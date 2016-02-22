#!/bin/sh
# only for local build. remove for travis checkin
# TRAVIS_BUILD_DIR='/home/ravindra/janus-git/janus'
echo $TRAVIS_BUILD_DIR
cd $TRAVIS_BUILD_DIR
sudo addgroup opentrv --gid 510 
sudo adduser opentrv --uid 510 --gid 510 --system --no-create-home --disabled-password
# sudo adduser opentrv --gid 510
sudo usermod -aG sudo opentrv

# sudo mkdir /srv/opentrv
sudo chown -R opentrv:opentrv $TRAVIS_BUILD_DIR
sudo chmod -R 777 $TRAVIS_BUILD_DIR
sudo mkdir $TRAVIS_BUILD_DIR/database/
sudo mkdir $TRAVIS_BUILD_DIR/logs/
sudo -u postgres psql -c "create user opentrv --createdb --superuser --password 'secret'"
# sudo -u postgres psql -c "ALTER USER opentrv WITH PASSWORD 'secret';"
sudo -u postgres psql -c 'create database opentrv_db owner opentrv'
# sudo -u opentrv -s
# sudo cp $TRAVIS_BUILD_DIR/templates/gunicorn.conf.j2 /etc/init/opentrv_gunicorn.conf
# sudo cp $TRAVIS_BUILD_DIR/templates/nginx.conf.j2 /etc/nginx/sites-available/opentrv
# sudo ln /etc/nginx/sites-enabled/opentrv /etc/nginx/sites-available/opentrv
# sudo service nginx restart
# sudo service gunicorn restart
# sudo service udp_server restart
