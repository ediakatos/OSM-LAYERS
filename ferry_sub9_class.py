# osm_ferry_route_data_downloader.py
import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMFerryRouteDataDownloader:
    # Class attribute for the output filename based on the MapAction file name requirement
   # output_filename = "/home/evangelos/osm-data/ferry_route/swe_tran_fer_ln_s2_osm_pp_ferryroute.gpkg"


    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        # OSM tags to search for ferry routes
        self.osm_tags = {'route': 'ferry'}  
        ox.config(log_console=True, use_cache=True)
        
        self.output_filename = f"/home/evangelos/osm-data/ferry_route/{country_code}_tran_fer_ln_s2_osm_pp_ferryroute.gpkg"

    def download_and_process_data(self):
        # Load the AOI from the GeoJSON file
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        # Check if the geometry is a Polygon or MultiPolygon
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download data from OSM based on the provided tags and the geometry of the AOI
        gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)

        # Ensure all tags are represented as columns, even if no data is present
        for key in self.osm_tags.values():
            if key not in gdf.columns:
                gdf[key] = pd.NA

        # # Handle list-type fields before saving
        # for col in gdf.columns:
        #     if isinstance(gdf[col].iloc[0], list):
        #         gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
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
