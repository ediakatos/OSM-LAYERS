# import os
# import osmnx as ox
# import geopandas as gpd
# import pandas as pd

# class OSMBuildingDataDownloader:
#     # Class attribute for the output filename with the specified MapAction naming convention
#     output_filename = "/home/evangelos/data/data_sub20/swe_sub20/swe_bldg_bdg_py_s4_osm_pp_buildings.shp"
    
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.tags = {'building': True, 'amenity': True}  # Assuming 'all available' means any building with any amenity
#         ox.settings.log_console = True
#         ox.settings.use_cache = True

#     def download_and_process_data(self):
#         # Load the region of interest geometry
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         # Ensure the geometry is appropriate
#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Download building data
#         gdf_buildings = ox.geometries_from_polygon(geometry, tags=self.tags)

#         # Reproject geometries if specified
#         if self.crs_project:
#             gdf_buildings = gdf_buildings.to_crs(epsg=self.crs_project)
#             gdf_buildings = gdf_buildings.to_crs(epsg=self.crs_global)

#         # Handle list-type fields before saving
#         gdf_buildings = self.process_list_fields(gdf_buildings)

#         # Ensure unique column names
#         gdf_buildings = self.ensure_unique_column_names(gdf_buildings)

#         # Save the data to a Shapefile
#         self.save_data(gdf_buildings)

#     def process_list_fields(self, gdf):
#         # Handle list-type fields
#         for col in gdf.columns:
#             if isinstance(gdf[col].iloc[0], list):
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf

#     def ensure_unique_column_names(self, gdf):
#         # Check and modify column names for uniqueness after truncation
#         unique_columns = {}
#         for col in gdf.columns:
#             col_truncated = col[:10]
#             if col_truncated in unique_columns:
#                 unique_columns[col_truncated] += 1
#                 col_truncated = f"{col_truncated}_{unique_columns[col_truncated]}"
#             else:
#                 unique_columns[col_truncated] = 0
#             gdf.rename(columns={col: col_truncated}, inplace=True)
#         return gdf

#     def save_data(self, gdf):
#         # Make directories if they don't exist
#         os.makedirs(os.path.dirname(OSMBuildingDataDownloader.output_filename), exist_ok=True)

#         # Attempt to save the GeoDataFrame
#         try:
#             gdf.to_file(OSMBuildingDataDownloader.output_filename, driver='ESRI Shapefile', crs=self.crs_global)
#         except Exception as e:
#             print(f"An error occurred while saving the GeoDataFrame: {e}")


import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMBuildingDataDownloader:
    # Class attribute for the output filename with the specified naming convention
    #output_filename = "/home/evangelos/data/data_sub20/swe_sub20/ISO_bldg_bdg_py_s4_osm_pp_buildings.shp"
    
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/data_sub20/{country_code}_bldg_bdg_py_s4_osm_pp_buildings.shp"

    def download_and_process_data(self):
        # Load the region of interest geometry
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        # Ensure the geometry is appropriate
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download building data
        gdf_buildings = ox.geometries_from_polygon(geometry, tags={'building': True, 'amenity': True})

        # Reproject geometries if specified
        if self.crs_project:
            gdf_buildings = gdf_buildings.to_crs(epsg=self.crs_project)
        gdf_buildings = gdf_buildings.to_crs(epsg=self.crs_global)

        # Handle list-type fields before saving
        gdf_buildings = self.process_list_fields(gdf_buildings)

        # Ensure unique column names
        gdf_buildings = self.ensure_unique_column_names(gdf_buildings)

        # Save the data to a Shapefile
        self.save_data(gdf_buildings)

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
        os.makedirs(os.path.dirname(OSMBuildingDataDownloader.output_filename), exist_ok=True)

        # Attempt to save the GeoDataFrame
        try:
            gdf.to_file(OSMBuildingDataDownloader.output_filename, driver='ESRI Shapefile', crs=self.crs_global)
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")