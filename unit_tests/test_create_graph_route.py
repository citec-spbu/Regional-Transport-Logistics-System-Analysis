import networkx as nx
import pandas as pd
import pytest

# 导入待测试的函数
from function import create_graph_route

# 创建一个测试用例类
class TestCreateGraphRoute:
    def test_create_graph_route_with_no_paths(self):
        # 创建一个空的图
        G = nx.Graph()
        # 创建一个空的DataFrame
        df = pd.DataFrame({'new_nodes': []})
        # 调用待测试的函数
        result = create_graph_route(G, df)
        # 验证结果是一个空的DataFrame
        assert result.empty

    def test_create_graph_route_with_paths(self):
        # 创建一个包含节点和边的图
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)
        G.add_edge(3, 4)
        # 创建一个包含节点信息的DataFrame
        df = pd.DataFrame({'new_nodes': [1, 3]})
        # 调用待测试的函数
        result = create_graph_route(G, df)
        # 验证结果包含一条路径
        assert len(result) == 1
        # 验证返回的路径是正确的
        expected_path = [1, 2, 3]
        assert result['route'].iloc[0] == expected_path

# 如果直接运行这个脚本，则执行测试
if __name__ == "__main__":
    pytest.main()
