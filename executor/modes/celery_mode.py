import json
import copy
import networkx as nx
from executor.task_manager import TaskManager
from .base_mode import BaseMode
from .poller import task_poller

class CeleryMode(BaseMode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def parse_graph(self, g=None):
        tm = TaskManager()
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
            task_pool = []
            for i in temp_queue:
                run = self.run_or_queue(g, i)
                if run:
                    print(f"Processing node - {i}")
                    task_id = tm.spawn_task(i)
                    self.processed_nodes.add(i)
                    task_pool.append(task_id)
                    out_edges = g.edges(i)
                    for _, nextnode in out_edges:
                        queue.add(nextnode)
                else:
                    print(f"Dependent nodes were not ready/failed for node {i}, so queuing now")
                    self.queued_nodes.add(i)
                
            task_poller(task_pool, tm)

if __name__ == "__main__":
    req = json.loads(open('samples/request_sample2', 'r').read())
    shit = CeleryMode(req=req)
    shit.parse_graph()