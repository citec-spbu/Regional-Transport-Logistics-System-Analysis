import unittest
import osmnx as ox
import networkx as nx
import pandas as pd
from function import create_graph_city,create_features_city,create_graph_route,create_final_graph
# 假设 result 函数已经定义好了
def result(name_city):
    graph_city = create_graph_city(name_city, my_network_type='drive')
    feature_df = create_features_city(*graph_city)
    ox.distance.add_edge_lengths(graph_city[1], edges=None)
    route_df = create_graph_route(graph_city[1], feature_df)
    final_graph_1_drive = create_final_graph(graph_city[1], route_df, feature_df)
    return final_graph_1_drive

class TestResultFunction(unittest.TestCase):

    def test_empty_city_name(self):
        with self.assertRaises(ValueError):
            result("")

    def test_existing_city_tallinn(self):
        # 使用塔林（Tallinn）作为测试城市
        city_name = "Tallinn, Estonia"
        graph = result(city_name)
        self.assertIsInstance(graph, nx.classes.multidigraph.MultiDiGraph)
        self.assertGreater(len(graph.nodes), 0)
        self.assertGreater(len(graph.edges), 0)

    def test_existing_city_riga(self):
        # 使用里加（Riga）作为测试城市
        city_name = "Riga, Latvia"
        graph = result(city_name)
        self.assertIsInstance(graph, nx.classes.multidigraph.MultiDiGraph)
        self.assertGreater(len(graph.nodes), 0)
        self.assertGreater(len(graph.edges), 0)

    def test_node_and_edge_counts_tallinn(self):
        # 使用塔林（Tallinn）作为测试城市
        city_name = "Tallinn, Estonia"
        graph = result(city_name)
        self.assertGreater(len(graph.nodes), 0)
        self.assertGreater(len(graph.edges), 0)
        # 检查节点和边的数量是否合理
        self.assertLess(len(graph.nodes), 10000)  # 这个值可以根据实际情况调整
        self.assertLess(len(graph.edges), 20000)  # 这个值可以根据实际情况调整

    def test_node_and_edge_counts_riga(self):
        # 使用里加（Riga）作为测试城市
        city_name = "Riga, Latvia"
        graph = result(city_name)
        self.assertGreater(len(graph.nodes), 0)
        self.assertGreater(len(graph.edges), 0)
        # 检查节点和边的数量是否合理
        self.assertLess(len(graph.nodes), 10000)  # 这个值可以根据实际情况调整
        self.assertLess(len(graph.edges), 20000)  # 这个值可以根据实际情况调整

if __name__ == '__main__':
    unittest.main()