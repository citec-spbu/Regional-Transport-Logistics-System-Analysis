import unittest
import pandas as pd
import osmnx as ox
import networkx as nx


class TestCreateGraphAero(unittest.TestCase):

    def setUp(self):
        # 创建模拟的 full_graph
        self.full_graph = ox.graph_from_place('Piedmont, California, USA', network_type='drive')

        # 创建模拟的 full_df_from 和 full_df_to
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
        from function1 import create_graph_aero  # 假设你的函数在 function1.py 文件中

        # 调用函数
        graph_aero = create_graph_aero(self.full_graph, self.full_df_from, self.full_df_to)

        # 验证返回值是否为 MultiDiGraph 类型
        self.assertIsInstance(graph_aero, nx.MultiDiGraph)

        # 检查节点数量
        expected_node_count = 1  # 根据提供的数据，应该有1个节点
        actual_node_count = len(graph_aero.nodes())
        print(f"Expected node count: {expected_node_count}, Actual node count: {actual_node_count}")
        self.assertEqual(actual_node_count, expected_node_count, "节点数量不匹配")

        # 检查边的数量
        expected_edge_count = 0  # 因为只有一个节点，所以不会有边
        actual_edge_count = len(graph_aero.edges())
        print(f"Expected edge count: {expected_edge_count}, Actual edge count: {actual_edge_count}")
        self.assertEqual(actual_edge_count, expected_edge_count, "边数量不匹配")


if __name__ == '__main__':
    unittest.main()