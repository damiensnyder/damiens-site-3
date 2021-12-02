# starts the server for production.
# run this from the base directory (i.e., `damiens-site-3`). type
#     sh scripts/start.sh
# to run it
kill -9 `ps aux | grep uwsgi | grep -v grep | awk '{print $2}'`
python3 manage.py collectstatic --no-input
/etc/init.d/nginx restart
uwsgi --socket damiens-site-3.sock --module damienssite3.wsgi --chmod-socket=666 --daemonize=/var/log/uwsgi/damiens-site-3.log