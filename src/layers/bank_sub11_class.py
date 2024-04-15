import os
import osmnx as ox
import geopandas as gpd

class OSMBankDataDownloader:
    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project  # The CRS to project geometries to before processing
        self.crs_global = crs_global    # The global CRS to convert geometries to for output
        self.osm_tags = {'amenity': 'bank'}  # OSM tags to filter bank data4
        self.attributes = ['name', 'name:en', 'name_en']
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/bank/{country_code}_cash_bnk_pt_s0_osm_pp_bank.shp"

    def download_and_process_data(self):
        # Load the region of interest geometry
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        # Ensure the geometry is appropriate
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        # Download geometries from OSM
        gdf = ox.geometries_from_polygon(geometry, tags=self.osm_tags)

        # Process geometries
        gdf = gdf.to_crs(epsg=self.crs_project)
        gdf['geometry'] = gdf.geometry.centroid
        gdf = gdf.to_crs(epsg=self.crs_global)

        # Handle list-type fields
        list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
        for col in list_type_cols:
            gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)
        
        actual_tags = gdf.columns.intersection(self.attributes)
        missing_tags = set(self.attributes) - set(actual_tags)
        if missing_tags:
            print(f"Warning: The following tags are missing from the data and will not be included: {missing_tags}")
        
        collumns_to_keep = ['geometry'] + list(actual_tags) #+ list(self.osm_tags)
        gdf = gdf[collumns_to_keep]

        # Ensure unique column names
        self.ensure_unique_column_names(gdf)

        # Save the processed data
        self.save_data(gdf)

    def ensure_unique_column_names(self, gdf):
        # Ensures that column names are unique (trimmed to 10 characters as Shapefile limitation)
        new_columns = {}
        for col in gdf.columns:
            new_col = col[:10]
            counter = 1
            while new_col in new_columns.values():
                new_col = f"{col[:9]}{counter}"
                counter += 1
            new_columns[col] = new_col
        gdf.rename(columns=new_columns, inplace=True)

    def save_data(self, gdf):
        # Make directories if they don't exist
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        # Attempt to save the GeoDataFrame
        try:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        except Exception as e:
            print(f"An error occurred while saving the GeoDataFrame: {e}")