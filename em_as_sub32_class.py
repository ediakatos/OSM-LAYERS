import os
import osmnx as ox
import geopandas as gpd

class OSMEmergencyAssemblyAreasDataDownloader:
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.osm_key = 'emergency'
        self.osm_value = 'assembly_point'
        ox.config(log_console=True, use_cache=True)
        self.output_filename = f"/home/evangelos/osm-data/data_sub32/{country_code}_pois_shel_pt_s2_osm_pp_assemblypoint.shp"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        gdf = ox.geometries_from_polygon(geometry, tags={self.osm_key: self.osm_value})
        gdf = gdf[gdf[self.osm_key] == self.osm_value]

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
            # Check if any entry in the column is a list
            if any(isinstance(item, list) for item in gdf[col]):
                # Convert lists to strings
                gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
        return gdf

    def ensure_unique_column_names(self, gdf):
        unique_columns = {}
        for col in gdf.columns:
            col_truncated = col[:10]  # Truncate the column name to fit Shapefile limitation
            # Ensure the truncated name is unique
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