import os
from multiprocessing import Pool, cpu_count
import logging

# Import statements for all downloader classes
from road_sub1_class import OSMRoadDataDownloader
#from main_road_sub2_class import OSMMainRoadDataDownloader
from railway_sub3_class import OSMRailwayDataDownloader
#from urban_t_s_sub4_class import OSMUrbanRailDataDownloader
from dam_sub5_class import OSMDamDataDownloader
from school_sub6_class import OSMSchoolDataDownloader
from uni_sub7_class import OSMEducationDataDownloader
from ferry_sub8_class import OSMFerryTerminalDataDownloader
from ferry_sub9_class import OSMFerryRouteDataDownloader
from port_sub10_class import OSMPortDataDownloader
from bank_sub11_class import OSMBankDataDownloader
from atm_sub12_class import OSMATMDataDownloader
from health_fac_sub13_class import OSMHealthDataDownloader
from hosp_sub14_class import OSMHospitalDataDownloader
#from market_place_sub15_class import OSMMarketplaceDataDownloader
#from place_of_worship_sub16_class import OSMPlacesOfWorshipDataDownloader
#from refugee_site_sub17_class import OSMRefugeeSitesDataDownloader
from border_control_sub18_class import OSMBorderControlDataDownloader
from settlement_sub19_class import OSMSettlementsDataDownloader
#from buildings_sub20_class import OSMBuildingDataDownloader
#from bridges_sub21_class import OSMBridgeDataDownloader
#from pipeline_sub22_class import OSMPipelineDataDownloader
#from voltage_powerline_sub23_class import OSMPowerLinesDataDownloader
#from pst_sub24_class import OSMPowerPlantDataDownloader
#from pst_sub_sub25_class import OSMPowerSubstationDataDownloader
#from military_sub26_class import OSMMilitaryDataDownloader
from waterbodies_sub27_class import OSMLakeDataDownloader
from large_river_sub28_class import OSMLargeRiverDataDownloader
from phy_river_sub29_class import OSMRiverDataDownloader
from canal_sub30_class import OSMCanalDataDownloader
from rail2_sub31_class import OSMRailwayStationDataDownloader
#from em_as_sub32_class import OSMEmergencyAssemblyAreasDataDownloader
#from wash_sub33_class import OSMWaterSourcesDataDownloader
#from wash2_toilets_sub34_class import OSMToiletsDataDownloader

def get_crs_project(country_code):
    crs_mapping = {
        'afg': 4255,  
        'gha': 2136, 
        'swe': 3006,
        'irq': 3893,
        'ken': 4210,
        # Add more mappings as necessary
    }
    return crs_mapping.get(country_code.lower(), 4326) 

def process_geojson_file(geojson_path):
    country_code = os.path.basename(geojson_path).split('.')[0]
    crs_project = get_crs_project(country_code)
    crs_global = 4326

    # Initialize downloader instances
    downloaders = [
 #       OSMRoadDataDownloader(geojson_path, country_code),
        # OSMMainRoadDataDownloader(geojson_path, country_code), # Uncomment if needed
 #       OSMRailwayDataDownloader(geojson_path, country_code),
        # OSMUrbanRailDataDownloader(geojson_path, country_code), # Uncomment if needed
 #       OSMDamDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMSchoolDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMEducationDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMFerryTerminalDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMFerryRouteDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMPortDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMBankDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMATMDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMHealthDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMHospitalDataDownloader(geojson_path, crs_project, crs_global, country_code),
        # OSMMarketplaceDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMPlacesOfWorshipDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMRefugeeSitesDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
 #       OSMBorderControlDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMSettlementsDataDownloader(geojson_path, crs_project, crs_global, country_code),
        # OSMBuildingDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMBridgeDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMPipelineDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMPowerLinesDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMPowerPlantDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMPowerSubstationDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMMilitaryDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
 #       OSMLakeDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMLargeRiverDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMRiverDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMCanalDataDownloader(geojson_path, crs_project, crs_global, country_code),
 #       OSMRailwayStationDataDownloader(geojson_path, crs_project, crs_global, country_code),
        # OSMEmergencyAssemblyAreasDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMWaterSourcesDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
        # OSMToiletsDataDownloader(geojson_path, crs_project, crs_global, country_code), # Uncomment if needed
    ]

    for downloader in downloaders:
        try:
            downloader.download_and_process_data()
            logging.info(f"Completed: {downloader.__class__.__name__}")
        except Exception as e:
            logging.error(f"Error in {downloader.__class__.__name__}: {e}")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    geojson_dir = "/home/evangelos/Targets/Targets_OSM"
    geojson_files = [os.path.join(geojson_dir, f) for f in os.listdir(geojson_dir) if f.endswith(".json")]

    # Use a multiprocessing Pool to process each geojson file in parallel
    with Pool(processes=cpu_count()) as pool:
        pool.map(process_geojson_file, geojson_files)

if __name__ == "__main__":
    main()
