import sqlite3
from kafka import KafkaConsumer
import json


class ValidationError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class SQLiteDumper:
    @staticmethod
    def validate_kwargs(
        kwargs,
    ):
        if kwargs.get("type") != "csv":
            raise ValidationError(
                "Wrong loader", errors="Loader chosen was wrong based on the argumnets"
            )

    def __init__(
        self,
        topic: str = None,
    ):
        self.consumer = KafkaConsumer(
            bootstrap_servers="public-kafka-965d1e0-clicklock3-a9c3.aivencloud.com:14508",
            security_protocol="SSL",
            ssl_cafile="ca.pem",
            ssl_certfile="service.cert",
            ssl_keyfile="service.key",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            consumer_timeout_ms=2000,
        )
        self.topic = topic
        self.get_sqlite_connection()

    def get_sqlite_connection(
        self,
    ):
        self.sql_conn = sqlite3.connect("back_store.db")

    @staticmethod
    def create_table_query(schema: dict, table):
        base_query = [f"'{key}' {value}" for key, value in schema.items()]
        base_query = ", ".join(base_query)

        return f"create table if not exists {table} ({base_query}) "

    @staticmethod
    def insert_query(
        schema: dict,
        table,
    ):
        qmarks = ["?" for i in schema.keys()]
        qmarks = ", ".join(qmarks)

        return f" insert into {table} values ({qmarks})"

    def dump(self, *args, **kwargs):
        self.validate_kwargs(kwargs)

        self.consumer.subscribe(self.topic)
        cursor = self.sql_conn.cursor()
        cursor.execute(self.create_table_query(kwargs.get("schema"), self.topic))
        buffer = []
        buffer_size = 100
        counter = 0
        batch_counter = 0
        row_counter = 0

        for each_row in self.consumer:
            buffer.append(each_row.value)
            counter += 1
            row_counter += 1
            if counter == buffer_size:

                query = self.insert_query(kwargs.get("schema"), self.topic)
                # print(buffer)
                cursor.executemany(query, buffer)
                buffer = []
                counter = 0
                batch_counter += 1
                # print(f"##\t Inserted {batch_counter} batch\n")
        self.sql_conn.commit()
        self.sql_conn.close()
        return row_counter
        # break


if __name__ == "__main__":
    dumper = SQLiteDumper(topic="guru")
    headers = "Cohort Year,Cohort Category,Demographic,# Total Cohort,# Total Grads,% of cohort Total Grads,# of cohort Total Grads,% of cohort Total Regents,% of grads  Total Regents,# of grads  Total Regents,% of cohort  Advanced Regents,% of grads  Advanced Regents,# of grads  Advanced Regents,% of cohort  Regents w/o Advanced,% of grads  Regents w/o Advanced,# of grads  Regents w/o Advanced,% of cohort Local,% of grads Local,# Still Enrolled,% of cohort Still Enrolled,# Dropped Out,% of cohort Dropped Out"
    headers = headers.split(",")
    schema = {}

    for i in headers:
        schema[i] = "text"
    print(schema)
    dumper.dump(type="csv", schema=schema)
