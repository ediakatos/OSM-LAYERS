# import os
# import osmnx as ox
# import geopandas as gpd

# class OSMToiletsDataDownloader:
#     def __init__(self, geojson_path, crs_project, crs_global):
#         self.geojson_path = geojson_path
#         self.crs_project = crs_project
#         self.crs_global = crs_global
#         self.osm_key = "amenity"
#         self.osm_value = "toilets"
#         self.osm_minimum_tags = {
#             "toilets:disposal": [
#                 "flush_toilet", "septic_tank", "flush/pour_flush_to_pit_latrine", 
#                 "ventilated_improved_pit_latrine", "pit_latrine_with_slab", "composting_toilet", 
#                 "special_case", "flush/pour_flush_to_elsewhere", "pit_latrine_without_slab", 
#                 "bucket", "hanging_toilet", "no_facilities_or_bush_or_field"
#             ],
#             "toilets:wheelchair": ["yes", "no"],
#             "toilets:handwashing": ["yes", "no"]
#         }
#         self.mapaction_file_name = "ISO_wash_toi_pt_s2_osm_pp_toilet"
#         self.output_filename = f"/home/evangelos/data/data_sub34/swe_sub34/{self.mapaction_file_name}.shp"
#         ox.config(log_console=True, use_cache=True)

#     def download_and_process_data(self):
#         region_gdf = gpd.read_file(self.geojson_path)
#         geometry = region_gdf['geometry'].iloc[0]

#         if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
#             raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

#         gdf = ox.geometries_from_polygon(geometry, tags={self.osm_key: self.osm_value})
#         gdf = gdf[gdf[self.osm_key] == self.osm_value]

#         # Process the minimum tags
#         for key, value_list in self.osm_minimum_tags.items():
#             if key in gdf.columns:
#                 # Standardize and filter the tags
#                 gdf[key] = gdf[key].apply(lambda x: x if x in value_list else 'other')
#             else:
#                 print(f"Warning: The key '{key}' does not exist in the data. It will be skipped.")

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

# v2

import os
import osmnx as ox
import geopandas as gpd

class OSMToiletsDataDownloader:
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.osm_key = "amenity"
        self.osm_value = "toilets"
        self.osm_minimum_tags = {
            "toilets:disposal": [
                "flush_toilet", "septic_tank", "flush/pour_flush_to_pit_latrine", 
                "ventilated_improved_pit_latrine", "pit_latrine_with_slab", "composting_toilet", 
                "special_case", "flush/pour_flush_to_elsewhere", "pit_latrine_without_slab", 
                "bucket", "hanging_toilet", "no_facilities_or_bush_or_field"
            ],
            "toilets:wheelchair": ["yes", "no"],
            "toilets:handwashing": ["yes", "no"]
        }
        
        self.mapaction_file_name = f"{country_code}_wash_toi_pt_s2_osm_pp_toilet"
        self.output_filename = f"/home/evangelos/osm-data/data_sub34/{self.mapaction_file_name}.shp"
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