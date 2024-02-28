# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMUrbanRailDataDownloader:
#     def __init__(self, geojson_path, output_filename):
#         self.geojson_path = geojson_path
#         self.output_filename = output_filename
#         ox.config(log_console=True, use_cache=True)

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         osm_tags = {'railway': ['subway', 'tram']}
#         gdf_combined = gpd.GeoDataFrame()

#         for rail_type in osm_tags['railway']:
#             gdf = ox.geometries_from_polygon(geometry, tags={'railway': rail_type})
#             gdf = gdf[gdf['geometry'].type.isin(['LineString', 'MultiLineString'])]
#             gdf['fclass'] = rail_type
#             gdf_combined = pd.concat([gdf_combined, gdf], ignore_index=True)

#         for col in gdf_combined.columns:
#             if isinstance(gdf_combined[col].iloc[0], list) or gdf_combined[col].dtype == object:
#                 gdf_combined[col] = gdf_combined[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else str(x))

#         new_columns = {}
#         for col in gdf_combined.columns:
#             new_name = col[:10]
#             if new_name in new_columns.values():
#                 suffix = 1
#                 while f"{new_name[:9]}{suffix}" in new_columns.values():
#                     suffix += 1
#                 new_name = f"{new_name[:9]}{suffix}"
#             new_columns[col] = new_name
#         gdf_combined.rename(columns=new_columns, inplace=True)

#         if not gdf_combined.empty:
#             os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
#             gdf_combined.to_file(self.output_filename, driver='ESRI Shapefile')
#             print(f"Data saved successfully to {self.output_filename}")
#         else:
#             print("No data to save.")

# v2

import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMUrbanRailDataDownloader:
    # Define the output filename as a class attribute
    #output_filename = "/home/evangelos/data/data_sub4/swe_sub4/oop_swe_urban_sub4.shp"

    def __init__(self, geojson_path, country_code):
        self.geojson_path = geojson_path
        ox.config(log_console=True, use_cache=True)
        self.output_filename = f"/home/evangelos/osm-data/data_sub4/{country_code}_tran_rrd_ln_s2_osm_pp_subway.shp"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        osm_tags = {'railway': ['subway', 'tram']}
        gdf_combined = gpd.GeoDataFrame()

        for rail_type in osm_tags['railway']:
            gdf = ox.geometries_from_polygon(geometry, tags={'railway': rail_type})
            gdf = gdf[gdf['geometry'].type.isin(['LineString', 'MultiLineString'])]
            gdf['fclass'] = rail_type
            gdf_combined = pd.concat([gdf_combined, gdf], ignore_index=True)

        for col in gdf_combined.columns:
            if isinstance(gdf_combined[col].iloc[0], list) or gdf_combined[col].dtype == object:
                gdf_combined[col] = gdf_combined[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else str(x))

        new_columns = {}
        for col in gdf_combined.columns:
            new_name = col[:10]
            if new_name in new_columns.values():
                suffix = 1
                while f"{new_name[:9]}{suffix}" in new_columns.values():
                    suffix += 1
                new_name = f"{new_name[:9]}{suffix}"
            new_columns[col] = new_name
        gdf_combined.rename(columns=new_columns, inplace=True)

        if not gdf_combined.empty:
            os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
            gdf_combined.to_file(self.output_filename, driver='ESRI Shapefile')
            print(f"Data saved successfully to {self.output_filename}")
        else:
            print("No data to save.")
