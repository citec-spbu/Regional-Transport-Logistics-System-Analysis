import pandas as pd
from shapely.geometry import LineString, MultiLineString
import unittest
from function import create_gdf_graph
# 示例节点数据
nodes_data = {
    'new_nodes': [1, 2, 3]
}
nn = pd.DataFrame(nodes_data)

# 示例边数据
edges_data = {
    'geometry': [
        [LineString([(0, 0), (1, 1)]), LineString([(1, 1), (2, 2)])],
        [LineString([(2, 2), (3, 3)])],
        [LineString([(3, 3), (4, 4)])],
        []  # 添加一个空的列表以匹配索引长度
    ]
}
index = pd.MultiIndex.from_tuples([(0, 0), (0, 1), (1, 0), (2, 0)], names=['u', 'v'])
ee = pd.DataFrame(edges_data, index=index)

class TestCreateGDFGraph(unittest.TestCase):

    def test_create_gdf_graph_empty_input(self):
        nn = pd.DataFrame({'new_nodes': []})
        ee = pd.DataFrame({'geometry': []}, index=pd.MultiIndex.from_tuples([], names=['u', 'v']))
        result = create_gdf_graph(nn, ee)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()