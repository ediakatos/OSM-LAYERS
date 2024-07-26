import os
import osmnx as ox
import geopandas as gpd

class OSMPortDataDownloader:
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        self.osm_tags = {'landuse': 'harbour', 'harbour': 'port'}
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/{country_code}/ports8/{country_code}_tran_por_pt_s0_osm_pp_port.shp"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)
        gdf = gdf.to_crs(epsg=self.crs_project)
        gdf['geometry'] = gdf.geometry.centroid
        gdf = gdf.to_crs(epsg=self.crs_global)

        # Handle list-type fields before saving
        list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
        for col in list_type_cols:
            gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

        # Ensure unique column names
        gdf = self.ensure_unique_column_names(gdf)

        # Make directories if they don't exist
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        # Save the data to a Shapefile
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")

    def ensure_unique_column_names(self, gdf):
        final_columns = {}
        truncated_columns = {}
        
        # Step 1: Truncate names and count occurrences
        for col in gdf.columns:
            truncated = col[:10]
            if truncated not in truncated_columns:
                truncated_columns[truncated] = 0
            truncated_columns[truncated] += 1
            final_columns[col] = truncated

        # Step 2: Ensure uniqueness by appending suffixes if necessary
        unique_columns = {}
        for original, truncated in final_columns.items():
            if truncated_columns[truncated] > 1:
                counter = truncated_columns[truncated]
                while truncated in unique_columns:
                    truncated = f"{truncated[:8]}_{counter}"
                    counter += 1
                truncated_columns[truncated] = 1
            unique_columns[truncated] = original

        # Rename columns in the GeoDataFrame
        gdf.rename(columns=unique_columns, inplace=True)
        return gdf