#! /bin/sh
export PYTHONPATH=$PWD/src
echo $PYTHONPATH
celery -A src.api.tasks.celery worker -l info -f logs/celery_worker.log --detach