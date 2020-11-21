import pandas as pd


class RowOperator:
    def __init__(
        self, row: list = [], columns: list = [], operating_columns: list = []
    ):
        self.row = row
        self.columns = columns
        self.operating_columns = operating_columns

    def drop_columns(
        self,
    ):
        df = pd.DataFrame(data=[self.row], columns=self.columns)
        # print(df.columns)
        df.drop(self.operating_columns, axis=1, inplace=True)
        # print(df)
        return df.values.tolist()


if __name__ == "__main__":
    op = RowOperator(row=[1, 2, 4], columns=["a", "b", "c"], operating_columns=["a"])
    op.drop_columns()
