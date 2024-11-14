import unittest
from unittest.mock import patch, MagicMock

import networkx as nx
import pandas as pd
from function import create_features_city

#Была вызвана функция create_features_city, и проверено, соответствует ли возвращаемый DataFrame ожидаемому результату.
# Если все в порядке, этот тест должен быть пройден успешно.
#检查了函数返回的 DataFrame 是否符合预期的结果。
class TestCreateFeaturesCity(unittest.TestCase):

    def setUp(self):

        self.features_df = pd.DataFrame({
            'name': ['Port A', 'Airport B'],
            'lat': [40.7128, 51.5074],
            'lon': [-74.0060, -0.1278],
            'geometry': [None, None],
            'nodes': [None, None],
            'kind_of': ['industrial', 'aeroway']
        })


        self.city_graph = nx.Graph()
        self.city_graph.add_node(1, x=-74.0060, y=40.7128)  # 添加与 features_df 中的点相对应的节点
        self.city_graph.add_node(2, x=-0.1278, y=51.5074)

        self.lat = [40.7128, 51.5074]
        self.lon = [-74.0060, -0.1278]

    @patch('osmnx.distance.nearest_nodes')
    def test_create_features_city(self, mock_nearest_nodes):

        mock_nearest_nodes.return_value = [1, 2]
        result_df = create_features_city(self.features_df, self.city_graph, self.lat, self.lon)
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