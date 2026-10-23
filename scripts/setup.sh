# How the droplet is set up for this site (for reference; run by hand, as root,
# from the repo root at /home/damiens-site-3). nginx config lives in
# /etc/nginx/sites-available/damiensnyder.com.

# Python + deps: uv manages its own Python under /opt/uv/python
#   (uv binary from https://github.com/astral-sh/uv/releases -> /usr/local/bin)
export UV_PYTHON_INSTALL_DIR=/opt/uv/python
uv python install 3.13
uv venv --python 3.13 .venv
uv pip install --python .venv -r requirements.txt

# The app runs as the unprivileged user 'sites', which may only write the db,
# media/ and logs/ (plus sqlite journal files in the repo root).
useradd --system --no-create-home --shell /usr/sbin/nologin sites
usermod -aG sites www-data   # lets nginx reach the gunicorn socket
chgrp sites . && chmod 775 .
chown sites:sites db.sqlite3 && chown -R sites:sites media logs
chown root:sites secrets.json && chmod 640 secrets.json

cp scripts/damiens-site-3.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now damiens-site-3

# Weekly db backups (crontab -e):
#   10 2 * * 5 /home/damiens-site-3/scripts/backup_database.sh >> /home/damiens-site-3/backups/backup.log 2>&1
