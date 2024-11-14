import pytest
import networkx as nx
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

# 导入待测试的函数
from function import create_final_graph

# 创建测试用的模拟数据
def create_mock_data():
    # 创建一个简单的arb_graph
    arb_graph = nx.DiGraph()
    arb_graph.add_node(1, x=10.0, y=20.0)
    arb_graph.add_node(2, x=15.0, y=25.0)
    arb_graph.add_edge(1, 2, key=0)

    # 创建route_df
    route_df = pd.DataFrame({
        'route': [[1, 2]]
    })

    # 创建feature_df
    feature_df = pd.DataFrame({
        'new_nodes': [1, 2]
    })

    return arb_graph, route_df, feature_df

# 定义测试函数
def test_create_final_graph():
    # 创建模拟数据
    arb_graph, route_df, feature_df = create_mock_data()

    # 调用待测试的函数
    final_graph = create_final_graph(arb_graph, route_df, feature_df)

    # 进行断言测试
    assert isinstance(final_graph, nx.DiGraph), "The output should be a networkx Directed Graph"
    assert len(final_graph.nodes) == 2, "There should be two nodes in the final graph"
    assert len(final_graph.edges) == 1, "There should be one edge in the final graph"
    assert final_graph.nodes[1]['x'] == 10.0 and final_graph.nodes[1]['y'] == 20.0, "Node coordinates are incorrect"
    assert final_graph.has_edge(1, 2), "The edge between nodes 1 and 2 should exist"

# 如果需要，可以添加更多的测试用例来覆盖不同的场景

# 运行测试
if __name__ == "__main__":
    pytest.main([__file__])
