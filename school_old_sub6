import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMSchoolDataDownloader:
    # Fixed class attribute for the output filename
    #output_filename = "/home/evangelos/data/data_sub6/swe_sub6/swe_schools_sub6.gpkg"

    # Fixed class attributes for the OSM query
    osm_key = 'amenity'
    osm_value = 'school'
    # Additional tags that need to be present in the data
    additional_tags = [
        "operator", "operator_type", "capacity", "grades",
        "min_age", "max_age", "school:gender"
    ]

    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        ox.config(log_console=True, use_cache=True)
        self.output_filename = f"/home/evangelos/osm-data/data_sub6/{country_code}_educ_edu_pt_s3_osm_pp_schools.gpkg"

    def download_and_process_data(self):
        # Load the AOI from the GeoJSON file
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        # Check if the geometry is a Polygon or MultiPolygon
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download data from OSM based on the provided tags and the geometry of the AOI
        gdf = ox.geometries_from_polygon(geometry, tags={self.osm_key: self.osm_value})
        
        # Convert to the projected CRS to calculate centroids
        gdf_projected = gdf.to_crs(epsg=self.crs_project)
        gdf_projected['geometry'] = gdf_projected['geometry'].centroid
        
        # Convert back to the global CRS
        gdf = gdf_projected.to_crs(epsg=self.crs_global)

        # Add 'fclass' column with 'school' as the value
        if 'fclass' not in gdf.columns:
            gdf['fclass'] = self.osm_value

        # Ensure all additional tags are represented as columns
        for tag in self.additional_tags:
            if tag not in gdf.columns:
                gdf[tag] = pd.NA

        # Handle list-type fields before saving
        #for col in gdf.columns:
          #  if isinstance(gdf[col].iloc[0], list):
            #    gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
        #Handle list-type fields before saving
        list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
        for col in list_type_cols:
            gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)


        # Make directories if they don't exist
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        # Truncate column names and ensure uniqueness
        unique_columns = {}
        for col in gdf.columns:
            col_truncated = col[:10]
            if col_truncated in unique_columns:
                unique_columns[col_truncated] += 1
                col_truncated = f"{col_truncated}_{unique_columns[col_truncated]}"
            else:
                unique_columns[col_truncated] = 1
            gdf.rename(columns={col: col_truncated}, inplace=True)

        # Save the data to a GeoPackage
        if not gdf.empty:
            gdf.to_file(self.output_filename, driver='GPKG')
        else:
            print("No data to save.")
