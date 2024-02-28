import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMMainRoadDataDownloader:
    # Class attributes for osm road types and required tags
    osm_road_types = ["motorway", "trunk", "primary", "secondary", "tertiary"]
    osm_required_tags = ['name', 'oneway', 'maxspeed', 'bridge', 'tunnel', 'surface']
    

    def __init__(self, geojson_path, countre_code):
        self.geojson_path = geojson_path
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/data_sub2/{countre_code}_tran_rds_ln_s0_osm_pp_roads_filtered.shp"

    def download_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry_type = region_gdf['geometry'].iloc[0].geom_type
        if geometry_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        polygon = region_gdf['geometry'].iloc[0]
        graph = ox.graph_from_polygon(polygon, network_type='drive')
        _, edges = ox.graph_to_gdfs(graph)

        all_roads_gdf = gpd.GeoDataFrame()
        for road_type in self.osm_road_types:
            gdf_filtered = edges[(edges['highway'] == road_type) | (edges['highway'] == f"{road_type}_link")]
            if gdf_filtered.empty:
                continue

            existing_tags = [tag for tag in self.osm_required_tags if tag in gdf_filtered.columns]
            tags = ['geometry'] + existing_tags
            gdf_filtered = gdf_filtered[tags]

            for tag in existing_tags:
                gdf_filtered[tag] = gdf_filtered[tag].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else str(x))

            gdf_filtered['fclass'] = road_type
            all_roads_gdf = pd.concat([all_roads_gdf, gdf_filtered], ignore_index=True)

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
