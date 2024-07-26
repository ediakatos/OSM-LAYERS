import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMHospitalDataDownloader:
    osm_key = 'amenity'
    osm_value = 'hospital'
    additional_tags = [
        "emergency", "operator", "operator_type", "beds"
    ]

    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        ox.config(log_console=True, use_cache=True)
        self.output_filename = f"/home/evangelos/osm-data/{country_code}/hospital/{country_code}_heal_hea_pt_s3_osm_pp_hospital.shp"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        gdf = ox.geometries_from_polygon(geometry, tags={self.osm_key: self.osm_value})
        
        gdf_projected = gdf.to_crs(epsg=self.crs_project)
        gdf_projected['geometry'] = gdf_projected.geometry.centroid
        gdf = gdf_projected.to_crs(epsg=self.crs_global)

        if 'fclass' not in gdf.columns:
            gdf['fclass'] = self.osm_value

        for tag in self.additional_tags:
            if tag not in gdf.columns:
                gdf[tag] = pd.NA

        list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
        for col in list_type_cols:
            gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

        # Ensure unique column names for Shapefile format
        gdf = self.ensure_unique_column_names(gdf)

        # Ensure required fields and create fclass2 column
        gdf = self.ensure_required_fields(gdf)

        # Reorder columns to make fclass the first column
        columns = ['fclass'] + [col for col in gdf.columns if col != 'fclass']
        gdf = gdf[columns]

        # Reorder columns to make fclass2 the second column
        columns = ['fclass'] + ['fclass2'] + [col for col in gdf.columns if col not in ['fclass', 'fclass2']]
        gdf = gdf[columns]

        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        if not gdf.empty:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        else:
            print("No data to save.")

    def process_geometries(self, gdf):
        # Create centroids for polygon geometries and reproject
        gdf = gdf.to_crs(epsg=self.crs_project)
        gdf['geometry'] = gdf.apply(lambda row: row['geometry'].centroid if row['geometry'].geom_type != 'Point' else row['geometry'], axis=1)
        gdf = gdf.to_crs(epsg=self.crs_global)

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
                gdf[field] = None  # Use None to create NA values in GeoDataFrame

        # Add fclass2 field containing the names of the required fields or 'hospital'
        gdf['fclass2'] = gdf.apply(
            lambda row: ', '.join([field for field in required_fields if pd.notna(row[field])]) or 'hospital', axis=1
        )

        return gdf

    def save_data(self, gdf):
        # Make directories if they don't exist
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        # Attempt to save the GeoDataFrame
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")
