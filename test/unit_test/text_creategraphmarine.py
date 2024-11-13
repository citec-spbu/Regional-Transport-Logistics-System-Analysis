import unittest
import pandas as pd
import networkx as nx
from unittest.mock import patch
from function1 import create_graph_marine, create_df_to_graphs, create_my_graphs

class TestCreateGraphMarine(unittest.TestCase):

    def setUp(self):
        # 创建一个简单的初始图并设置 CRS 属性
        self.full_g = nx.Graph()
        self.full_g.add_node(1, pos=(40.7128, -74.0060))  # New York
        self.full_g.add_node(2, pos=(51.5074, -0.1278))   # London
        self.full_g.graph['crs'] = 'epsg:4326'

        # 创建示例 DataFrame
        self.full_df_from = pd.DataFrame({
            'x': [-74.0060],
            'y': [40.7128],
            'kind_of': ['aeroway']
        })

        self.full_df_to = pd.DataFrame({
            'x': [-0.1278],
            'y': [51.5074],
            'kind_of': ['aeroway']
        })

    @patch('function1.marnet_geograph.get_shortest_path')
    def test_create_graph_marine(self, mock_get_shortest_path):
        # 创建虚拟数据
        mock_output = {
            'coordinate_path': [
                (40.7128, -74.0060),
                (45.0, -5.0),
                (51.5074, -0.1278)
            ]
        }
        mock_get_shortest_path.return_value = mock_output

        # 调用函数
        result_graph = create_graph_marine(self.full_g, self.full_df_from, self.full_df_to)

        # 检查输出图的节点数
        initial_node_count = len(self.full_g.nodes())
        new_node_count = len(result_graph.nodes())
        self.assertGreater(new_node_count, initial_node_count, "New nodes should be added to the graph")

        # 检查输出图的边数
        initial_edge_count = len(self.full_g.edges())
        new_edge_count = len(result_graph.edges())
        self.assertGreater(new_edge_count, initial_edge_count, "New edges should be added to the graph")

        # 检查特定边的存在
        expected_nodes = [(40.7128, -74.0060), (45.0, -5.0), (51.5074, -0.1278)]
        for node in expected_nodes:
            self.assertIn(node, result_graph.nodes(), f"Node {node} should be in the result graph")

        # 检查路径上的边是否存在于结果图中
        for k in range(len(expected_nodes) - 1):
            u = expected_nodes[k]
            v = expected_nodes[k + 1]
            self.assertTrue(result_graph.has_edge(u, v), f"Edge between {u} and {v} should be in the result graph")

if __name__ == '__main__':
    unittest.main()