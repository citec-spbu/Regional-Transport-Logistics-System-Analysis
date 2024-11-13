import unittest
from unittest.mock import patch, MagicMock

import networkx as nx
import pandas as pd
from function1 import create_features_city

#调用了 create_features_city 函数，并检查了返回的 DataFrame 是否与预期的结果相匹配。如果一切正常，这个测试应该通过。
# 如果有任何错误，比如函数没有正确地添加 new_nodes 列，或者列中的值不正确，测试将会失败，从而帮助我们定位问题
class TestCreateFeaturesCity(unittest.TestCase):

    def setUp(self):
        # 创建一个示例的 DataFrame
        self.features_df = pd.DataFrame({
            'name': ['Port A', 'Airport B'],
            'lat': [40.7128, 51.5074],
            'lon': [-74.0060, -0.1278],
            'geometry': [None, None],  # 这里可以填充实际的几何数据
            'nodes': [None, None],
            'kind_of': ['industrial', 'aeroway']
        })

        # 创建一个模拟的 NetworkX 图
        self.city_graph = nx.Graph()
        self.city_graph.add_node(1, x=-74.0060, y=40.7128)  # 添加与 features_df 中的点相对应的节点
        self.city_graph.add_node(2, x=-0.1278, y=51.5074)

        # 示例的经纬度列表
        self.lat = [40.7128, 51.5074]
        self.lon = [-74.0060, -0.1278]

    @patch('osmnx.distance.nearest_nodes')
    def test_create_features_city(self, mock_nearest_nodes):
        # 定义 mock 的行为
        mock_nearest_nodes.return_value = [1, 2]

        # 调用要测试的函数
        result_df = create_features_city(self.features_df, self.city_graph, self.lat, self.lon)

        # 验证结果
        expected_result = pd.DataFrame({
            'name': ['Port A', 'Airport B'],
            'lat': [40.7128, 51.5074],
            'lon': [-74.0060, -0.1278],
            'geometry': [None, None],
            'nodes': [None, None],
            'kind_of': ['industrial', 'aeroway'],
            'new_nodes': [1, 2]
        })

        pd.testing.assert_frame_equal(result_df, expected_result)


if __name__ == '__main__':
    unittest.main()