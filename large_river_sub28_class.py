# import os
# import osmnx as ox
# import geopandas as gpd

# class OSMLargeRiverDataDownloader:
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_tags = {'water': 'river'}
#         ox.config(log_console=True, use_cache=True)
#         self.output_filename = "/home/evangelos/data/data_subXX/swe_subXX/ISO_phys_riv_py_s3_osm_pp_rivers.shp"

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
#         gdf_polygons = gdf[gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])]

#         if self.crs_project:
#             gdf_polygons = gdf_polygons.to_crs(epsg=self.crs_project)
#         gdf_polygons = gdf_polygons.to_crs(epsg=self.crs_global)

#         gdf_polygons = self.process_list_fields(gdf_polygons)
#         gdf_polygons = self.ensure_unique_column_names(gdf_polygons)

#         self.save_data(gdf_polygons)

#     def process_list_fields(self, gdf):
#         for col in gdf.columns:
#             if isinstance(gdf[col].iloc[0], list):
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if x else '')
#         return gdf

#     def ensure_unique_column_names(self, gdf):
#         unique_columns = {}
#         for col in gdf.columns:
#             new_col = col[:10]
#             counter = 1
#             while new_col in unique_columns.values():
#                 new_col = f"{new_col[:9]}{counter}"
#                 counter += 1
#             unique_columns[col] = new_col
#         gdf.rename(columns=unique_columns, inplace=True)
#         return gdf

#     def save_data(self, gdf):
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
#         try:
#             gdf.to_file(self.output_filename, driver='ESRI Shapefile')
#         except Exception as e:
#             print(f"An error occurred while saving the GeoDataFrame: {e}")
#

import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMLargeRiverDataDownloader:
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.osm_tags = {'water': 'river'}
        ox.config(log_console=True, use_cache=True)
        self.output_filename = f"/home/evangelos/osm-data/data_sub28/{country_code}_phys_riv_py_s3_osm_pp_rivers.shp"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
        gdf = gdf[gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])]
        gdf_projected = gdf.to_crs(epsg=self.crs_project)
        gdf_projected = gdf_projected.to_crs(epsg=self.crs_global)

        gdf_projected = self.process_list_fields(gdf_projected)
        gdf_projected = self.ensure_unique_column_names(gdf_projected)

        self.save_data(gdf_projected)

    def process_list_fields(self, gdf):
        for col in gdf.columns:
            if gdf[col].dtype == object and gdf[col].apply(lambda x: isinstance(x, list)).any():
                gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
        return gdf

    def ensure_unique_column_names(self, gdf):
        unique_columns = {}
        for col in gdf.columns:
            col_truncated = col[:10]
            counter = 1
            while col_truncated in unique_columns.values():
                col_truncated = f"{col[:9]}{counter}"
                counter += 1
            unique_columns[col] = col_truncated
        gdf.rename(columns=unique_columns, inplace=True)
        return gdf

    def save_data(self, gdf):
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")