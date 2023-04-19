#!/bin/bash
#create log dir
if [ ! -d /data/server/logs/ ]; then
    mkdir -p /data/server/logs/
    echo "create server logs dir"
fi
echo "check db if not init"
python scripts/check_db.py
echo "start rulemanager"
python manage.py runserver 0.0.0.0:8088  --insecure --noreload
