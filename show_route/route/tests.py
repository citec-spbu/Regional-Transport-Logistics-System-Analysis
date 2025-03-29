import unittest
from django.test import RequestFactory
from django.urls import reverse
from .views import (
    showmap,
    showroutes,
    create_graph_city,
    create_features_city,
    create_graph_route,
    result,
    result_marine,
    result_aero,
    func_tags,
    create_route_marine,
    create_route_aero,
    create_final_graph,
)
import osmnx as ox
import pandas as pd
import geopandas as gpd
import networkx as nx
from unittest.mock import patch, MagicMock


class TestViews(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_showmap(self):
        request = self.factory.get(reverse('showmap'))
        response = showmap(request)
        self.assertEqual(response.status_code, 200)

    @patch('route.views.create_graph_city')
    @patch('route.views.create_features_city')
    @patch('route.views.create_graph_route')
    @patch('route.views.result')
    @patch('route.views.result_marine')
    @patch('route.views.result_aero')
    def test_showroutes(self, mock_result_aero, mock_result_marine, mock_result, mock_create_graph_route, mock_create_features_city, mock_create_graph_city):
        # Пример координат для тестирования
        lat1, long1, lat2, long2 = '55.75', '37.61', '55.76', '37.62'
        metrics = 'degree'

        # Мокируем возвращаемые значения
        mock_create_graph_city.return_value = (pd.DataFrame(), nx.Graph(), [55.75, 55.76], [37.61, 37.62])
        mock_create_features_city.return_value = pd.DataFrame({'new_nodes': [1, 2]})
        mock_create_graph_route.return_value = pd.DataFrame({'route': [[1, 2]]})
        mock_result.return_value = nx.Graph()
        mock_result_marine.return_value = nx.Graph()
        mock_result_aero.return_value = nx.Graph()

        request = self.factory.get(reverse('showroute', args=[metrics, lat1, long1, lat2, long2]))
        response = showroutes(request, metrics, lat1, long1, lat2, long2)
        self.assertEqual(response.status_code, 200)

    @patch('route.views.ox.features.features_from_bbox')
    @patch('route.views.ox.graph_from_bbox')
    def test_create_graph_city(self, mock_graph_from_bbox, mock_features_from_bbox):
        # Мокируем возвращаемые значения
        mock_features_from_bbox.return_value = pd.DataFrame({
            'element_type': ['node', 'way'],
            'osmid': [123, 456],
            'lat': [55.75, 55.76],
            'lon': [37.61, 37.62]
        })
        mock_graph_from_bbox.return_value = nx.Graph()

        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        full_df, G, lat, lon = create_graph_city(point_y, point_x)
        self.assertIsNotNone(full_df)
        self.assertIsNotNone(G)
        self.assertIsNotNone(lat)
        self.assertIsNotNone(lon)

    @patch('route.views.create_graph_city')
    def test_create_features_city(self, mock_create_graph_city):
        # Мокируем возвращаемые значения
        mock_create_graph_city.return_value = (pd.DataFrame(), nx.Graph(), [55.75, 55.76], [37.61, 37.62])

        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        full_df, G, lat, lon = create_graph_city(point_y, point_x)
        features_df = create_features_city(full_df, G, lat, lon)
        self.assertIsNotNone(features_df)
        self.assertIn('new_nodes', features_df.columns)

    @patch('route.views.create_graph_city')
    @patch('route.views.create_features_city')
    def test_create_graph_route(self, mock_create_features_city, mock_create_graph_city):
        # Мокируем возвращаемые значения
        mock_create_graph_city.return_value = (pd.DataFrame(), nx.Graph(), [55.75, 55.76], [37.61, 37.62])
        mock_create_features_city.return_value = pd.DataFrame({'new_nodes': [1, 2]})

        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        full_df, G, lat, lon = create_graph_city(point_y, point_x)
        features_df = create_features_city(full_df, G, lat, lon)
        route_df = create_graph_route(G, features_df)
        self.assertIsNotNone(route_df)
        self.assertIn('route', route_df.columns)

    @patch('route.views.create_graph_city')
    @patch('route.views.create_features_city')
    @patch('route.views.create_graph_route')
    def test_result(self, mock_create_graph_route, mock_create_features_city, mock_create_graph_city):
        # Мокируем возвращаемые значения
        mock_create_graph_city.return_value = (pd.DataFrame(), nx.Graph(), [55.75, 55.76], [37.61, 37.62])
        mock_create_features_city.return_value = pd.DataFrame({'new_nodes': [1, 2]})
        mock_create_graph_route.return_value = pd.DataFrame({'route': [[1, 2]]})

        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        final_graph = result(point_y, point_x)
        self.assertIsNotNone(final_graph)

    @patch('route.views.create_graph_city')
    @patch('route.views.create_features_city')
    @patch('route.views.create_route_marine')
    def test_result_marine(self, mock_create_route_marine, mock_create_features_city, mock_create_graph_city):
        # Мокируем возвращаемые значения
        mock_create_graph_city.return_value = (pd.DataFrame(), nx.Graph(), [55.75, 55.76], [37.61, 37.62])
        mock_create_features_city.return_value = pd.DataFrame({'new_nodes': [1, 2]})
        mock_create_route_marine.return_value = pd.DataFrame({'route': [[1, 2]]})

        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        final_graph = result_marine(point_y, point_x)
        self.assertIsNotNone(final_graph)

    @patch('route.views.create_graph_city')
    @patch('route.views.create_features_city')
    @patch('route.views.create_route_aero')
    def test_result_aero(self, mock_create_route_aero, mock_create_features_city, mock_create_graph_city):
        # Мокируем возвращаемые значения
        mock_create_graph_city.return_value = (pd.DataFrame(), nx.Graph(), [55.75, 55.76], [37.61, 37.62])
        mock_create_features_city.return_value = pd.DataFrame({'new_nodes': [1, 2]})
        mock_create_route_aero.return_value = pd.DataFrame({'route': [[1, 2]]})

        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        final_graph = result_aero(point_y, point_x)
        self.assertIsNotNone(final_graph)

    @patch('route.views.ox.features.features_from_bbox')
    def test_func_tags(self, mock_features_from_bbox):
        mock_features_from_bbox.return_value = pd.DataFrame({
            'element_type': ['node', 'way'],
            'osmid': [123, 456],
            'lat': [55.75, 55.76],
            'lon': [37.61, 37.62]
        })

        tags = {'industrial': 'port'}
        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        result_df = func_tags(tags, point_y, point_x)

        self.assertIsNotNone(result_df)
        self.assertIn('lat', result_df.columns)
        self.assertIn('lon', result_df.columns)
        self.assertIn('kind_of', result_df.columns)

    @patch('route.views.ox.features.features_from_bbox')
    def test_func_tags_no_data(self, mock_features_from_bbox):
        mock_features_from_bbox.side_effect = ox._errors.InsufficientResponseError

        tags = {'industrial': 'port'}
        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        result_df = func_tags(tags, point_y, point_x)

        self.assertIsNone(result_df)

    @patch('route.views.marnet_geograph.get_shortest_path')
    def test_create_route_marine(self, mock_get_shortest_path):
        mock_get_shortest_path.return_value = {
            'coordinate_path': [(55.75, 37.61), (55.76, 37.62)]
        }

        G = nx.Graph()
        f_df = pd.DataFrame({
            'kind_of': ['industrial'],
            'lat': [55.75],
            'lon': [37.61]
        })

        route_df = create_route_marine(G, f_df)

        self.assertIsNotNone(route_df)
        self.assertIn('route', route_df.columns)

    @patch('route.views.marnet_geograph.get_shortest_path')
    def test_create_route_marine_no_data(self, mock_get_shortest_path):
        mock_get_shortest_path.side_effect = Exception

        G = nx.Graph()
        f_df = pd.DataFrame({
            'kind_of': ['industrial'],
            'lat': [55.75],
            'lon': [37.61]
        })

        route_df = create_route_marine(G, f_df)

        self.assertIsNotNone(route_df)
        self.assertTrue(route_df.empty)

    def test_create_route_aero(self):
        G = nx.Graph()
        G.add_node(1, x=37.61, y=55.75)
        G.add_node(2, x=37.62, y=55.76)

        f_df = pd.DataFrame({
            'kind_of': ['aeroway'],
            'lat': [55.75, 55.76],
            'lon': [37.61, 37.62]
        })

        route_df = create_route_aero(G, f_df)

        self.assertIsNotNone(route_df)
        self.assertIn('route', route_df.columns)

    def test_create_route_aero_no_data(self):
        G = nx.Graph()
        f_df = pd.DataFrame({
            'kind_of': ['aeroway'],
            'lat': [],
            'lon': []
        })

        route_df = create_route_aero(G, f_df)

        self.assertIsNotNone(route_df)
        self.assertTrue(route_df.empty)

    def test_create_final_graph(self):
        G = nx.Graph()
        G.add_node(1, x=37.61, y=55.75)
        G.add_node(2, x=37.62, y=55.76)
        G.add_edge(1, 2)

        route_df = pd.DataFrame({
            'route': [[1, 2]]
        })

        feature_df = pd.DataFrame({
            'new_nodes': [1, 2]
        })

        final_graph = create_final_graph(G, route_df, feature_df)

        self.assertIsNotNone(final_graph)
        self.assertTrue(isinstance(final_graph, nx.MultiDiGraph))

    def test_create_final_graph_no_data(self):
        G = nx.Graph()
        route_df = pd.DataFrame({
            'route': []
        })

        feature_df = pd.DataFrame({
            'new_nodes': []
        })

        final_graph = create_final_graph(G, route_df, feature_df)

        self.assertIsNotNone(final_graph)
        self.assertTrue(isinstance(final_graph, nx.MultiDiGraph))

    @patch('route.views.create_graph_city')
    @patch('route.views.create_features_city')
    @patch('route.views.create_graph_route')
    @patch('route.views.result')
    @patch('route.views.result_marine')
    @patch('route.views.result_aero')
    def test_showroutes(self, mock_result_aero, mock_result_marine, mock_result, mock_create_graph_route,
                        mock_create_features_city, mock_create_graph_city):
        mock_create_graph_city.return_value = (pd.DataFrame(), nx.Graph(), [55.75, 55.76], [37.61, 37.62])
        mock_create_features_city.return_value = pd.DataFrame({'new_nodes': [1, 2]})
        mock_create_graph_route.return_value = pd.DataFrame({'route': [[1, 2]]})
        mock_result.return_value = nx.Graph()
        mock_result_marine.return_value = nx.Graph()
        mock_result_aero.return_value = nx.Graph()

        metrics = 'degree'
        lat1, long1, lat2, long2 = '55.75', '37.61', '55.76', '37.62'

        request = self.factory.get(reverse('showroute', args=[metrics, lat1, long1, lat2, long2]))
        response = showroutes(request, metrics, lat1, long1, lat2, long2)
        self.assertEqual(response.status_code, 200)


class TestAdditionalViews(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('route.views.os.path.exists')
    @patch('route.views.pd.read_csv')
    @patch('route.views.ox.graph_from_gdfs')
    def test_showroutes_with_existing_files(self, mock_graph_from_gdfs, mock_read_csv, mock_exists):
        mock_exists.return_value = True
        mock_read_csv.side_effect = [
            pd.DataFrame({'osmid': [1], 'y': [55.75], 'x': [37.61], 'geometry': ['POINT (37.61 55.75)']}),
            pd.DataFrame({'u': [1], 'v': [2], 'key': [0], 'geometry': ['LINESTRING (37.61 55.75, 37.62 55.76)']})
        ]
        mock_graph_from_gdfs.return_value = nx.Graph()

        request = self.factory.get(reverse('showroute', args=['degree', '55.75', '37.61', '55.76', '37.62']))
        response = showroutes(request, 'degree', '55.75', '37.61', '55.76', '37.62')
        self.assertEqual(response.status_code, 200)

    @patch('route.views.ox.features.features_from_bbox')
    def test_func_tags_with_empty_dataframe(self, mock_features_from_bbox):
        mock_features_from_bbox.return_value = pd.DataFrame()

        tags = {'industrial': 'port'}
        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        result_df = func_tags(tags, point_y, point_x)

        self.assertIsNone(result_df)

    @patch('route.views.ox.graph_from_bbox')
    def test_create_graph_city_with_empty_graph(self, mock_graph_from_bbox):
        mock_graph_from_bbox.return_value = nx.Graph()

        point_y = (55.75, 55.76)
        point_x = (37.61, 37.62)
        full_df, G, lat, lon = create_graph_city(point_y, point_x)

        self.assertTrue(G.number_of_nodes() == 0)

    def test_create_features_city_with_empty_coordinates(self):
        empty_df = pd.DataFrame()
        G = nx.Graph()
        lat = []
        lon = []

        features_df = create_features_city(empty_df, G, lat, lon)

        self.assertTrue(features_df.empty)

    @patch('route.views.ox.distance.nearest_nodes')
    def test_create_features_city_with_invalid_nodes(self, mock_nearest_nodes):
        mock_nearest_nodes.return_value = None

        df = pd.DataFrame({'lat': [55.75], 'lon': [37.61]})
        G = nx.Graph()
        lat = [55.75]
        lon = [37.61]

        features_df = create_features_city(df, G, lat, lon)

        self.assertTrue(features_df['new_nodes'].isnull().all())

    @patch('route.views.nx.shortest_path')
    def test_create_graph_route_with_no_path(self, mock_shortest_path):
        mock_shortest_path.side_effect = nx.NetworkXNoPath

        G = nx.Graph()
        feature_df = pd.DataFrame({'new_nodes': [1, 2]})

        route_df = create_graph_route(G, feature_df)

        self.assertTrue(route_df.empty)

    @patch('route.views.nx.compose_all')
    @patch('route.views.ox.graph_to_gdfs')
    def test_showroutes_with_graph_composition_error(self, mock_graph_to_gdfs, mock_compose_all):
        mock_compose_all.side_effect = nx.NetworkXError
        mock_graph_to_gdfs.return_value = (pd.DataFrame(), pd.DataFrame())

        request = self.factory.get(reverse('showroute', args=['degree', '55.75', '37.61', '55.76', '37.62']))
        with self.assertRaises(nx.NetworkXError):
            showroutes(request, 'degree', '55.75', '37.61', '55.76', '37.62')


if __name__ == '__main__':
    unittest.main()
