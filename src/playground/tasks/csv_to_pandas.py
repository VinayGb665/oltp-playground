from .app import app
from faust import Record
import pandas as pd
from .operators.row_operator import RowOperator


class SchemaRecordGenerator:
    def __init__(self, schema):
        self.schema = schema

    def convert(self):
        return


csv_topic = app.topic("faust.csvs.2", value_type=bytes)


class PandasOperator:
    def __init__(self, dataframe: object = None, operation: str = None):

        if self.validate_operation(operation):
            self.dataframe = dataframe
            self.operator = self.get_operator(operation)

    @staticmethod
    def validate_operation(operation, n=100):
        supported_operations = ["topn", "avg"]

        if operation.get("name") in supported_operations:
            return True
        return False

    def row_filter_opertor(self, operation: dict):
        pass

    async def column_filter_operator(self, operation: dict):
        """
        Parameters:
            operation: dict : Manifest of operation: {
                'column' : column_name,
                'output_topic': output topic for filtered data
                'name' : 'column_filter'
            }
        """

        column_name = operation.get("column_name")
        output_topic = operation.get("output_topic")

    def topn_operator(self, operation: dict):
        """
        Parameters:
            operation: dict : Manifest of operation: {
                'column' : column_name,
                'n': number of rows to return,
                'name' : 'topn'
            }
        """
        column_name = operation.get("column_name")
        n_top = operation.get("n", 100)
        return self.dataframe.nlargest(n_top, column_name)

    def get_operator(self, operation):
        operator_map = {
            "topn": self.topn_operator,
            "columnn_filter": self.column_filter_operator,
        }
        return operator_map.get(operation.get("name"))

    def __call__(
        self,
    ):
        return self.operator()


@app.agent(csv_topic)
async def greet(rows):
    headers = []
    columns = []
    count = 0
    df = pd.DataFrame()
    output_topic = app.topic("faust.output.csvs.3")
    async for row in rows:
        axis = (1,)
        count += 1
        if count == 1:
            headers = row
            print(headers)
            await output_topic.send(value=row)
        else:
            transformed_row = RowOperator(
                row=row, columns=headers, operating_columns=["a"]
            ).drop_columns()
            await output_topic.send(value=transformed_row)


output_topic = app.topic("faust.output.csvs.3")


@app.agent(output_topic)
async def show_transformed(rows):
    async for row in rows:
        print(f"######## -{row}- ##########")
