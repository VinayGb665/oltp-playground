import json
from api import celery, app
from src.playground.csv_to_topic import CSVLoader
from src.utils import Consumer
from src.utils.pykafka_clients import Producer


@celery.task
def add_data(a, b):
    """Background task to send an email with Flask-Mail."""
    with app.app_context():
        print(f"A + B invoked {a+b}")


@celery.task(bind=True)
def start_csv_producer(self, *args, **kwargs):
    """
    Celery task to convert csv data to topic
    """
    print(kwargs)
    file_path = kwargs.get("file_path")
    topic = kwargs.get("topic")
    loader = CSVLoader(topic=topic)
    schema = loader.publish(
        path=file_path,
        type="csv",
    )


@celery.task(bind=True, time_limit=200)
def pull_transform_push(self, *args, **kwargs):
    ## Pull Transform Push task for row filter
    output_topic = kwargs.get("output_topic")
    input_topic = kwargs.get("input_topic")
    tranform_value = kwargs.get("value", "Claire Gute")
    column_index = kwargs.get("index")

    ## Using hardcoded filter now - equal
    cons = Consumer(topic=input_topic, group_id=output_topic).get_consumer()
    producer = Producer(topic=output_topic).get_producer()
    count = 0
    for msg in cons:
        row_value = json.loads(msg.value.decode("utf-8"))
        if row_value[column_index] == tranform_value:
            print(f"Found , tranforming and sending - {row_value} {output_topic}")
            producer.produce(json.dumps(row_value).encode("utf-8"))
        else:
            count += 1
            print(f"Discared {count}", end="\r")
        cons.commit()
