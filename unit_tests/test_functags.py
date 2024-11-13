import unittest
from unittest.mock import patch
import pandas as pd
import osmnx as ox
from function1 import func_tags

#Тестирование функции `func_tags` на предмет того, соответствует ли её поведение ожиданиям при различных условиях ввода.
class TestFuncTags(unittest.TestCase):

    def test_normal_case(self):
        tags = {'amenity': 'restaurant'}
        city = 'New York, USA'
        result = func_tags(tags, city)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertIn('kind_of', result.columns)
        self.assertEqual(result['kind_of'][0], 'amenity')

    def test_no_data_found(self):
        tags = {'amenity': 'nonexistent'}
        city = 'New York, USA'
        result = func_tags(tags, city)
        self.assertIsNone(result)

    def test_invalid_city(self):
        tags = {'amenity': 'restaurant'}
        city = 'Nonexistent City, USA'
        result = func_tags(tags, city)
        self.assertIsNone(result)  # 或者根据实际情况调整预期结果

    @patch('osmnx.features_from_place')
    def test_exception_handling(self, mock_features_from_place):
        # 模拟 features_from_place 方法抛出 InsufficientResponseError
        mock_features_from_place.side_effect = ox._errors.InsufficientResponseError

        tags = {'amenity': 'restaurant'}
        city = 'New York, USA'
        result = func_tags(tags, city)

        # 验证 func_tags 函数是否正确处理了异常并返回 None
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()