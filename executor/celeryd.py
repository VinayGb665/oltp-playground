from celery import Celery
from .config import BaseConfig

app = Celery(
    "DAG Runtime",
    broker=BaseConfig.redis_url,
    result_backend=BaseConfig.redis_url,
)
app.conf.result_backend = BaseConfig.redis_url
