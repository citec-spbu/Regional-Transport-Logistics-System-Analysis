import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from function1 import create_graph_city
#Проверить, правильно ли функция `create_graph_city` извлекает географические характеристики из города,
# создает объект графа и возвращает правильные списки широты и долготы.
class TestCreateGraphCity(unittest.TestCase):

    def setUp(self):
        self.name_city = "北京"

        self.expected_full_df = pd.DataFrame({
            'name': ['Port1', 'Airport1', 'Railway1', 'Warehouse1'],
            'lat': [39.9042, 40.0618, 39.9295, 39.9151],
            'lon': [116.4074, 116.3192, 116.4601, 116.4042],
            'geometry': [None, None, None, None],
            'nodes': [[], [], [], []],
            'kind_of': ['industrial', 'aeroway', 'landuse', 'building']
        })
        self.expected_G = MagicMock()
        self.expected_lat = [39.9042, 40.0618, 39.9295, 39.9151]
        self.expected_lon = [116.4074, 116.3192, 116.4601, 116.4042]

    @patch('function1.func_tags')
    @patch('function1.ox.graph_from_place')
    def test_create_graph_city(self, mock_graph_from_place, mock_func_tags):

        mock_func_tags.side_effect = [
            self.expected_full_df.iloc[0:1],
            self.expected_full_df.iloc[1:2],
            self.expected_full_df.iloc[2:3],
            self.expected_full_df.iloc[3:]
        ]
        mock_graph_from_place.return_value = self.expected_G

        full_df, G, lat, lon = create_graph_city(self.name_city, my_network_type='all_private',
                                                 my_filter='["highway"~"motorway|trunk"]')

        pd.testing.assert_frame_equal(full_df, self.expected_full_df)
        self.assertEqual(G, self.expected_G)
        self.assertListEqual(lat, self.expected_lat)
        self.assertListEqual(lon, self.expected_lon)


if __name__ == '__main__':
    unittest.main()