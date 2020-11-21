import faust
import json

app = faust.App(
    "hello-world",
    broker="kafka://localhost:9092",
    value_serializer="json",
)
