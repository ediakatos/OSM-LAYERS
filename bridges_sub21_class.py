import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMBridgeDataDownloader:
    # Class attribute for the output filename with the specified naming convention
    #output_filename = "/home/evangelos/data/data_sub21/swe_sub21/ISO_tran_brg_ln_s2_osm_pp_bridge.shp"
    
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.tags = {'man_made': 'bridge', 'bridge': True}  # To include any feature with a bridge tag
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/data_sub21/{country_code}_tran_brg_ln_s2_osm_pp_bridge.shp"

    def download_and_process_data(self):
        # Load the region of interest geometry
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        # Ensure the geometry is appropriate
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download OSM bridge data
        gdf = ox.geometries_from_polygon(geometry, tags=self.tags)

        # Reproject geometries for accurate centroid calculation if they are polygons or linestrings
        gdf_projected = gdf.to_crs(epsg=self.crs_project)
        gdf['geometry'] = gdf_projected.centroid
        gdf = gdf.to_crs(epsg=self.crs_global)

        # Handle list-type fields before saving
        gdf = self.process_list_fields(gdf)

        # Ensure unique column names
        gdf = self.ensure_unique_column_names(gdf)

        # Add length attribute if it's not present
        gdf['length'] = gdf.geometry.length

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
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        # Attempt to save the GeoDataFrame
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile', crs=self.crs_global)
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")

# Usage example:
# downloader = OSMBridgeDataDownloader(
#     geojson_path="path_to_your_geojson_file.geojson",
#     crs_project=27700,  # UK national CRS
#     crs_global=4326    # Global geographic CRS
# )
# downloader.download_and_process_data()
