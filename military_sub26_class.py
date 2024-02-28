# # import os
# # import osmnx as ox
# # import geopandas as gpd
# # import pandas as pd

# # class OSMMilitaryDataDownloader:
# #     def __init__(self, geojson_path, crs_project, crs_global):
# #         self.geojson_path = geojson_path
# #         self.crs_project = crs_project
# #         self.crs_global = crs_global
# #         self.tags = {'military': True}  # To include all military tags
# #         ox.config(log_console=True, use_cache=True)
# #         self.output_filename = "/home/evangelos/data/data_sub26/swe_sub26/ISO_util_mil_py_s2_osm_pp_militaryinstallation.shp"

# #     def download_and_process_data(self):
# #         # Load the region of interest geometry
# #         region_gdf = gpd.read_file(self.geojson_path)
# #         geometry = region_gdf['geometry'].iloc[0]

# #         # Ensure the geometry is appropriate
# #         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
# #             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

# #         # Download OSM military data
# #         gdf = ox.geometries_from_polygon(geometry, tags=self.tags)

# #         # Reproject geometries for accurate geometry calculation if necessary
# #         if self.crs_project:
# #             gdf = gdf.to_crs(epsg=self.crs_project)
        
# #         # Check if we need to convert to points
# #         if 'polygon?' in self.output_filename:
# #             gdf['geometry'] = gdf.centroid
        
# #         gdf = gdf.to_crs(epsg=self.crs_global)

# #         # Handle list-type fields before saving
# #         gdf = self.process_list_fields(gdf)

# #         # Ensure the 'fclass' field is included
# #         gdf = self.ensure_fclass_field(gdf)

# #         # Ensure unique column names
# #         gdf = self.ensure_unique_column_names(gdf)

# #         # Save the data to a Shapefile
# #         self.save_data(gdf)

# #     def process_list_fields(self, gdf):
# #         # Handle list-type fields
# #         for col in gdf.columns:
# #             if isinstance(gdf[col].iloc[0], list):
# #                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
# #         return gdf

# #     def ensure_fclass_field(self, gdf):
# #         if 'fclass' not in gdf.columns:
# #             gdf['fclass'] = 'military'
# #         return gdf

# #     def ensure_unique_column_names(self, gdf):
# #         # Ensure that column names are unique after truncation
# #         unique_columns = {}
# #         for col in gdf.columns:
# #             col_truncated = col[:10]
# #             counter = 1
# #             while col_truncated in unique_columns.values():
# #                 col_truncated = f"{col[:9]}{counter}"
# #                 counter += 1
# #             unique_columns[col] = col_truncated
# #         gdf.rename(columns=unique_columns, inplace=True)
# #         return gdf

# #     def save_data(self, gdf):
# #         # Make directories if they don't exist
# #         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

# #         # Attempt to save the GeoDataFrame
# #         try:
# #             gdf.to_file(self.output_filename, driver='ESRI Shapefile')
# #         except Exception as e:
# #             print(f"An error occurred while saving the GeoDataFrame: {e}")

# # v2

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMMilitaryDataDownloader:
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.tags = {'military': True}  # To include all military tags
#         ox.config(log_console=True, use_cache=True)
#         self.output_filename = "/home/evangelos/data/data_sub26/swe_sub26/ISO_util_mil_py_s2_osm_pp_militaryinstallation.shp"

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         gdf = ox.geometries_from_polygon(geometry, tags=self.tags)

#         if self.crs_project:
#             gdf = gdf.to_crs(epsg=self.crs_project)
        
#         gdf = gdf.to_crs(epsg=self.crs_global)

#         gdf = self.process_list_fields(gdf)
#         gdf = self.ensure_unique_column_names(gdf)
#         self.save_data(gdf)

#     def process_list_fields(self, gdf):
#         for col in gdf.columns:
#             if pd.api.types.is_object_dtype(gdf[col]) and gdf[col].apply(lambda x: isinstance(x, list)).any():
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf

