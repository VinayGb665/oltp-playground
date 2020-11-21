from pykafka import KafkaClient
from pykafka.common import OffsetType


class Consumer:
    def __init__(self, topic: str = None):
        self.client = KafkaClient(
            hosts="localhost:9092",
        )
        self.topic = topic

    def get_consumer(self):
        topic = self.client.topics[self.topic]
        return topic.get_simple_consumer(
            consumer_group=self.topic,
            auto_offset_reset=OffsetType.LATEST,
            reset_offset_on_start=False,
            auto_commit_enable=True,
        )


class Producer:
    def __init__(self, topic: str = None):
        self.client = KafkaClient(
            hosts="localhost:9092",
        )
        self.topic = topic

    def get_producer(self):
        topic = self.client.topics[self.topic]
        return topic.get_producer()
