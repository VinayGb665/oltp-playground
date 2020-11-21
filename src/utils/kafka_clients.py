from kafka import KafkaConsumer, KafkaProducer
from pykafka import KafkaClient


class Consumer:
    def __init__(self, topic: str = None, group_id=None):
        self.consumer = KafkaConsumer(
            bootstrap_servers="public-kafka-965d1e0-clicklock3-a9c3.aivencloud.com:14508",
            security_protocol="SSL",
            ssl_cafile="ca.pem",
            ssl_certfile="service.cert",
            ssl_keyfile="service.key",
            auto_offset_reset="earliest",
            consumer_timeout_ms=2000,
        )
        # self.consumer = KafkaConsumer(bootstrap_servers='localhost:9092', consumer_timeout_ms=3000, group_id=group_id, auto_offset_reset='earliest',api_version=(2,4,1),)
        self.topic = topic

    def get_consumer(self):
        self.consumer.subscribe(self.topic)
        return self.consumer


class Producer:
    def __init__(
        self,
    ):
        # self.producer = KafkaProducer(bootstrap_servers='localhost:9092',)
        self.producer = KafkaProducer(
            bootstrap_servers="public-kafka-965d1e0-clicklock3-a9c3.aivencloud.com:14508",
            security_protocol="SSL",
            ssl_cafile="ca.pem",
            ssl_certfile="service.cert",
            ssl_keyfile="service.key",
        )

    def get_producer(self):
        return self.producer
