from csv_to_topic import CSVLoader
from topic_to_sqlite import SQLiteDumper
import os
from time import time
class CSVPlayground():
    def __init__(self, file_path :str = None, topic: str = None):
        self.file_path = file_path
        self.loader = CSVLoader(topic=topic)
        self.dumper = SQLiteDumper(topic=topic)

    def run(self, ):
        ## Pump data into kafka get the schema
        schema = self.loader.publish(path=self.file_path, type='csv')
        ## Read from kafka into sqlite
        return self.dumper.dump(type='csv', schema=schema)

if __name__ == "__main__":
    base_dir = "/home/vinay/Downloads/ecomm-ds/brazilian-ecommerce/"
    total_start_time = time()
    file_count = 0
    total_rows = 0
    for each_csv in os.listdir(base_dir):
        file_count+=1
        start_time = time()
        print(f"## Running csv playground for {each_csv}")
        file_path = os.path.join(base_dir, each_csv)
        topic = each_csv[:-4]
        csvplay = CSVPlayground(file_path=file_path, topic=topic)
        total_rows+= csvplay.run()
        print(f"## Finished in {time()-start_time}s \n\n")
    print(f"\n ################ SUMMARY - Finished pumping and databasing {file_count} files in {time()-total_start_time}s \n Total Rows - {total_rows}")