#! /bin/sh
chmod +x venv/bin/activate
./venv/bin/activate
export export PYTHONPATH=$PWD/src

python -m src.api.run