# these are the commands i entered to set up the DigitalOcean droplet.
# after running these, i connected via FTP to send the whole directory with
# this repo over.
apt-get update
apt-get install python3-venv
apt install python3-pip
Y
python3 -m venv venv
pip install uwsgi
pip install django
pip install markdown
pip install markdown-katex
pip install markdown-customblocks
apt-get install nginx
/etc/init.d/nginx start
