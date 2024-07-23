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
