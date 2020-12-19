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
from executor.modes.poller import task_poller
import random

class BaseMode():
    def __init__(self, *args, **kwargs):
        self.convergence = 1
        self.processed_nodes = set()
        self.queued_nodes = set()
        self.graph_request = kwargs.get('req')
        self.nnodes = len(self.graph_request)

    def list_nodes(self,):
        return [ i.get('name') for i in self.graph_request]

    def create_networkx_graph(self, save=True, saveto="latestdag.png"):
        g = nx.DiGraph()
        nodes = self.list_nodes()
        g.add_nodes_from(nodes)
        
        for point in self.graph_request:
            pointname = point.get('name')
            downstreams = point.get('downstreams')
            for each_downstream in downstreams:
                edge = (pointname, each_downstream)
                g.add_edge(*edge)
        
        if save:
            nx.draw(g,with_labels=True)
            plt.savefig(saveto)
        
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
        """
            List all the nodes which have incoming edges to them from the request
        """
        downstreams = []
        
        for point in self.graph_request:
            downstreams+=point.get('downstreams', [])
        
        return list(set(downstreams))
    
    def parse_graph(self, g=None):
        tm = TaskManager()
        if g==None:
            g = self.create_networkx_graph()
        
        if list(nx.simple_cycles(g)):
            print("Cycles were found in the workflow. Exiting")
            return

        raise NotImplementedError