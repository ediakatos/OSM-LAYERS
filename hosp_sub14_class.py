import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMHospitalDataDownloader:
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.osm_tags_hospital = {'amenity': 'hospital'}
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/{country_code}/hosp/{country_code}_heal_hea_pt_s3_osm_pp_hospital.shp"

    def download_and_process_data(self):
        # Load the region of interest geometry
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        # Ensure the geometry is appropriate
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download hospital data
        gdf_hospitals = ox.geometries_from_polygon(geometry, tags=self.osm_tags_hospital)

        # Process geometries to centroid points
        gdf_hospitals = self.process_geometries(gdf_hospitals)

        # Add 'fclass' column with relevant values
        gdf_hospitals['fclass'] = gdf_hospitals.apply(lambda row: self.determine_fclass(row), axis=1)

        # Ensure unique column names and presence of required fields
        gdf_hospitals = self.ensure_unique_column_names(gdf_hospitals)
        gdf_hospitals = self.ensure_required_fields(gdf_hospitals)

        # Save the processed data
        self.save_data(gdf_hospitals)

    def process_geometries(self, gdf):
        # Create centroids for polygon geometries and reproject
        gdf = gdf.to_crs(epsg=self.crs_project)
        gdf['geometry'] = gdf.apply(lambda row: row['geometry'].centroid if row['geometry'].geom_type != 'Point' else row['geometry'], axis=1)
        gdf = gdf.to_crs(epsg=self.crs_global)

        # Handle list-type fields
        for col in gdf.columns:
            if pd.api.types.is_object_dtype(gdf[col]) and gdf[col].apply(lambda x: isinstance(x, list)).any():
                gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

        return gdf

    def ensure_unique_column_names(self, gdf):
        truncated_columns = {}
        final_columns = {}
        unique_suffixes = {}

        # Step 1: Truncate names
        for col in gdf.columns:
            truncated = col[:10]
            if truncated not in truncated_columns:
                truncated_columns[truncated] = 1
            else:
                truncated_columns[truncated] += 1
            final_columns[col] = truncated

        # Step 2: Resolve duplicates by adding a unique suffix
        for original, truncated in final_columns.items():
            if truncated_columns[truncated] > 1:
                if truncated not in unique_suffixes:
                    unique_suffixes[truncated] = 1
                else:
                    unique_suffixes[truncated] += 1
                suffix = unique_suffixes[truncated]
                suffix_length = len(str(suffix))
                truncated_with_suffix = truncated[:10-suffix_length] + str(suffix)
                final_columns[original] = truncated_with_suffix

        gdf.rename(columns=final_columns, inplace=True)
        return gdf

    def ensure_required_fields(self, gdf):
        # Ensure specified columns are included, create them if not present
        required_fields = ['emergency', 'operator', 'operator_type', 'beds']
        for field in required_fields:
            if field not in gdf.columns:
                gdf[field] = pd.NA

        return gdf

    def determine_fclass(self, row):
        # Determine the fclass value based on the row's attributes
        if 'emergency' in row and pd.notna(row['emergency']):
            return 'emergency'
        elif 'operator' in row and pd.notna(row['operator']):
            return 'operator'
        elif 'operator_type' in row and pd.notna(row['operator_type']):
            return 'operator_type'
        elif 'beds' in row and pd.notna(row['beds']):
            return 'beds'
        else:
            return 'hospital'

    def save_data(self, gdf):
        # Make directories if they don't exist
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        # Attempt to save the GeoDataFrame
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")