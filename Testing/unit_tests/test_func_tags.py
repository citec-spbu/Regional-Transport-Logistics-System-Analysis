import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import osmnx as ox
from function import func_tags

#test_func_tags_with_valid_data тестирует, правильно ли функция обрабатывает входные данные при получении корректных данных и возвращает ожидаемый результат.

#test_func_tags_with_insufficient_response_error тестирует, что функция func_tags должна возвращать None,
# когда метод features_from_place выбрасывает исключение InsufficientResponseError.
class TestFuncTags(unittest.TestCase):
    @patch('osmnx.features_from_place')
    @patch('osmnx.geocode_to_gdf')
    def test_func_tags_with_valid_data(self, mock_geocode_to_gdf, mock_features_from_place):
        mock_features_from_place.return_value = pd.DataFrame({
            'element_type': ['node', 'way'],
            'osmid': [123, 456],
            'index': [0, 1]
        })
        mock_geocode_to_gdf.side_effect = [
            pd.DataFrame({'lat': [51.5074], 'lon': [-0.1278]}),  # 第一次调用
            pd.DataFrame({'lat': [40.7128], 'lon': [-74.0060]})  # 第二次调用
        ]
        # 测试输入
        tags = {'industrial': 'port'}
        city = "London"

        result = func_tags(tags, city)
        # 预期结果
        expected_result = pd.DataFrame({
            'lat': [51.5074, 40.7128],
            'lon': [-0.1278, -74.0060],
            'kind_of': ['industrial', 'industrial']
        }).reset_index(drop=True)
        pd.testing.assert_frame_equal(result, expected_result)

    @patch('osmnx.features_from_place')
    def test_func_tags_with_insufficient_response_error(self, mock_features_from_place):
        # 设置模拟异常
        mock_features_from_place.side_effect = ox._errors.InsufficientResponseError
        # 测试输入
        tags = {'industrial': 'port'}
        city = "InvalidCityName"

        result = func_tags(tags, city)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
    #est_func_tags_with_valid_data 测试当接收到有效数据时，是否能够正确处理这些数据并返回预期的结果。
#func_tags_with_insufficient_response_error 测试
# 当 features_from_place 抛出 InsufficientResponseError 异常时，func_tags 函数应该返回 None。