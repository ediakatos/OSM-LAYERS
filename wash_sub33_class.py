# import os
# import osmnx as ox
# import geopandas as gpd

# class OSMWaterSourcesDataDownloader:
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_key = 'amenity'
#         self.osm_value = 'drinking_water' # We need to confirm the correct OSM value for water sources.
#         ox.config(log_console=True, use_cache=True)
#         self.output_filename = "/home/evangelos/data/data_sub33/swe_sub33/ISO_wash_wts_pt_s2_osm_pp_waterpoint.shp"

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         gdf = ox.geometries_from_polygon(geometry, tags={self.osm_key: self.osm_value})
#         gdf = gdf[gdf[self.osm_key] == self.osm_value]

#         # Reproject geometries to the specified projection before calculating centroids
#         gdf_projected = gdf.to_crs(epsg=self.crs_project)
#         gdf_projected['geometry'] = gdf_projected['geometry'].centroid
#         gdf_projected = gdf_projected.to_crs(epsg=self.crs_global)

#         if gdf_projected.empty:
#             raise ValueError("No features to process after filtering.")

#         gdf_projected = self.process_list_fields(gdf_projected)
#         gdf_projected = self.ensure_unique_column_names(gdf_projected)

#         self.save_data(gdf_projected)
    
#     def process_list_fields(self, gdf):
#         for col in gdf.columns:
#             if any(isinstance(item, list) for item in gdf[col]):
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf

#     def ensure_unique_column_names(self, gdf):
#         unique_columns = {}
#         for col in gdf.columns:
#             col_truncated = col[:10]  # Shapefile column name limitation
#             if col_truncated in unique_columns.values():
#                 suffix = 1
#                 new_col_name = col_truncated
#                 while new_col_name in unique_columns.values():
#                     new_col_name = f"{col_truncated[:9]}_{suffix}"
#                     suffix += 1
#                 col_truncated = new_col_name
#             unique_columns[col] = col_truncated
#         gdf.rename(columns=unique_columns, inplace=True)
#         return gdf

#     def save_data(self, gdf):
#         os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
#         try:
#             gdf.to_file(self.output_filename, driver='ESRI Shapefile')
#         except Exception as e:
#             print(f"An error occurred while saving the GeoDataFrame: {e}")

# import os
# import osmnx as ox
# import geopandas as gpd

# class OSMWaterSourcesDataDownloader:
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_key = 'amenity'
#         self.osm_value = 'water_point'  # This is a general tag for water points.
#         self.osm_minimum_tags = {
#             "water_source_type": [
#                 "protected_dug_well", "unprotected_dug_well", "well", "manually_drilled_borehole",
#                 "mechanically_drilled_borehole", "borehole", "protected_spring", "rainwater_harvesting",
#                 "public_tap_stand", "infiltration_gallery", "subsurface_dam", "sand_dam", "dam",
#                 "pond", "river_direct_abstraction", "river_earth_concrete_dam", "indoor_household_connection",
#                 "outdoor_household_connection", "other"
#             ],
#             "extraction_system": ["manual", "semi-manual", "powered", "gravity"],
#             "management_structure": ["government", "private", "community", "none", "unknown"]
#         }
#         self.mapaction_file_name = "ISO_wash_wts_pt_s2_osm_pp_waterpoint"
#         ox.config(log_console=True, use_cache=True)
#         self.output_directory = "/home/evangelos/data/data_sub33/swe_sub33"
#         self.output_filename = f"{self.output_directory}/{self.mapaction_file_name}.shp"

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         # Filtering the data with the specified tags
#         tags = {self.osm_key: self.osm_value}
#         for tag_key, tag_values in self.osm_minimum_tags.items():
#             tags[tag_key] = tag_values  # This will work if OSM accepts a list of values for filtering
        
#         gdf = ox.geometries_from_polygon(geometry, tags=tags)
        
#         # Filter out points that do not match the water_source_type criteria
#         gdf = gdf[gdf[self.osm_key] == self.osm_value]
        
#         # Process the tags for water_source_type, extraction_system, and management_structure
#         for key, value_list in self.osm_minimum_tags.items():
#             gdf[key] = gdf[key].apply(lambda x: x if x in value_list else 'other')

