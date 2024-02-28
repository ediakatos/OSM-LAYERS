# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPortDataDownloader:
#     # Class attribute for the output filename based on the MapAction file name requirement
#     output_filename = "/home/evangelos/data/data_sub10/swe_sub10/swe_tran_por_pt_s0_osm_pp_port.gpkg"

#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         # OSM tags to search for ports
#         self.osm_tags = {'landuse': ['harbour', 'industrial'], 'harbour': 'port'}
#         ox.settings.log_console = True
#         ox.settings.use_cache = True

#     def download_and_process_data(self):
#         # Load the AOI from the GeoJSON file
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         # Check if the geometry is a Polygon or MultiPolygon
#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download data from OSM based on the provided tags and the geometry of the AOI
#         gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)

#         # Convert to the projected CRS to calculate centroids
#         gdf_projected = gdf.to_crs(epsg=self.crs_project)
#         gdf_projected['geometry'] = gdf_projected['geometry'].centroid
        
#         # Convert back to the global CRS
#         gdf = gdf_projected.to_crs(epsg=self.crs_global)
        
#         list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
#         for col in list_type_cols:
#             gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

      
#         # Make directories if they don't exist
#         os.makedirs(os.path.dirname(OSMPortDataDownloader.output_filename), exist_ok=True)

#         new_columns = {}
#         suffixes = {}
#         for col in gdf.columns:
#             new_name = col[:10]
#             if new_name not in new_columns:
#                 new_columns[col] = new_name
#                 suffixes[new_name] = 1
#             else:
#                 # If the truncated name already exists, add a suffix
#                 new_name = f"{new_name[:9]}{suffixes[new_name]}"
#                 while new_name in new_columns.values():
#                     suffixes[col[:10]] += 1
#                     new_name = f"{col[:9]}{suffixes[col[:10]]}"
#                 new_columns[col] = new_name
#         gdf.rename(columns=new_columns, inplace=True)

#         # Save the data to a GeoPackage
#         if not gdf.empty:
#             gdf.to_file(OSMPortDataDownloader.output_filename, driver='GPKG')
#         else:
#             print("No data to save.")

# v2

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPortDataDownloader:
#     # Class attribute for the output filename based on the MapAction file name requirement
#     output_filename = "/home/evangelos/data/data_sub10/swe_sub10/swe_tran_por_pt_s0_osm_pp_port.gpkg"

#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         # OSM tags to search for ports
#         self.osm_tags = {'landuse': ['harbour', 'industrial'], 'harbour': 'port'}
#         ox.settings.log_console = True
#         ox.settings.use_cache = True

#     def download_and_process_data(self):
#         # Load the AOI from the GeoJSON file
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         # Check if the geometry is a Polygon or MultiPolygon
#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download data from OSM based on the provided tags and the geometry of the AOI
#         gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)

#         # Convert to the projected CRS to calculate centroids
#         gdf_projected = gdf.to_crs(epsg=self.crs_project)
#         gdf_projected['geometry'] = gdf_projected['geometry'].centroid
        
#         # Convert back to the global CRS
#         gdf = gdf_projected.to_crs(epsg=self.crs_global)
        
#         # Process list-type columns
#         list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
#         for col in list_type_cols:
#             gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

#         # Ensure unique column names
#         new_columns = {}
#         suffixes = {}
#         for col in gdf.columns:
#             new_col = col[:10]
#             if new_col not in new_columns.values():
#                 new_columns[col] = new_col
#                 suffixes[new_col] = 1
#             else:
#                 # If the truncated name already exists, increment a suffix
#                 while f"{new_col}_{suffixes[new_col]}" in new_columns.values():
#                     suffixes[new_col] += 1
#                 new_col = f"{new_col}_{suffixes[new_col]}"
#                 new_columns[col] = new_col
#                 suffixes[new_col] = 1  # Start a new suffix for the new column name
#         gdf.rename(columns=new_columns, inplace=True)

#         # Check for duplicate column names
#         assert len(set(gdf.columns)) == len(gdf.columns), "There are duplicate column names!"

#         # Make directories if they
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

#         # Save the data to a GeoPackage
#         if not gdf.empty:
#             gdf.to_file(self.output_filename, driver='GPKG')
#         else:
#             print("No data to save.")