#     def ensure_unique_column_names(self, gdf):
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
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
#         try:
#             gdf.to_file(self.output_filename, driver='ESRI Shapefile')
#         except Exception as e:
#             print(f"An error occurred while saving the GeoDataFrame: {e}")

# v2
# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMMilitaryDataDownloader:
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.tags = {'military': True}  # To include all military tags
#         ox.config(log_console=True, use_cache=True)
#         self.output_filename = "/home/evangelos/data/data_sub26/swe_sub26/ISO_util_mil_py_s2_osm_pp_militaryinstallation.shp"

#     def download_and_process_data(self):
#         # Load the region of interest geometry
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         # Ensure the geometry is appropriate
#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download OSM military data
#         gdf = ox.geometries_from_polygon(geometry, tags=self.tags)

#         # Reproject geometries for accurate geometry calculation if necessary
#         if self.crs_project:
#             gdf = gdf.to_crs(epsg=self.crs_project)

#         # Check if we need to convert to points
#         if 'polygon?' in self.output_filename:
#             gdf['geometry'] = gdf.centroid

#         gdf = gdf.to_crs(epsg=self.crs_global)

#         # Handle list-type fields before saving
#         gdf = self.process_list_fields(gdf)

#         # Ensure the 'fclass' field is included
#         gdf = self.ensure_fclass_field(gdf)

#         # Ensure unique column names
#         gdf = self.ensure_unique_column_names(gdf)

#         # Save the data to a Shapefile
#         self.save_data(gdf)

#     def process_list_fields(self, gdf):
#         # Handle list-type fields in all columns
#         for col in gdf.columns:
#             # Check if any value in the column is a list
#             if gdf[col].apply(lambda x: isinstance(x, list)).any():
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf


#     def ensure_fclass_field(self, gdf):
#         if 'fclass' not in gdf.columns:
#             gdf['fclass'] = 'military'
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

#         # Convert polygons to centroids if the filename suggests points should be saved
#         if 'pt' in self.output_filename or 'point' in self.output_filename.lower():
#             gdf['geometry'] = gdf.centroid

#         # Attempt to save the GeoDataFrame
#         try:
#             gdf.to_file(self.output_filename, driver='ESRI Shapefile')
#         except Exception as e:
#             print(f"An error occurred while saving the GeoDataFrame: {e}")


# v3

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMMilitaryDataDownloader:
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.tags = {'military': True}  # To include all military tags
#         ox.config(log_console=True, use_cache=True)
#         self.output_filename = "/home/evangelos/data/data_sub26/swe_sub26/ISO_util_mil_py_s2_osm_pp_militaryinstallation.shp"

#     def download_and_process_data(self):
#         # Load the region of interest geometry
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         # Ensure the geometry is appropriate
#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download OSM military data
#         gdf = ox.geometries_from_polygon(geometry, tags=self.tags)

#         # Reproject geometries for accurate geometry calculation if necessary
#         if self.crs_project:
#             gdf = gdf.to_crs(epsg=self.crs_project)

#         # Convert polygons to centroids if the filename suggests points should be saved
#         if 'pt' in self.output_filename or 'point' in self.output_filename.lower():
#             gdf['geometry'] = gdf.centroid

#         # Reproject to the global CRS for compatibility
#         gdf = gdf.to_crs(epsg=self.crs_global)

#         # Handle list-type fields before saving
#         gdf = self.process_list_fields(gdf)

#         # Ensure the 'fclass' field is included
#         gdf = self.ensure_fclass_field(gdf)

#         # Ensure unique column names
#         gdf = self.ensure_unique_column_names(gdf)

#         # Save the data to a Shapefile
#         self.save_data(gdf)

#     def process_list_fields(self, gdf):
#         # Handle list-type fields in all columns
#         for col in gdf.columns:
#             if gdf[col].apply(lambda x: isinstance(x, list)).any():
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf

