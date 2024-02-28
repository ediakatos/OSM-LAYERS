import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

class OSMMarketplaceDataDownloader:
    # Class attribute for the output filename with the specified naming convention
    #output_filename = "/home/evangelos/data/data_sub15/swe_sub15/swe_cash_mkt_pt_s3_osm_pp_marketplace.shp"
    
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.osm_tags_marketplace = {'amenity': 'marketplace'}
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/data_sub15/{country_code}_cash_mkt_pt_s3_osm_pp_marketplace.shp"

    def download_and_process_data(self):
        # Load the region of interest geometry
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        # Ensure the geometry is appropriate
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download marketplace data
        gdf_marketplaces = ox.geometries_from_polygon(geometry, tags=self.osm_tags_marketplace)

        # Process geometries to centroid points
        gdf_marketplaces = self.process_geometries(gdf_marketplaces)

        # Ensure unique column names and presence of required fields
        gdf_marketplaces = self.ensure_unique_column_names(gdf_marketplaces)
        gdf_marketplaces = self.ensure_required_fields(gdf_marketplaces)

        # Save the processed data
        self.save_data(gdf_marketplaces)

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
        # Ensure that column names are unique after truncation
        new_columns = {}
        for col in gdf.columns:
            new_col = col[:10]
            counter = 1
            while new_col in new_columns.values():
                new_col = f"{col[:9]}{counter}"
                counter += 1
            new_columns[col] = new_col
        gdf.rename(columns=new_columns, inplace=True)
        return gdf

    def ensure_required_fields(self, gdf):
        # Ensure the 'name' field is included
        if 'name' not in gdf.columns:
            gdf['name'] = pd.NA
        return gdf

    def save_data(self, gdf):
        # Make directories if they don't exist
        os.makedirs(os.path.dirname(OSMMarketplaceDataDownloader.output_filename), exist_ok=True)

        # Attempt to save the GeoDataFrame
        try:
            gdf.to_file(OSMMarketplaceDataDownloader.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")
