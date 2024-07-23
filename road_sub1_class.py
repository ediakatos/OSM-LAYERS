import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

class OSMRoadDataDownloader:
    osm_road_values = "motorway,trunk,primary,secondary,tertiary,unclassified,residential,motorway_link,trunk_link,primary_link,secondary_link,tertiary_link,lining_street,service,track,road"
    osm_required_tags = ['name', 'oneway', 'maxspeed', 'bridge', 'tunnel', 'surface']
    #output_filename = f"/home/evangelos/data/data_sub1/swe_sub1/{country_code}_roads_full.shp"

    def __init__(self, geojson_path, country_code):
        self.geojson_path = geojson_path
        self.country_code = country_code
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/data_sub1/{country_code}_tran_rds_ln_s0_osm_pp_roads.shp"

    def download_and_process_data(self):
        gdf = gpd.read_file(self.geojson_path)
        geometry_type = gdf['geometry'].iloc[0].geom_type
        if geometry_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")
        
        polygon = gdf['geometry'].iloc[0]
        graph = ox.graph_from_polygon(polygon, network_type='drive')
        _, gdf_edges = ox.graph_to_gdfs(graph)

        all_roads_gdf = gpd.GeoDataFrame()
        for road_type in self.osm_road_values.split(','):
            gdf_filtered = gdf_edges[gdf_edges['highway'].apply(lambda x: road_type in x if isinstance(x, list) else road_type == x)]
            tags = ['geometry'] + [tag for tag in self.osm_required_tags if tag in gdf_edges.columns]
            gdf_filtered = gdf_filtered[tags]

            for column in gdf_filtered.columns:
                if column != 'geometry' and gdf_filtered[column].apply(type).eq(list).any():
                    gdf_filtered[column] = gdf_filtered[column].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else str(x))

            gdf_filtered['fclass'] = road_type
            all_roads_gdf = gpd.GeoDataFrame(pd.concat([all_roads_gdf, gdf_filtered], ignore_index=True))

        new_columns = {}
        for col in all_roads_gdf.columns:
            new_name = col[:10]
            if new_name in new_columns.values():
                suffix = 1
                while f"{new_name[:9]}{suffix}" in new_columns.values():
                    suffix += 1
                new_name = f"{new_name[:9]}{suffix}"
            new_columns[col] = new_name
        all_roads_gdf.rename(columns=new_columns, inplace=True)

        if not all_roads_gdf.empty:
            all_roads_gdf.to_file(self.output_filename, driver='ESRI Shapefile')
            print(f"Data saved successfully to {self.output_filename}")
        else:
            print("No data to save.")
