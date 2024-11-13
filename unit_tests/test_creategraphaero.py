import unittest
import pandas as pd
import osmnx as ox
import networkx as nx
from function1 import create_graph_aero
#Проверить, может ли `create_graph_aero` правильно создавать граф с определенными узлами и ребрами на основе входных данных.
class TestCreateGraphAero(unittest.TestCase):
    def setUp(self):

        self.full_graph = ox.graph_from_place('Piedmont, California, USA', network_type='drive')

        data_from = {
            'kind_of': ['aeroway'],
            'lat': [37.8563],
            'lon': [-122.2912]
        }
        data_to = {
            'kind_of': [],
            'lat': [],
            'lon': []
        }
        self.full_df_from = pd.DataFrame(data_from)
        self.full_df_to = pd.DataFrame(data_to)

    def test_create_graph_aero(self):

        graph_aero = create_graph_aero(self.full_graph, self.full_df_from, self.full_df_to)

        self.assertIsInstance(graph_aero, nx.MultiDiGraph)

        expected_node_count = 1
        actual_node_count = len(graph_aero.nodes())
        print(f"Expected node count: {expected_node_count}, Actual node count: {actual_node_count}")
        self.assertEqual(actual_node_count, expected_node_count, "Not matched node count")

        expected_edge_count = 0
        actual_edge_count = len(graph_aero.edges())
        print(f"Expected edge count: {expected_edge_count}, Actual edge count: {actual_edge_count}")
        self.assertEqual(actual_edge_count, expected_edge_count, "Not matched edge count")


if __name__ == '__main__':
    unittest.main()