import faust
import json
import faust


app = faust.App(
    "csv_dealer_1",
    broker="kafka://kafka-51c344b-clicklock3-a9c3.aivencloud.com:14498",
    value_serializer=json,
)


kafka_topic = app.topic("guru")


@app.agent(kafka_topic)
async def process(transactions):
    async for value in transactions:
        # result = requests.post('http://127.0.0.1:5000/invocations', json=json.loads(value))
        print("Input data: " + str(value))
        # print('Fraud detection result: ' + str(result.json()))
