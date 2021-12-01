# starts the server for production.
# run this from the base directory (i.e., `damiens-site-3`). type
#     sh scripts/start.sh
# to run it
python3 manage.py collectstatic
yes
/etc/init.d/nginx restart
uwsgi --socket damiens-site-3.sock --module damienssite3.wsgi --chmod-socket=666 --daemonize=/var/log/uwsgi/damiens-site-3.log
