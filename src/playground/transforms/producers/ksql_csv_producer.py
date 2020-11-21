import os
from kafka import KafkaProducer


class CSVToKSQL:
    def __init__(self, file_path: str = None):
        if not (os.path.exists(file_path)):
            raise ValueError("Fuck off file doesnt exist")
        else:
            self.file_path = file_path
        self.producer = KafkaProducer(
            bootstrap_servers="public-kafka-965d1e0-clicklock3-a9c3.aivencloud.com:14508",
            security_protocol="SSL",
            ssl_cafile="ca.pem",
            ssl_certfile="service.cert",
            ssl_keyfile="service.key",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
