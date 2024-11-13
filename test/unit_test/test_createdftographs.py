import unittest
import pandas as pd
from function1 import create_df_to_graphs
#我们为 full_df_from 和 full_df_to 创建了两个简单的数据框，它们包含了不同类型的机场信息。
# 然后，在 test_create_df_to_graphs 方法中，我们调用了 create_df_to_graphs 函数，并将返回的结果与预期的结果进行了比较。
# 如果结果与预期不符，测试将失败，并显示错误消息。
class TestCreateDfToGraphs(unittest.TestCase):

    def setUp(self):
        # 创建测试用的数据框
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
        # 测试 'A' 类型的数据
        result = create_df_to_graphs('A', self.full_df_from, self.full_df_to)

        expected_result = pd.DataFrame({
            'x': [100.0, 300.0, 105.0, 305.0],
            'y': [10.0, 30.0, 15.0, 35.0]
        })

        # 检查结果是否与预期相符
        self.assertTrue(result.equals(expected_result), "The result does not match the expected output.")


if __name__ == '__main__':
    unittest.main()