#         # Reproject geometries to the specified projection before calculating centroids
#         gdf_projected = gdf.to_crs(epsg=self.crs_project)
#         gdf_projected['geometry'] = gdf_projected['geometry'].centroid
#         gdf_projected = gdf_projected.to_crs(epsg=self.crs_global)

#         if gdf_projected.empty:
#             raise ValueError("No features to process after filtering.")

#         gdf_projected = self.process_list_fields(gdf_projected)
#         gdf_projected = self.ensure_unique_column_names(gdf_projected)

#         self.save_data(gdf_projected)

#     def process_list_fields(self, gdf):
#         for col in gdf.columns:
#             if any(isinstance(item, list) for item in gdf[col]):
#                 gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
#         return gdf

#     def ensure_unique_column_names(self, gdf):
#         unique_columns = {}
#         for col in gdf.columns:
#             col_truncated = col[:10]  # Shapefile column name limitation
#             if col_truncated in unique_columns.values():
#                 suffix = 1
#                 new_col_name = col_truncated
#                 while new_col_name in unique_columns.values():
#                     new_col_name = f"{col_truncated[:9]}_{suffix}"
#                     suffix += 1
#                 col_truncated = new_col_name
#             unique_columns[col] = col_truncated
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

class OSMWaterSourcesDataDownloader:
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.osm_key = "amenity"
        self.osm_value = "water_point"
        self.osm_minimum_tags = {
            "water_source_type": [
                "protected_dug_well", "unprotected_dug_well", "well_(general)", 
                "manually_drilled_borehole", "mechanically_drilled_borehole", "borehole_(general)", 
                "protected_spring", "rainwater_harvesting", "public_tap_stand", 
                "infiltration_gallery", "subsurface_dam", "sand_dam", "dam_(general)", 
                "pond", "river_(direct_abstraction)", "river_(earth/concrete_dam)", 
                "indoor_household_connection_(dwelling_connection)", 
                "outdoor_household_connection_(yard_connection)", "other"
            ],
            "extraction_system": ["manual", "semi-manual", "powered", "gravity"],
            "management_structure": ["government", "private", "community", "none", "unknown"]
        }
        self.mapaction_file_name = f"{country_code}_wash_wts_pt_s2_osm_pp_waterpoint"
        self.output_filename = f"/home/evangelos/osm-data/data_sub33/{self.mapaction_file_name}.shp"
        ox.config(log_console=True, use_cache=True)

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        gdf = ox.geometries_from_polygon(geometry, tags={self.osm_key: self.osm_value})
        gdf = gdf[gdf[self.osm_key] == self.osm_value]

        # Process the minimum tags
        for key, value_list in self.osm_minimum_tags.items():
            if key in gdf.columns:
                # Standardize and filter the tags
                gdf[key] = gdf[key].apply(lambda x: x if x in value_list else 'other')
            else:
                print(f"Warning: The key '{key}' does not exist in the data. It will be skipped.")

        # Reproject geometries to the specified projection before calculating centroids
        gdf_projected = gdf.to_crs(epsg=self.crs_project)
        gdf_projected['geometry'] = gdf_projected['geometry'].centroid
        gdf_projected = gdf_projected.to_crs(epsg=self.crs_global)

        if gdf_projected.empty:
            raise ValueError("No features to process after filtering.")

        gdf_projected = self.process_list_fields(gdf_projected)
        gdf_projected = self.ensure_unique_column_names(gdf_projected)

        self.save_data(gdf_projected)
    
    def process_list_fields(self, gdf):
        for col in gdf.columns:
            if any(isinstance(item, list) for item in gdf[col]):
                gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
        return gdf

    def ensure_unique_column_names(self, gdf):
        unique_columns = {}
        for col in gdf.columns:
            col_truncated = col[:10]  # Shapefile column name limitation
            if col_truncated in unique_columns.values():
                suffix = 1
                new_col_name = col_truncated
                while new_col_name in unique_columns.values():
                    new_col_name = f"{col_truncated[:9]}_{suffix}"
                    suffix += 1
                col_truncated = new_col_name
            unique_columns[col] = col_truncated
        gdf.rename(columns=unique_columns, inplace=True)
        return gdf

    def save_data(self, gdf):
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")

