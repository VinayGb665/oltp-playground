import json
import copy
import networkx as nx
import pprint
import collections
import matplotlib.pyplot as plt
import threading
from time import sleep
from executor.graph_generator import gnp_random_connected_graph
from executor.task_manager import TaskManager
from executor.poller import task_poller
import random

class SomeShit():
    def __init__(self, *args, **kwargs):
        self.convergence = 1
        self.processed_nodes = set()
        self.queued_nodes = set()
        self.graph_request = kwargs.get('req')
    
    def create_n_point_graph(self, n):
        graph = []
        for _ in range(0,n):
            graph.append([0]*n)
        return graph
    
    def get_name_to_point_map(self, ):
        dmap = {}

        for i in range(0, len(self.graph_request)):
            name = self.graph_request[i].get('name')
            dmap[name] = i
        return dmap
            
    def plot_graph_on_array(self,):
        nunique_points = len(self.graph_request)
        unplotted_graph = self.create_n_point_graph(nunique_points)
        dmap = self.get_name_to_point_map()

        if unplotted_graph:
            index = 0
            for point_outs in unplotted_graph:
                point_config = self.graph_request[index]
                downstreams = point_config.get("downstreams" , [])
                for other_point in downstreams:
                    other_point_index = dmap.get(other_point)
                    point_outs[other_point_index] = 1
                index+=1
        
        return unplotted_graph
    
    def list_nodes(self,):
        return [ i.get('name') for i in self.graph_request]
    
    def task(self, name):
        print(f" == >>Runninng {name} ")
        sleep(5)

    def spawn_thread_task(self, id):
        t = threading.Thread(target=self.task, args=[id])
        t.start()
        self.processed_nodes.add(id)
        return t

    def create_networkx_graph(self,):
        g = nx.DiGraph()
        nunique_points = len(self.graph_request)
        # nodes = list(range(1, nunique_points+1))
        nodes = self.list_nodes()
        g.add_nodes_from(nodes)
        print("=============")
        for point in self.graph_request:
            pointname = point.get('name')
            downstreams = point.get('downstreams')
            for each_downstream in downstreams:
                edge = (pointname, each_downstream)
                g.add_edge(*edge)
        print("=============")
        nx.draw(g,with_labels=True)
        # plt.show(block=False)
        # plt.pause(2)
        # plt.close()
        plt.savefig('latestdag.png')
        return g
    
    def run_or_queue(self, graph, node):
        """
            Returns true if run , false if to queue
        """

        in_nodes = [ innode for innode,_ in graph.in_edges(node)]
        print(in_nodes, self.processed_nodes)
        for dependentnode in in_nodes:
            if dependentnode not in self.processed_nodes:
                return False
        return True

    def list_all_downstreamed_nodes(self,):
        downstreams = []
        for point in self.graph_request:
            downstreams+=point.get('downstreams', [])
        return list(set(downstreams))
    
    def check_if_any_alive(self, thread_pool):
        for thread in thread_pool:
            if thread.is_alive():
                return True
    
    def join_thread_pool(self, thread_pool):
        for thread in thread_pool:
            thread.join()
    
    def parse_using_dfs(self, g=None):
        pass

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
                    print(f"Processing node - {i} (Outedges for node {i} {g.edges(i)})")
                    thread = self.spawn_thread_task(i)
                    thread_pool.append(thread)
                    # self.processed_nodes.adscriptd(i)
                    out_edges = g.edges(i)
                    for _, nextnode in out_edges:
                        queue.add(nextnode)
                else:
                    print(f"Dependent nodes were not ready/failed for node {i}, so queuing now")
                    self.queued_nodes.add(i)
                
            self.join_thread_pool(thread_pool)

    def parse_graph_celery(self, g=None):
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
                    print(f"Processing node - {i} (Outedges for node {i} {g.edges(i)})")
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

            
        # print(start_nodes)

if __name__ == "__main__":
    # shit = SomeShit()
    # graph = shit.plot_graph_on_array()
    # nodes = random.randint(5,10)
    # seed = random.randint(1,10)
    # probability = 0.1
    # g = gnp_random_connected_graph(nodes, probability)
    # plt.figure(figsize=(10,6))

    # nx.draw(g, node_color='lightblue', 
    #         with_labels=True, 
    #         node_size=500)
    # plt.show()
    # print(f"Cycles in graph are {list(nx.simple_cycles(g))}")
    # shit.parse_graph_celery()
    # shit.spawn_thread_task(1)
    req = json.loads(open('executor/request_sample2', 'r').read())
    shit = SomeShit(req=req)
    shit.parse_graph_celery()