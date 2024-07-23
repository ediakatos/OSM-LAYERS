import os
import osmnx as ox
import geopandas as gpd

class OSMRailwayDataDownloader:
    railway_tags = {
        'railway': ['rail', 'narrow_gauge', 'subway'],
        '!railway': ['miniature']
    }
    #output_filename = "/home/evangelos/data/data_sub3/swe_sub3/swe_rail_sub3.shp"

    def __init__(self, geojson_path, country_code):
        self.geojson_path = geojson_path
        ox.settings.log_console = True
        ox.settings.use_cache = True
        self.output_filename = f"/home/evangelos/osm-data/data_sub3/{country_code}_ran_rrd_ln_s2_osm_pp_railways.shp"

    def download_and_process_data(self):
        region_gdf = gpd.read_file(self.geojson_path)
        geometry_type = region_gdf['geometry'].iloc[0].geom_type
        if geometry_type not in ['Polygon', 'MultiPolygon']:
            raise ValueError("Geometry type not supported. Please provide a Polygon or MultiPolygon.")

        polygon = region_gdf['geometry'].iloc[0]
        gdf = ox.geometries_from_polygon(polygon, tags=self.railway_tags)
        gdf = gdf[gdf['railway'].isin(self.railway_tags['railway'])]
        gdf = gdf[gdf['geometry'].type.isin(['LineString', 'MultiLineString'])]
        gdf['fclass'] = gdf['railway']

        for col in gdf.columns:
            if isinstance(gdf[col].iloc[0], list):
                gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

        new_columns = {}
        for col in gdf.columns:
            new_name = col[:10]
            if new_name in new_columns.values():
                suffix = 1
                while f"{new_name[:9]}{suffix}" in new_columns.values():
                    suffix += 1
                new_name = f"{new_name[:9]}{suffix}"
            new_columns[col] = new_name
        gdf.rename(columns=new_columns, inplace=True)

        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)

        if not gdf.empty:
            try:
                gdf.to_file(filename=self.output_filename, driver='ESRI Shapefile')
                print(f"GeoDataFrame saved successfully to {self.output_filename}")
            except Exception as e:
                print(f"Failed to save GeoDataFrame: {e}")
        else:
            print("No data to save.")
