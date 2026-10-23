#!/bin/bash
# Deploys whatever is checked out. Run after `git pull`:
#     bash scripts/deploy.sh
# Add --static if static files changed (collectstatic takes ~4 minutes because
# of all the flag images):
#     bash scripts/deploy.sh --static
# The site runs as the systemd service damiens-site-3 (see
# scripts/damiens-site-3.service); logs: journalctl -u damiens-site-3
set -e
cd "$(dirname "$0")/.."

export UV_PYTHON_INSTALL_DIR=/opt/uv/python
[ -d .venv ] || uv venv --python 3.13 .venv
uv pip install --python .venv -r requirements.txt
if [ "$1" = "--static" ]; then
    .venv/bin/python manage.py collectstatic --no-input
fi
systemctl restart damiens-site-3
systemctl is-active damiens-site-3
