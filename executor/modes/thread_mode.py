import json
import copy
import networkx as nx
import threading
from time import sleep
from executor.graph_generator import gnp_random_connected_graph
from .base_mode import BaseMode
import random

class ThreadMode(BaseMode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def task(self, name):
        print(f" == >>Runninng {name} ")
        sleep(5)

    def spawn_thread_task(self, id):
        t = threading.Thread(target=self.task, args=[id])
        t.start()
        self.processed_nodes.add(id)
        return t

    def check_if_any_alive(self, thread_pool):
        for thread in thread_pool:
            if thread.is_alive():
                return True
    
    def join_thread_pool(self, thread_pool):
        for thread in thread_pool:
            thread.join()
    
    def parse_graph(self, g=None):
        if g==None:
            g = self.create_networkx_graph()
        
        if list(nx.simple_cycles(g)):
            print("Cycles were found in the workflow. Exiting")
            return
        
        all_nodes = g.nodes()
        queue = []
        downstreamed_nodes = self.list_all_downstreamed_nodes()
        
        start_nodes = all_nodes - downstreamed_nodes
        queue+=start_nodes
        while queue:
            temp_queue = copy.deepcopy(queue)
            queue = set()
            thread_pool = []
            for i in temp_queue:
                run = self.run_or_queue(g, i)
                if run:
                    print(f"Processing node - {i}")
                    thread = self.spawn_thread_task(i)
                    thread_pool.append(thread)
                    out_edges = g.edges(i)
                    for _, nextnode in out_edges:
                        queue.add(nextnode)
                else:
                    print(f"Dependent nodes were not ready/failed for node {i}, so queuing now")
                    self.queued_nodes.add(i)
                
            self.join_thread_pool(thread_pool)


if __name__ == "__main__":
    req = json.loads(open('samples/request_sample2', 'r').read())
    shit = ThreadMode(req=req)
    shit.parse_graph()