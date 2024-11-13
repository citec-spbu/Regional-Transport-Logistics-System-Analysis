import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from function1 import create_graph_city
#这个单元测试脚本通过模拟外部依赖和断言函数的返回值，确保create_graph_city函数能够正确地从城市中提取地理特征、创建图对象，并返回正确的纬度和经度列表
class TestCreateGraphCity(unittest.TestCase):

    def setUp(self):
        self.name_city = "北京"
        # 假设数据结构
        self.expected_full_df = pd.DataFrame({
            'name': ['Port1', 'Airport1', 'Railway1', 'Warehouse1'],
            'lat': [39.9042, 40.0618, 39.9295, 39.9151],
            'lon': [116.4074, 116.3192, 116.4601, 116.4042],
            'geometry': [None, None, None, None],  # 这里简化处理
            'nodes': [[], [], [], []],
            'kind_of': ['industrial', 'aeroway', 'landuse', 'building']
        })
        self.expected_G = MagicMock()  # 假设的图对象
        self.expected_lat = [39.9042, 40.0618, 39.9295, 39.9151]
        self.expected_lon = [116.4074, 116.3192, 116.4601, 116.4042]

    @patch('function1.func_tags')
    @patch('function1.ox.graph_from_place')
    def test_create_graph_city(self, mock_graph_from_place, mock_func_tags):
        # 模拟返回值
        mock_func_tags.side_effect = [
            self.expected_full_df.iloc[0:1],
            self.expected_full_df.iloc[1:2],
            self.expected_full_df.iloc[2:3],
            self.expected_full_df.iloc[3:]
        ]
        mock_graph_from_place.return_value = self.expected_G

        # 调用函数
        full_df, G, lat, lon = create_graph_city(self.name_city, my_network_type='all_private',
                                                 my_filter='["highway"~"motorway|trunk"]')

        # 断言
        pd.testing.assert_frame_equal(full_df, self.expected_full_df)
        self.assertEqual(G, self.expected_G)
        self.assertListEqual(lat, self.expected_lat)
        self.assertListEqual(lon, self.expected_lon)


if __name__ == '__main__':
    unittest.main()