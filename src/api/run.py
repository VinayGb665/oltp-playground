from api.app import app, api
from time import sleep
from flask_rest_api import Api, Blueprint
import os
from flask import Response, request, render_template
from src.utils.pykafka_clients import Consumer
import json
from src.api.tasks import add_data, start_csv_producer, pull_transform_push
from flask_redoc import Redoc
from pykafka.common import OffsetType


redoc = Redoc(app, "petstore.yml")


info = {
    "version": 1,
    "topics": [{"name": "Topic Visualizer", "topic": "covid.data.2 "}],
}
data_blueprint = Blueprint(
    "streams", "streams", url_prefix="/", description="Operations on streams"
)


@data_blueprint.route("/")
def basic_info():
    return info


@data_blueprint.route("/data/<string:topic>")
def fetch_data(topic):
    def event_handler():
        consumer = Consumer(
            topic=topic,
        ).get_consumer()
        # consumer._auto_offset_reset()
        for each_msg in consumer:
            sleep(2)
            yield f'\r\ndata: {json.loads(each_msg.value.decode("utf-8"))}\nOffest: {each_msg.offset}\n'

    return Response(event_handler(), mimetype="text/event-stream")


@data_blueprint.route("/publish/<string:file_name>/", methods=["GET", "POST"])
def publish_connection(file_name):
    if request.method == "GET":
        return "AA IDK"

    topic = request.json.get("topic", "default")
    print(request.json, os.path.join(app.config["UPLOAD_FOLDER"], file_name))

    kwargs = {
        "topic": topic,
        "file_path": os.path.join(
            "/home/vinay/SIDE_HOE/oltp_playground/src/api/downloads", file_name
        ),
    }
    info["topics"].append(kwargs)

    sender_id = start_csv_producer.delay(**kwargs)
    return Response({"status": "Task created", "id": sender_id})


@data_blueprint.route("/transform/<string:topic>/filter", methods=["POST"])
def transform_and_spit(topic):
    print(request.json)
    output_topic = request.json.get("output_topic")
    filter_column = request.json.get("column")
    columns = request.json.get("headers")
    value = request.json.get("value")
    kwargs = {
        "output_topic": output_topic,
        "input_topic": topic,
        "index": columns.index(filter_column),
        "value": value,
    }
    info["topics"].append(kwargs)
    pull_transform_push.delay(**kwargs)
    print(kwargs)
    return {"ok": 1}


@data_blueprint.route("/visualize")
def view_data():
    return render_template("index.html")


api.register_blueprint(data_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2233, debug=True)
