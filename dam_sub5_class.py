import os
import osmnx as ox
import geopandas as gpd

class OSMDamDataDownloader:
    # Fixed class attributes
    #output_filename = "/home/evangelos/data/data_sub5/swe_sub5/swe_dam_sub5.gpkg"
    osm_key = 'waterway'
    osm_value = 'dam'

    def __init__(self, geojson_path, crs_project, crs_global, country_code):
        self.geojson_path = geojson_path
        self.crs_project = crs_project
        self.crs_global = crs_global
        ox.config(log_console=True, use_cache=True)
        self.output_filename = f"/home/evangelos/osm-data/data_sub5/{country_code}_phys_dam_pt_s2_osm_pp_dam.shp.gpkg"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry = region_gdf['geometry'].iloc[0]

        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        gdf = ox.geometries_from_polygon(geometry, tags={self.osm_key: self.osm_value})
        gdf_projected = gdf.to_crs(epsg=self.crs_project)
        gdf_projected['geometry'] = gdf_projected['geometry'].centroid
        gdf = gdf_projected.to_crs(epsg=self.crs_global)

        list_type_cols = [col for col, dtype in gdf.dtypes.items() if dtype == object]
        for col in list_type_cols:
            gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

        if 'fclass' not in gdf.columns:
            gdf['fclass'] = self.osm_value

        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        unique_columns = {}
        for col in gdf.columns:
            col_truncated = col[:10]
            if col_truncated in unique_columns:
                unique_columns[col_truncated] += 1
                col_truncated = f"{col_truncated}_{unique_columns[col_truncated]}"
            else:
                unique_columns[col_truncated] = 1
            gdf.rename(columns={col: col_truncated}, inplace=True)

        if not gdf.empty:
            gdf.to_file(self.output_filename, driver='GPKG')
        else:
            print("No data to save.")
