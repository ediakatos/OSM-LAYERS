# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPowerPlantDataDownloader:
#     # Class attribute for the output filename with the specified naming convention
#     output_filename = "/home/evangelos/data/data_sub24/swe_sub24/ISO_util_pst_pt_s2_osm_pp_powerstation.shp"
    
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         ox.config(log_console=True, use_cache=True)

#     def download_and_process_data(self):
#         # Load the region of interest geometry
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         # Ensure the geometry is appropriate
#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download OSM power plant data
#         tags = {'power': 'plant'}
#         gdf = ox.geometries_from_polygon(geometry, tags=tags)

#         # Reproject geometries for accurate geometry calculation
#         gdf_projected = gdf.to_crs(epsg=self.crs_project)
#         gdf_projected = gdf_projected.to_crs(epsg=self.crs_global)

#         # Ensure all specified attribute fields are included in the GeoDataFrame
#         for attribute in ['name', 'operator', 'source']:
#             if attribute not in gdf_projected.columns:
#                 gdf_projected[attribute] = pd.NA

#         # Handle list-type fields before saving
#         gdf_projected = self.process_list_fields(gdf_projected)

#         # Ensure unique column names
#         gdf_projected = self.ensure_unique_column_names(gdf_projected)

#         # Save the data to a Shapefile
#         self.save_data(gdf_projected)

#     def process_list_fields(self, gdf):
#         # Handle list-type fields
#         for col in gdf.columns:
#             if pd.api.types.is_object_dtype(gdf[col]) and gdf[col].apply(lambda x: isinstance(x, list)).any():
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf

#     def ensure_unique_column_names(self, gdf):
#         # Ensure that column names are unique after truncation
#         unique_columns = {}
#         for col in gdf.columns:
#             col_truncated = col[:10]
#             counter = 1
#             while col_truncated in unique_columns.values():
#                 col_truncated = f"{col[:9]}{counter}"
#                 counter += 1
#             unique_columns[col] = col_truncated
#         gdf.rename(columns=unique_columns, inplace=True)
#         return gdf

#     def save_data(self, gdf):
#         # Make directories if they don't exist
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

#         # Attempt to save the GeoDataFrame
#         try:
#             gdf.to_file(self.output_filename, driver='ESRI Shapefile')
#         except Exception as e:
#             print(f"An error occurred while saving the GeoDataFrame: {e}")

##

import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMPowerPlantDataDownloader:
    # Assuming the output filename is a class attribute
    #output_filename = "/home/evangelos/data/data_sub24/swe_sub24/ISO_util_pst_pt_s2_osm_pp_power_station.shp"

    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        ox.config(log_console=True, use_cache=True)
        self.output_filename = f"/home/evangelos/osm-data/data_sub24/{country_code}_util_pst_pt_s2_osm_pp_power_station.shp"

    def download_and_process_data(self):
        # Load the region of interest geometry
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        # Ensure the geometry is appropriate
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download OSM power plant data
        gdf = ox.geometries_from_polygon(geometry, tags={'power': 'plant'})

        # Reproject geometries for accurate geometry calculation if necessary
        if self.crs_project != self.crs_global:
            gdf = gdf.to_crs(epsg=self.crs_project)

        # Filter out non-polygon geometries and reproject to global CRS
        gdf = gdf[gdf['geometry'].type == 'Polygon'].to_crs(epsg=self.crs_global)

        # Process list-type fields
        gdf = self.process_list_fields(gdf)

        # Ensure unique column names
        gdf = self.ensure_unique_column_names(gdf)

        # Save the data to a Shapefile
        self.save_data(gdf)

    def process_list_fields(self, gdf):
        # Handle list-type fields
        for col in gdf.columns:
            if pd.api.types.is_object_dtype(gdf[col]) and gdf[col].apply(lambda x: isinstance(x, list)).any():
                gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
        return gdf

    def ensure_unique_column_names(self, gdf):
        # Ensure that column names are unique after truncation
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
        # Make directories if they don't exist
        os.makedirs(os.path.dirname(OSMPowerPlantDataDownloader.output_filename), exist_ok=True)

        # Attempt to save the GeoDataFrame
        try:
            gdf.to_file(OSMPowerPlantDataDownloader.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPowerPlantDataDownloader:
#     """
#     Class for downloading and processing power substation data from OpenStreetMap.
#     """

#     # Class attribute for the output filename with the specified naming convention
#     output_filename = "/home/evangelos/data/data_sub24/swe_sub24_v2/ISO_util_pst_pt_s2_osm_pp_substation.shp"
    
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.tags = {'power': 'plant'}
#         ox.config(log_console=True, use_cache=True)

#     def download_and_process_data(self):
#         # Load the region of interest geometry
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         # Ensure the geometry is appropriate
#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download OSM data
#         gdf = ox.geometries_from_polygon(geometry, tags=self.tags)

#         # Reproject geometries for accurate geometry calculation if necessary
#         if self.crs_project:
#             gdf = gdf.to_crs(epsg=self.crs_project)

#         # Filter out geometries that are not points and reproject to global CRS for compatibility
#         gdf_points = gdf[gdf['geometry'].type == 'Point'].to_crs(epsg=self.crs_global)

#         # Handle list-type fields before saving
#         gdf_points = self.process_list_fields(gdf_points)

#         # Ensure unique column names
#         gdf_points = self.ensure_unique_column_names(gdf_points)

#         # Save the data to a Shapefile
#         self.save_data(gdf_points)

#     def process_list_fields(self, gdf):
#         # Handle list-type fields
#         for col in gdf.columns:
#             if pd.api.types.is_object_dtype(gdf[col]) and gdf[col].apply(lambda x: isinstance(x, list)).any():
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf

#     def ensure_unique_column_names(self, gdf):
#         # Ensure that column names are unique after truncation
#         unique_columns = {}
#         for col in gdf.columns:
#             col_truncated = col[:10]
#             counter = 1
#             while col_truncated in unique_columns.values():
#                 col_truncated = f"{col[:9]}{counter}"
#                 counter += 1
#             unique_columns[col] = col_truncated
#         gdf.rename(columns=unique_columns, inplace=True)
#         return gdf

#     def save_data(self, gdf):
#         # Make directories if they don't exist
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

#         # Attempt to save the GeoDataFrame
#         try:
#             gdf.to_file(self.output_filename, driver='ESRI Shapefile')
#         except Exception as e:
#             print(f"An error occurred while saving the GeoDataFrame: {e}")

