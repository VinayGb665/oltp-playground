from sqlitedict import SqliteDict
from kafka import KafkaConsumer
from executor.config import BaseConfig

class BusHandler():
    def __init__(self,):
        self.consumer = KafkaConsumer(bootstrap_servers=BaseConfig.kafka_url)
        self.event_topic = "dagmanager"
        self.consumer.subsribe(self.event_topic)
    
    def start_consumer_thread(self):
        pass


class Pipeline():
    def __init__(self, *args, **kwargs):
        self.pipeid = kwargs.get('id')
        
    def add_step(self, start, end):
        pass
    
    def trigger(self, *args, **kwargs):
        pass

        
