git clone https://github.com/opentrv/janus.git /srv/opentrv/
sudo adduser opentrv --system --disabled-password --uid 510
sudo addgroup --gid 510 opentrv
sudo adduser --uid 510 opentrv --ingroup opentrv sudo
sudo mkdir /srv/opentrv
sudo chown -R opentrv:opentrv /srv/opentrv
sudo mkdir /srv/opentrv/database/
sudo mkdir /srv/opentrv/logs/
sudo -u postgres psql -c 'create user opentrv --createdb --superuser' 
sudo -u postgres psql -c 'create database opentrv_db owner opentrv'
sudo cp /srv/opentrv/templates/gunicorn.conf.j2 /etc/init/opentrv_gunicorn.conf
sudo cp /srv/opentrv/templates/nginx.conf.j2 /etc/nginx/sites-available/opentrv
sudo ln /etc/nginx/sites-enabled/opentrv /etc/nginx/sites-available/opentrv
sudo service nginx restart
sudo service gunicorn restart
sudo service udp_server restart