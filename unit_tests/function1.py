import osmnx as ox
import pandas as pd
import geopandas as gd
import networkx as nx
from scgraph.geographs.marnet import marnet_geograph

tags_port = {'industrial': 'port'}
tags_aeroway = {'aeroway': ['aerodrome', 'heliport', 'airstrip']}
tags_landuse = {'landuse': 'railway'}
tags_build = {'building': 'warehouse', 'amenity': 'mailroom'}

def func_tags(tags, city):
    try:
        gdf = ox.features_from_place(city, tags)
    except ox._errors.InsufficientResponseError:
        return None
    gdf = gdf[['name', 'geometry', 'nodes']]
    gdf = gdf.dropna().reset_index()
    gdf['n_osmid'] = gdf['element_type'].apply(lambda x: x[0]) + gdf['osmid'].astype(str)
    ex = [gdf['n_osmid'].apply(lambda x: ox.geocode_to_gdf(x, by_osmid=True)[['lat', 'lon']]).iloc[:].values[x] for x in range(len(gdf))]
    dfs = pd.concat(ex, axis=0).reset_index(drop=True)
    gdf = gdf.merge(dfs, on=dfs.index)
    gdf = gdf.drop('key_0', axis=1)
    gdf = gdf[['name', 'lat', 'lon', 'geometry', 'nodes']]
    gdf['kind_of'] = list(tags.keys())[0]
    return gdf


def create_graph_city(name_city, my_network_type=None, my_filter=None):
    full_df = pd.concat([func_tags(tags_port, name_city),
                         func_tags(tags_aeroway, name_city),
                         func_tags(tags_landuse, name_city),
                         func_tags(tags_build, name_city)], ignore_index=True)
    G = ox.graph_from_place(name_city, retain_all=True, simplify=True, network_type=my_network_type,
                            custom_filter=my_filter)

    lat = list(full_df['lat'].values)
    lon = list(full_df['lon'].values)

    return full_df, G, lat, lon


''' Формирование датафрейма фич '''


def create_features_city(features_df, city_graph, lat, lon):
    features_df['new_nodes'] = ox.distance.nearest_nodes(city_graph, lon, lat)
    return features_df


''' Построение bbox '''


def create_graph_several_city(full_graph, my_network_type=None, my_filter=None):
    gdf_nodes, gdf_relationships = ox.graph_to_gdfs(full_graph)
    north, south, east, west = gdf_nodes[['y']].max(), gdf_nodes[['y']].min(), gdf_nodes[['x']].min(), gdf_nodes[
        ['x']].max()
    full_graph_from_bbox = ox.graph_from_bbox(bbox=(north, south, east, west), simplify=True, retain_all=True,
                                              network_type=my_network_type, custom_filter=my_filter)
    return full_graph_from_bbox


''' Построение датафрейма долгот и широт для морей и аэро '''
def create_df_to_graphs(kind_of, full_df_from, full_df_to):
    list_lat_aero_from = full_df_from[full_df_from['kind_of'] == kind_of].lat.to_list()
    list_lon_aero_from = full_df_from[full_df_from['kind_of'] == kind_of].lon.to_list()
    list_lat_aero_to = full_df_to[full_df_to['kind_of'] == kind_of].lat.to_list()
    list_lon_aero_to = full_df_to[full_df_to['kind_of'] == kind_of].lon.to_list()
    full_list_lat_aero = list_lat_aero_from + list_lat_aero_to
    full_list_lon_aero = list_lon_aero_from + list_lon_aero_to
    full_df_aero = pd.DataFrame({'x': full_list_lon_aero, 'y': full_list_lat_aero})
    return full_df_aero


''' Построение графа по точкам '''


def create_my_graphs(full_graph, full_df_aero):
    full_df_aero['new_nodes'] = ox.distance.nearest_nodes(full_graph, full_df_aero.x, full_df_aero.y)
    full_df_aero['osmid'] = full_df_aero['new_nodes']
    full_df_aero = full_df_aero.set_index('osmid')

    edge_dict = {'u': full_df_aero.new_nodes[:-1].values, 'v': full_df_aero.new_nodes[1:].values, 'key': 0}
    edge_gdf = gd.GeoDataFrame(edge_dict, crs=None)
    edge_gdf = edge_gdf.set_index(['u', 'v', 'key'])

    graph_attrs = {"crs": "WGS84"}
    multi_digraph_aero = ox.convert.graph_from_gdfs(
        full_df_aero, edge_gdf, graph_attrs=graph_attrs)

    return multi_digraph_aero


''' Построение воздушного графа '''


def create_graph_aero(full_graph, full_df_from, full_df_to):
    f = create_df_to_graphs('aeroway', full_df_from, full_df_to)
    multi_digraph_aero = create_my_graphs(full_graph, f)
    return multi_digraph_aero


''' Построение морского графа '''


def create_graph_marine(full_g, full_df_from, full_df_to):
    df_marine = create_df_to_graphs('aeroway', full_df_from, full_df_to)
    full_df_marine_x = list(df_marine.x)
    full_df_marine_y = list(df_marine.y)

    for i in range(len(full_df_marine_x)):
        for j in range(i + 1, len(full_df_marine_y)):
            output = (marnet_geograph.get_shortest_path(
                origin_node={"latitude": full_df_marine_y[i], "longitude": full_df_marine_x[i]},
                destination_node={"latitude": full_df_marine_y[j], "longitude": full_df_marine_x[j]}
            ))
            list_lat_marine = [output['coordinate_path'][i][0] for i in range(len(output['coordinate_path']))]
            list_lon_marine = [output['coordinate_path'][i][1] for i in range(len(output['coordinate_path']))]
            full_df_marine = pd.DataFrame({'x': list_lon_marine, 'y': list_lat_marine})

            multi_digraph_marine = create_my_graphs(full_g, full_df_marine)

            full_g = nx.compose_all([full_g, multi_digraph_marine])

    return full_g