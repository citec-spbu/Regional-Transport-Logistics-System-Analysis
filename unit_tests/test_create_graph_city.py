import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import osmnx as ox
from function import create_graph_city, func_tags
#Вызовите функцию create_graph_city и проверьте, соответствуют ли возвращенные значения full_df, G, lat и lon ожидаемым.
class TestCreateGraphCity(unittest.TestCase):
    @patch('function.func_tags')
    @patch('osmnx.graph_from_place')
    def test_create_graph_city_with_valid_data(self, mock_graph_from_place, mock_func_tags):
        # 模拟 func_tags 返回的数据
        mock_func_tags.side_effect = [
            pd.DataFrame({'lat': [51.5074], 'lon': [-0.1278], 'kind_of': ['industrial']}),
            pd.DataFrame({'lat': [40.7128], 'lon': [-74.0060], 'kind_of': ['aeroway']}),
            pd.DataFrame({'lat': [48.8566], 'lon': [2.3522], 'kind_of': ['landuse']}),
            pd.DataFrame({'lat': [34.0522], 'lon': [-118.2437], 'kind_of': ['building']})
        ]
        # 模拟 graph_from_place 返回的图
        mock_graph = MagicMock()
        mock_graph_from_place.return_value = mock_graph
        # 测试输入
        name_city = "London"
        my_network_type = "drive"
        my_filter = "['highway'~'primary|secondary']"

        full_df, G, lat, lon = create_graph_city(name_city, my_network_type, my_filter)
        # 预期结果
        expected_full_df = pd.DataFrame({
            'lat': [51.5074, 40.7128, 48.8566, 34.0522],
            'lon': [-0.1278, -74.0060, 2.3522, -118.2437],
            'kind_of': ['industrial', 'aeroway', 'landuse', 'building']
        })
        expected_lat = [51.5074, 40.7128, 48.8566, 34.0522]
        expected_lon = [-0.1278, -74.0060, 2.3522, -118.2437]
        # 断言
        pd.testing.assert_frame_equal(full_df, expected_full_df)
        self.assertEqual(G, mock_graph)
        self.assertEqual(lat, expected_lat)
        self.assertEqual(lon, expected_lon)

if __name__ == '__main__':
    unittest.main()
    #调用 create_graph_city 函数并验证返回的 full_df、G、lat 和 lon 是否符合预期。