from kafka import KafkaProducer, KafkaAdminClient
import json
import os
import csv
class ValidationError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

class DataLoader():
    def __init__(self, topic: str='', ):
        self.kafka_admin = KafkaAdminClient(bootstrap_servers="public-kafka-965d1e0-clicklock3-a9c3.aivencloud.com:14508",
                        security_protocol="SSL",
                        ssl_cafile="ca.pem",
                        ssl_certfile="service.cert",
                        ssl_keyfile="service.key",
                    )
        # self.producer = KafkaProducer(bootstrap_servers='kafka-51c344b-clicklock3-a9c3.aivencloud.com:14498', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.producer = KafkaProducer(
                        bootstrap_servers="public-kafka-965d1e0-clicklock3-a9c3.aivencloud.com:14508",
                        security_protocol="SSL",
                        ssl_cafile="ca.pem",
                        ssl_certfile="service.cert",
                        ssl_keyfile="service.key",
                        value_serializer=lambda v: json.dumps(v).encode('utf-8')
                    )
        self.pub_topic = topic

    def flush(self,):
        ## Drop the topic before trying to send
        self.kafka_admin.delete_topics([self.pub_topic], timeout_ms=2000)
    
    def publish(self, *args, **kwargs):
        raise NotImplementedError

class CSVLoader(DataLoader):
    @staticmethod
    def validate_kwargs(kwargs, ):
        if kwargs.get('type') != 'csv':
            raise ValidationError('Wrong loader', errors='Loader chosen was wrong based on the argumnets')
        if not(os.path.exists(kwargs.get('path'))):
            raise ValidationError('Invalid path', errors='Path does not exist or cannot access')
    
    @staticmethod
    def get_csv_reader(file_path: str, ):
        csvfile =  open(file_path,'r')
        reader = csv.reader(csvfile)
        headers = next(reader)
        return headers, reader

    @staticmethod
    def make_schema_from_headers(headers):
        schema = {}
        for i in headers:
            schema[i.strip()] = 'text'
        return schema
    


    def publish(self, *args, **kwargs):
        self.validate_kwargs(kwargs)
        # self.flush()
        headers, reader = self.get_csv_reader(kwargs.get('path'))
        nrows = 0
        print("Starting producer 0-0 %")
        for row in reader:
            nrows+=1
            self.producer.send(self.pub_topic, row)
        print(f"Finished producing events, headers are {headers}, nrows= {nrows}")
        return self.make_schema_from_headers(headers)

if __name__ == "__main__":
    loader = CSVLoader(topic='guru')
    schema = loader.publish(path='/home/vinay/Downloads/csvs/2005_-_2015_Graduation_Outcomes.csv', type='csv', )
