import os
import osmnx as ox
import geopandas as gpd

class OSMDamDataDownloader:
    # Fixed class attributes
    osm_key = 'waterway'
    osm_value = 'dam'

    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        ox.config(log_console=True, use_cache=True)
        self.output_filename = f"/home/evangelos/osm-data/{country_code}/dam/{country_code}_phys_dam_pt_s2_osm_pp_dam.shp"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        gdf = ox.features_from_polygon(geometry, tags={self.osm_key: self.osm_value})
        gdf_projected = gdf.to_crs(epsg=self.crs_project)
        gdf_projected['geometry'] = gdf_projected['geometry'].centroid
        gdf = gdf_projected.to_crs(epsg=self.crs_global)

        list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
        for col in list_type_cols:
            gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

        if 'fclass' not in gdf.columns:
            gdf['fclass'] = self.osm_value

        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        self.ensure_unique_column_names(gdf)

        if not gdf.empty:
            gdf.to_file(self.output_filename, driver='ESRI Shapefile')
        else:
            print("No data to save.")

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