# v3

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPortDataDownloader:
#     output_filename = "/home/evangelos/data/data_sub10/swe_sub10/swe_tran_por_pt_s0_osm_pp_port.gpkg"

#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_tags = {'landuse': ['harbour', 'industrial'], 'harbour': 'port'}
#         ox.settings.log_console = True
#         ox.settings.use_cache = True

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
#         gdf_projected = gdf.to_crs(epsg=self.crs_project)
#         gdf_projected['geometry'] = gdf_projected.geometry.centroid
#         gdf = gdf_projected.to_crs(epsg=self.crs_global)

#         self.rename_columns(gdf)
#         self.save_geodataframe(gdf)

#     def rename_columns(self, gdf):
#         unique_identifier = 1
#         new_columns = {}
#         for col in gdf.columns:
#             new_col = col[:10] if len(col) > 10 else col
#             if new_col in new_columns.values():
#                 new_col = f"{new_col[:9]}{unique_identifier}"
#                 unique_identifier += 1
#             new_columns[col] = new_col
#         gdf.rename(columns=new_columns, inplace=True)

#     def save_geodataframe(self, gdf):
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
#         if not gdf.empty:
#             gdf.to_file(self.output_filename, driver='GPKG')
#         else:
#             print("No data to save.")

#v4

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPortDataDownloader:
#     output_filename = "/home/evangelos/data/data_sub10/swe_sub10/swe_tran_por_pt_s0_osm_pp_port.gpkg"

#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_tags = {'landuse': ['harbour', 'industrial'], 'harbour': 'port'}
#         ox.settings.log_console = True
#         ox.settings.use_cache = True

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
#         gdf_projected = gdf.to_crs(epsg=self.crs_project)
#         gdf_projected['geometry'] = gdf_projected.geometry.centroid
#         gdf = gdf_projected.to_crs(epsg=self.crs_global)

#         self.handle_list_type_fields(gdf)
#         self.rename_columns(gdf)
#         self.save_geodataframe(gdf)

#     def handle_list_type_fields(self, gdf):
#         # Convert list-type fields to string
#         for col, dtype in gdf.dtypes.items():
#             if dtype == object:
#                 if gdf[col].apply(lambda x: isinstance(x, list)).any():
#                     gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

#     def rename_columns(self, gdf):
#         unique_identifier = 1
#         new_columns = {}
#         for col in gdf.columns:
#             new_col = col[:10] if len(col) > 10 else col
#             if new_col in new_columns.values():
#                 new_col = f"{new_col[:9]}{unique_identifier}"
#                 unique_identifier += 1
#             new_columns[col] = new_col
#         gdf.rename(columns=new_columns, inplace=True)

#     def save_geodataframe(self, gdf):
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
#         if not gdf.empty:
#             gdf.to_file(self.output_filename, driver='GPKG')
#         else:
#             print("No data to save.")



# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPortDataDownloader:
#     # Keep output_filename as a class attribute
#     output_filename = "/home/evangelos/data/data_sub10/swe_sub10/swe_tran_por_pt_s0_osm_pp_port.gpkg"

#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_tags = {'landuse': ['harbour', 'industrial'], 'harbour': 'port'}
#         ox.settings.log_console = True
#         ox.settings.use_cache = True

#     def download_and_process_data(self):
#         # Load the AOI from the GeoJSON file
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download data from OSM based on the provided tags and the geometry of the AOI
#         gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
        
#         # Convert to the projected CRS to calculate centroids
#         gdf = gdf.to_crs(epsg=self.crs_project)
#         gdf['geometry'] = gdf['geometry'].centroid
        
#         # Convert back to the global CRS
#         gdf = gdf.to_crs(epsg=self.crs_global)
        
#         # Handle list-type fields
#         for col in gdf.columns:
#             if isinstance(gdf[col].iloc[0], list):
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

#         # Ensure unique column names
#         new_columns = {col: col[:10] for col in gdf.columns}
#         gdf.rename(columns=new_columns, inplace=True)

#         # Make directories if they don't exist
#         os.makedirs(os.path.dirname(OSMPortDataDownloader.output_filename), exist_ok=True)

#         # Save the data to a GeoPackage
#         if not gdf.empty:
#             gdf.to_file(OSMPortDataDownloader.output_filename, driver='GPKG')
#         else:
#             print("No data to save.")

