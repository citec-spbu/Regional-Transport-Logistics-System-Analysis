import unittest
import osmnx as ox
from function1 import create_graph_several_city  # 假设你的函数在这个模块中

class TestCreateGraphSeveralCity(unittest.TestCase):

    def setUp(self):
        # 设置一个测试用的城市图
        self.test_graph = ox.graph_from_place('Piedmont, California, USA', network_type='drive')

    def test_create_graph_several_city_with_valid_inputs(self):
        # 使用默认参数创建子图
        sub_graph = create_graph_several_city(self.test_graph, my_network_type='drive')
        # 检查返回的是一个非空图
        self.assertGreater(len(sub_graph.nodes()), 0, "The created graph should not be empty")

    def test_create_graph_several_city_with_custom_network_type(self):
        # 使用自定义网络类型创建子图
        sub_graph = create_graph_several_city(self.test_graph, my_network_type='walk')
        # 检查返回的是一个非空图
        self.assertGreater(len(sub_graph.nodes()), 0, "The created graph should not be empty when using 'walk' network type")

    def test_create_graph_several_city_with_invalid_graph(self):
        # 尝试使用无效的图结构作为输入
        with self.assertRaises((ValueError, AttributeError)):
            create_graph_several_city("not a graph")

if __name__ == '__main__':
    unittest.main()