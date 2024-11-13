import unittest
import pandas as pd
from function1 import create_df_to_graphs
#Мы создали два простых фрейма данных, full_df_from и full_df_to, которые содержат информацию о разных типах аэропортов.
#Затем, в методе test_create_df_to_graphs, мы вызвали функцию create_df_to_graphs и сравнили возвращенный результат с ожидаемым результатом.
#Если результат не соответствует ожидаемому, тест будет завершен неудачно, и будет отображено сообщение об ошибке.
class TestCreateDfToGraphs(unittest.TestCase):

    def setUp(self):

        self.full_df_from = pd.DataFrame({
            'kind_of': ['A', 'B', 'A', 'C'],
            'lat': [10.0, 20.0, 30.0, 40.0],
            'lon': [100.0, 200.0, 300.0, 400.0]
        })

        self.full_df_to = pd.DataFrame({
            'kind_of': ['A', 'B', 'A', 'C'],
            'lat': [15.0, 25.0, 35.0, 45.0],
            'lon': [105.0, 205.0, 305.0, 405.0]
        })

    def test_create_df_to_graphs(self):

        result = create_df_to_graphs('A', self.full_df_from, self.full_df_to)

        expected_result = pd.DataFrame({
            'x': [100.0, 300.0, 105.0, 305.0],
            'y': [10.0, 30.0, 15.0, 35.0]
        })

        self.assertTrue(result.equals(expected_result), "The result does not match the expected output.")


if __name__ == '__main__':
    unittest.main()