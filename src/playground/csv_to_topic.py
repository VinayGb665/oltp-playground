from kafka import KafkaProducer, KafkaAdminClient
from src.playground.tasks import app
import asyncio
import json
import os
import csv


class ValidationError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class DataLoader:
    def __init__(
        self,
        topic: str = "",
    ):
        # self.kafka_admin = KafkaAdminClient(bootstrap_servers="public-kafka-965d1e0-clicklock3-a9c3.aivencloud.com:14508",
        #                 security_protocol="SSL",
        #                 ssl_cafile="ca.pem",
        #                 ssl_certfile="service.cert",
        #                 ssl_keyfile="service.key",
        #             )
        # self.producer = KafkaProducer(bootstrap_servers='localhost', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.producer = KafkaProducer(
            bootstrap_servers="public-kafka-965d1e0-clicklock3-a9c3.aivencloud.com:14508",
            security_protocol="SSL",
            ssl_cafile="/home/vinay/SIDE_HOE/oltp_playground/src/playground/ca.pem",
            ssl_certfile="/home/vinay/SIDE_HOE/oltp_playground/src/playground/service.cert",
            ssl_keyfile="/home/vinay/SIDE_HOE/oltp_playground/src/playground/service.key",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self.pub_topic = topic

    def flush(
        self,
    ):
        ## Drop the topic before trying to send
        self.kafka_admin.delete_topics([self.pub_topic], timeout_ms=2000)

    def publish(self, *args, **kwargs):
        raise NotImplementedError


class CSVLoader(DataLoader):
    @staticmethod
    def validate_kwargs(
        kwargs,
    ):
        if kwargs.get("type") != "csv":
            raise ValidationError(
                "Wrong loader", errors="Loader chosen was wrong based on the argumnets"
            )
        if not (os.path.exists(kwargs.get("path"))):
            raise ValidationError(
                f'Invalid path {kwargs.get("path")}',
                errors="Path does not exist or cannot access",
            )

    @staticmethod
    def get_csv_reader(file_path: str, skip_header: bool = False):
        csvfile = open(file_path, "r")
        reader = csv.reader(csvfile)
        if skip_header:
            headers = next(reader)
        else:
            headers = []
        return headers, reader

    @staticmethod
    def make_schema_from_headers(headers):
        schema = {}
        for i in headers:
            schema[i.strip()] = "text"
        return schema

    def publish(self, *args, **kwargs):
        self.validate_kwargs(kwargs)
        # self.flush()
        headers, reader = self.get_csv_reader(kwargs.get("path"))
        nrows = 0
        print("Starting producer 0-0 %")
        loop = asyncio.get_event_loop()
        for row in reader:
            nrows += 1
            outtopic = app.topic(self.pub_topic)

            loop.run_until_complete(
                outtopic.send(value=json.dumps(row).encode("utf-8"))
            )
            # self.producer.send(self.pub_topic, row)
        print(f"Finished producing events, headers are {headers}, nrows= {nrows}")
        return self.make_schema_from_headers(headers)


if __name__ == "__main__":
    loader = CSVLoader(topic="my-csv-1")
    schema = loader.publish(
        path="/home/vinay/SIDE_HOE/oltp_playground/src/api/downloads/test1.csv",
        type="csv",
    )
    # schema = loader.publish(path='/home/vinay/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/01-22-2020.csv', type='csv', )
