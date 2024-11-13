import unittest
import pandas as pd
import osmnx as ox
from function1 import create_my_graphs
from networkx import MultiDiGraph

#Тестирование функции `create_my_graphs` на предмет того, может ли она правильно создавать новый графический объект при заданных входных данных,
# а также проверка того, соответствуют ли количество и атрибуты узлов и ребер этого объекта ожиданиям.
class TestCreateMyGraphs(unittest.TestCase):
    def setUp(self):
        # 创建一个简单的图对象
        self.full_graph = ox.graph_from_place('Piedmont, California, USA', network_type='drive')

        # 创建一个包含地理坐标的 DataFrame，只包含一个点
        self.full_df_aero = pd.DataFrame({
            'x': [-122.2719],
            'y': [37.8255]
        })
    def test_create_my_graphs(self):
        # 调用函数
        result_graph = create_my_graphs(self.full_graph, self.full_df_aero)
        # 验证结果
        self.assertIsInstance(result_graph, MultiDiGraph, "Result is not a MultiDiGraph")
        # 检查节点数量
        expected_node_count = len(self.full_df_aero)
        self.assertEqual(len(result_graph.nodes), expected_node_count, "Incorrect number of nodes in the result graph")
        # 检查边的数量
        expected_edge_count = len(self.full_df_aero) - 1
        self.assertEqual(len(result_graph.edges), expected_edge_count, "Incorrect number of edges in the result graph")
        # 检查节点属性
        for node_id in result_graph.nodes:
            node_data = result_graph.nodes[node_id]
            self.assertIn('x', node_data, "Node missing 'x' attribute")
            self.assertIn('y', node_data, "Node missing 'y' attribute")
        # 检查边属性
        for u, v, key in result_graph.edges:
            edge_data = result_graph.edges[u, v, key]
            self.assertIn('u', edge_data, "Edge missing 'u' attribute")
            self.assertIn('v', edge_data, "Edge missing 'v' attribute")
            self.assertIn('key', edge_data, "Edge missing 'key' attribute")

if __name__ == '__main__':
    unittest.main()