#

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPortDataDownloader:
#     # Class attribute for the output filename
#     output_filename = "/home/evangelos/data/data_sub10/swe_sub10/swe_tran_por_pt_s0_osm_pp_port.gpkg"

#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_tags = {'landuse': ['harbour', 'industrial'], 'harbour': 'port'}
#         ox.settings.log_console = True
#         ox.settings.use_cache = True

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
#         gdf = gdf.to_crs(epsg=self.crs_project)
#         gdf['geometry'] = gdf.geometry.centroid
#         gdf = gdf.to_crs(epsg=self.crs_global)

#         self.ensure_unique_column_names(gdf)

#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
#         if not gdf.empty:
#             gdf.to_file(self.output_filename, driver='GPKG')
#         else:
#             print("No data to save.")

#     def ensure_unique_column_names(self, gdf):
#         new_names = {}
#         for column in gdf.columns:
#             new_name = column[:10]
#             count = 2
#             while new_name in new_names.values():
#                 new_name = f"{column[:9]}{count}"
#                 count += 1
#             new_names[column] = new_name
#         gdf.rename(columns=new_names, inplace=True)

# # Assuming you have a main.py or similar for running the downloader
# if __name__ == "__main__":
#     downloader = OSMPortDataDownloader(
#         geojson_path="path_to_your_geojson_file.geojson",
#         crs_project=3857,  # Example CRS - Web Mercator
#         crs_global=4326   # WGS 84
#     )
#     downloader.download_and_process_data()

#  v5

# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMPortDataDownloader:
#     # Class attribute for the output filename
#     output_filename = "/home/evangelos/data/data_sub10/swe_sub10/swe_tran_por_pt_s0_osm_pp_port.gpkg"

#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_tags = {'landuse': ['harbour', 'industrial'], 'harbour': 'port'}
#         ox.settings.log_console = True
#         ox.settings.use_cache = True

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
#         gdf = gdf.to_crs(epsg=self.crs_project)
#         gdf['geometry'] = gdf.geometry.centroid
#         gdf = gdf.to_crs(epsg=self.crs_global)

#         # Handle list-type fields before saving
#         list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
#         for col in list_type_cols:
#             gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

#         # Ensure unique column names
#         self.ensure_unique_column_names(gdf)

#         # Make directories if they don't exist
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

#         # Save the data to a GeoPackage
#         if not gdf.empty:
#             gdf.to_file(self.output_filename, driver='GPKG')
#         else:
#             print("No data to save.")

#     def ensure_unique_column_names(self, gdf):
#         new_names = {}
#         for column in gdf.columns:
#             new_name = column[:10] if len(column) > 10 else column
#             count = 1
#             while new_name in new_names.values():
#                 new_name = f"{column[:9]}{count}"
#                 count += 1
#             new_names[column] = new_name
#         gdf.rename(columns=new_names, inplace=True)


# v6

import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMPortDataDownloader:
    # Class attribute for the output filename
    output_filename = "/home/evangelos/data/data_sub10/swe_sub10/swe_tran_por_pt_s0_osm_pp_port.shp"

    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.osm_tags = {'landuse': ['harbour', 'industrial'], 'harbour': 'port'}
        ox.settings.log_console = True
        ox.settings.use_cache = True
        # Class attribute for the output filename
        self.output_filename = f"/home/evangelos/osm-data/data_sub10/{country_code}_tran_por_pt_s0_osm_pp_port.shp"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
        gdf = gdf.to_crs(epsg=self.crs_project)
        gdf['geometry'] = gdf.geometry.centroid
        gdf = gdf.to_crs(epsg=self.crs_global)

        # # Handle list-type fields before saving
        list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
        for col in list_type_cols:
            gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)


        # Ensure unique column names
        self.ensure_unique_column_names(gdf)

        # Make directories if they don't exist
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        # Save the data to a GeoPackage
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")

    def ensure_unique_column_names(self, gdf):
        new_columns = {}
        for col in gdf.columns:
            new_col = col[:10]
            counter = 1
            while new_col in new_columns.values():
                new_col = f"{col[:9]}{counter}"
                counter += 1
            new_columns[col] = new_col
        gdf.rename(columns=new_columns, inplace=True)
