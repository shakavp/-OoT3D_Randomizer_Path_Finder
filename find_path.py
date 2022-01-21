"""
created on 21/01/2022
@author: Geraldo C. Zampoli
"""

import re
import os

import xml.etree.ElementTree as ET
import networkx as nx

from bidict import bidict


DEBUG = False

class RandoEntrance:
    """
    Class for get the information needed for the digraph from the spoilerlog
    """

    SPOILER_LOG = re.compile(r".*-spoilerlog.xml$")
    ENTRANCE_ENTRY = './/entrance-playthrough/sphere/entrance'

    def __init__(self, log=None):
        if log is None:
            for file in os.listdir():
                if RandoEntrance.SPOILER_LOG.search(file):
                    log = file
                    break
        self.spoiler_log = log
        tree = ET.parse(self.spoiler_log)
        self.root = tree.getroot()
        self.edges = {}
        self.vertex_dict = {}

    def find_vertex(self):
        """
        Gets all the digraph vertex from the spoilerlog
        Retuns a bidirectional dictionary with all the vertex
        """
        vertex_list = []
        for child in self.root.findall(RandoEntrance.ENTRANCE_ENTRY):
            start_aux = child.attrib['name'].split('->')[0].strip()
            finish_aux = child.text.split('from')[0].strip()
            vertex_list.extend([start_aux, finish_aux])
        vertex_list = list(set(vertex_list))

        self.vertex_dict = bidict(dict(enumerate(sorted(vertex_list))))
        return self.vertex_dict

    def find_edges(self):
        """
        Gets all the digraph edges from the spoilerlog
        Returns a dictionary where:
        key = edge
        value = edge name
        """
        for child in self.root.findall(RandoEntrance.ENTRANCE_ENTRY):
            start_aux = child.attrib['name'].split('->')[0].strip()
            path = child.attrib['name']
            finish_aux = child.text.split('from')[0].strip()
            self.edges[(start_aux, finish_aux)] = path
        return self.edges

    def __str__(self):
        all_edges = self.find_edges()
        data = '\n'
        for path, name in all_edges.items():
            data += f'{path[0]} [-> ({name}) ->] {path[1]}\n'
        return data


class DigraphConstructor:
    """
    Digraph of paths construction
    """
    def __init__(self):
        """
        Return a empty digraph
        """
        self.digraph = nx.DiGraph()
        self.edges = {}

    @staticmethod
    def _edge_set(edges):
        """
        Set edges for the digraph
        """
        return list(edges.keys())

    def create_digraph(self, edges):
        """
        Create a digraph with given edges
        """
        self.edges = edges
        edge_list = self._edge_set(edges)
        self.digraph.add_edges_from(edge_list)

    def find_path(self, path_start, path_finish):
        """
        Find shortest path from start to finish
        Returns the complete path
        """
        path = nx.shortest_path(self.digraph, path_start, path_finish)
        final_path = []
        for index, item_p in enumerate(path):
            if index + 1 == len(path):
                break
            final_path.append(item_p)
            final_path.append(self.edges[(path[index], path[index+1])])
        final_path.append(path[-1])
        return final_path

    def __str__(self):
        text = ''
        text += f"{str(self.digraph)}\n"
        text += "Nodes:\n"
        for node in self.digraph.nodes():
            text += f"  {str(node)}\n"
        text += f"Digraph acyclic: {str(nx.is_directed_acyclic_graph(self.digraph))}\n"
        return text


if __name__ == '__main__':
    p = RandoEntrance()
    p.find_vertex()
    p.find_edges()

    d = DigraphConstructor()
    d.create_digraph(p.edges)

    if DEBUG:
        print(p)
        print(d.find_path("KF Link's House", "Market"))

    print("Choose your start and finish point from the list:")
    for vertex in p.vertex_dict.items():
        print(f"{vertex[0]} : {vertex[1]}")
    print("\nUse the number for the selection")
    start = int(input("Starting Point: "))
    finish = int(input("Finish point: "))

    result = d.find_path(p.vertex_dict[start], p.vertex_dict[finish])
    print("Path:")
    for item in result:
        print(f"  {item}")