#     def ensure_fclass_field(self, gdf):
#         if 'fclass' not in gdf.columns:
#             gdf['fclass'] = 'military'
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
        
#         # Convert all geometries to points if the output filename suggests saving as points
#         if 'pt' in self.output_filename or 'point' in self.output_filename.lower():
#             # Convert polygon geometries to their centroids
#             gdf['geometry'] = gdf['geometry'].centroid

#         # Check that all geometries are points after conversion
#         if not all(gdf.geometry.type == 'Point'):
#             raise ValueError("Not all geometries are points. Please check the GeoDataFrame.")

#         # Attempt to save the GeoDataFrame
#         try:
#             gdf.to_file(self.output_filename, driver='ESRI Shapefile')
#         except Exception as e:
#             print(f"An error occurred while saving the GeoDataFrame: {e}")


#v4

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMMilitaryDataDownloader:
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.tags = {'military': True}  # To include all military tags
#         ox.config(log_console=True, use_cache=True)
#         self.output_filename = "/home/evangelos/data/data_sub26/swe_sub26/ISO_util_mil_py_s2_osm_pp_militaryinstallation.shp"

#     def download_and_process_data(self):
#         # Load the region of interest geometry
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download OSM military data
#         gdf = ox.geometries_from_polygon(geometry, tags=self.tags)

#         if self.crs_project:
#             gdf = gdf.to_crs(epsg=self.crs_project)

#         # Convert to points if specified in the filename
#         if 'pt' in self.output_filename or 'point' in self.output_filename.lower():
#             gdf['geometry'] = gdf.apply(lambda row: row['geometry'].centroid if row['geometry'].geom_type != 'Point' else row['geometry'], axis=1)

#         gdf = gdf.to_crs(epsg=self.crs_global)

#         # Handle list-type fields
#         gdf = self.process_list_fields(gdf)

#         # Ensure the 'fclass' field is included
#         gdf = self.ensure_fclass_field(gdf)

#         # Ensure unique column names
#         gdf = self.ensure_unique_column_names(gdf)

#         # Save the data
#         self.save_data(gdf)

#     def process_list_fields(self, gdf):
#         for col in gdf.columns:
#             if gdf[col].dtype == object and gdf[col].apply(lambda x: isinstance(x, list)).any():
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf

#     def ensure_fclass_field(self, gdf):
#         if 'fclass' not in gdf.columns:
#             gdf['fclass'] = 'military'
#         return gdf

#     def ensure_unique_column_names(self, gdf):
#         new_columns = {}
#         for col in gdf.columns:
#             new_col = col[:10]
#             counter = 1
#             while new_col in new_columns.values():
#                 new_col = f"{col[:9]}{counter}"
#                 counter += 1
#             new_columns[col] = new_col
#         gdf.rename(columns=new_columns, inplace=True)
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

class OSMMilitaryDataDownloader:
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.tags = {'military': True}  # To include all military tags
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/data_sub26/{country_code}_util_mil_py_s2_osm_pp_militaryinstallation.shp"

    def download_and_process_data(self):
        # Load the region of interest geometry
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download OSM military data
        gdf = ox.geometries_from_polygon(geometry, tags=self.tags)

        # Reproject geometries for accurate geometry calculation if necessary
        if self.crs_project:
            gdf = gdf.to_crs(epsg=self.crs_project)

        # Convert all geometries to centroids
        gdf['geometry'] = gdf.centroid
        gdf = gdf.to_crs(epsg=self.crs_global)

        # Process list-type fields before saving
        gdf = self.process_list_fields(gdf)

        # Ensure unique column names
        gdf = self.ensure_unique_column_names(gdf)

        # Save the data to a Shapefile
        self.save_data(gdf)

    def process_list_fields(self, gdf):
        # Handle list-type fields 
        for col in gdf.columns:
            if gdf[col].apply(lambda x: isinstance(x, list)).any():
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
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        # Attempt to save the GeoDataFrame
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")