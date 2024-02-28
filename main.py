# from road_sub1_class import OSMRoadDataDownloader
# from main_road_sub2_class import OSMMainRoadDataDownloader
# from railway_sub3_class import OSMRailwayDataDownloader
# from urban_t_s_sub4_class import OSMUrbanRailDataDownloader
# from dam_sub5_class import OSMDamDataDownloader

# def main():
#     geojson_path = "/home/evangelos/json/GeoJSON/swe.json"
#     #future version will make it dynamic
#     crs_project = 3006  # SWEREF99 TM, for Sweden
#     crs_global = 4326   # Global geographic CRS

#     downloader = OSMRoadDataDownloader(geojson_path)
#     downloader.download_data()
#     downloader2 = OSMMainRoadDataDownloader(geojson_path)
#     downloader2.download_data()
#     downloader3 = OSMRailwayDataDownloader(geojson_path)
#     downloader3.download_and_process_data()
#     downloader4 = OSMUrbanRailDataDownloader(geojson_path)
#     downloader4.download_and_process_data()
#     downloader5 = OSMDamDataDownloader(geojson_path, crs_project, crs_global)
#     downloader5.download_and_process_data()

# if __name__ == "__main__":
#     main()
#
#
# Parallel programming

# import threading
# from road_sub1_class import OSMRoadDataDownloader
# from main_road_sub2_class import OSMMainRoadDataDownloader
# from railway_sub3_class import OSMRailwayDataDownloader
# from urban_t_s_sub4_class import OSMUrbanRailDataDownloader
# from dam_sub5_class import OSMDamDataDownloader
# from school_sub6_class import OSMSchoolDataDownloader
# from uni_sub7_class import OSMEducationDataDownloader
# from ferry_sub8_class import OSMFerryTerminalDataDownloader
# from ferry_sub9_class import OSMFerryRouteDataDownloader
# from port_sub10_class import OSMPortDataDownloader
# from bank_sub11_class import OSMBankDataDownloader
# from atm_sub12_class import OSMATMDataDownloader
# from health_fac_sub13_class import OSMHealthDataDownloader
# from hosp_sub14_class import OSMHospitalDataDownloader
# from market_place_sub15_class import OSMMarketplaceDataDownloader
# from place_of_worship_sub16_class import OSMPlacesOfWorshipDataDownloader
# from refugee_site_sub17_class import OSMRefugeeSitesDataDownloader
# from border_control_sub18_class import OSMBorderControlDataDownloader
# from settlement_sub19_class import OSMSettlementsDataDownloader
# from buildings_sub20_class import OSMBuildingDataDownloader
# from bridges_sub21_class   import OSMBridgeDataDownloader
# from pipeline_sub22_class import OSMPipelineDataDownloader
# from voltage_powerline_sub23_class import OSMPowerLinesDataDownloader
# from pst_sub24_class import OSMPowerPlantDataDownloader
# from pst_sub_sub25_class import OSMPowerSubstationDataDownloader
# from military_sub26_class import OSMMilitaryDataDownloader
# from waterbodies_sub27_class import OSMLakeDataDownloader
# from large_river_sub28_class import OSMLargeRiverDataDownloader
# from phy_river_sub29_class import OSMRiverDataDownloader
# from canal_sub30_class import OSMCanalDataDownloader
# from rail2_sub31_class import OSMRailwayStationDataDownloader
# from em_as_sub32_class import OSMEmergencyAssemblyAreasDataDownloader
# from wash_sub33_class import OSMWaterSourcesDataDownloader
# from wash2_toilets_sub34_class import OSMToiletsDataDownloader


# def main():
#     geojson_path = "/home/evangelos/Downloads/GeoJSON/swe.json"
#     crs_project = 3006  # SWEREF99 TM, for Sweden
#     crs_global = 4326   # Global geographic CRS

#     # Initialise downloader instances
#     #downloader1 = OSMRoadDataDownloader(geojson_path)
#     #downloader2 = OSMMainRoadDataDownloader(geojson_path)
#     #downloader3 = OSMRailwayDataDownloader(geojson_path)
#     #downloader4 = OSMUrbanRailDataDownloader(geojson_path)
#     #downloader5 = OSMDamDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader6 = OSMSchoolDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader7 = OSMEducationDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader8 = OSMFerryTerminalDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader9 = OSMFerryRouteDataDownloader(geojson_path, crs_project, crs_project)
#     #downloader10 = OSMPortDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader11 = OSMBankDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader12 = OSMATMDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader12.download_and_process_data()
#     #downloader13 = OSMHealthDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader14 = OSMHospitalDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader15 = OSMMarketplaceDataDownloader(geojson_path,crs_project, crs_global)
#     #downloader16 = OSMPlacesOfWorshipDataDownloader(geojson_path,crs_project, crs_global)
#     #downloader17 = OSMRefugeeSitesDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader18 = OSMBorderControlDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader19 = OSMSettlementsDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader20 = OSMBuildingDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader21 = OSMBridgeDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader22 = OSMPipelineDataDownloader(geojson_path,crs_project,crs_global)
#     #downloader23 = OSMPowerLinesDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader24 = OSMPowerPlantDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader25 = OSMPowerSubstationDataDownloader(geojson_path,crs_project, crs_global)
#     #downloader26 = OSMMilitaryDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader27 = OSMLakeDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader28 = OSMLargeRiverDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader29 = OSMRiverDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader30 = OSMCanalDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader31 = OSMRailwayStationDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader32 = OSMEmergencyAssemblyAreasDataDownloader(geojson_path, crs_project, crs_global)
#     #downloader33 = OSMWaterSourcesDataDownloader(geojson_path, crs_project, crs_global)
#     downloader34 = OSMToiletsDataDownloader(geojson_path, crs_project, crs_global)

#     # Create threads for each download process
#     threads = [
#      #   threading.Thread(target=downloader1.download_data),
#       #  threading.Thread(target=downloader2.download_data),
#        # threading.Thread(target=downloader3.download_and_process_data),
#         #threading.Thread(target=downloader4.download_and_process_data),
#         #threading.Thread(target=downloader5.download_and_process_data),
#         #threading.Thread(target=downloader6.download_and_process_data),
#         #threading.Thread(target=downloader7.download_and_process_data),
#         #threading.Thread(target=downloader8.download_and_process_data),
#         #threading.Thread(target=downloader9.download_and_process_data),
#         #threading.Thread(target=downloader10.download_and_process_data),
#         #threading.Thread(target=downloader11.download_and_process_data),
#         #threading.Thread(target=downloader12.download_and_process_data),
#         #threading.Thread(target=downloader13.download_and_process_data),
#         #threading.Thread(target=downloader14.download_and_process_data),
#         #threading.Thread(target=downloader15.download_and_process_data),
#         #threading.Thread(target=downloader16.download_and_process_data),
#         #threading.Thread(target=downloader17.download_and_process_data),
#         #threading.Thread(target=downloader18.download_and_process_data),
#         #threading.Thread(target=downloader19.download_and_process_data),
#         #threading.Thread(target=downloader20.download_and_process_data),
#         #threading.Thread(target=downloader21.download_and_process_data),
#         #threading.Thread(target=downloader22.download_and_process_data),
#         #threading.Thread(target=downloader24.download_and_process_data),
#         #threading.Thread(target=downloader25.download_and_process_data),
#         #threading.Thread(target=downloader26.download_and_process_data),
#         #threading.Thread(target=downloader27.download_and_process_data),
#         #threading.Thread(target=downloader28.download_and_process_data),
#         #threading.Thread(target=downloader29.download_and_process_data),
#         #threading.Thread(target=downloader30.download_and_process_data),
#         #threading.Thread(target=downloader31.download_and_process_data),
#         #threading.Thread(target=downloader32.download_and_process_data),
#         #threading.Thread(target=downloader33.download_and_process_data),
#         threading.Thread(target=downloader34.download_and_process_data)



#     ]

#     # Start the threads
#     for thread in threads:
#         thread.start()

#     # Wait for all threads to complete
#     for thread in threads:
#         thread.join()

# if __name__ == "__main__":
#     main()

# v3 

import os
import threading
from road_sub1_class import OSMRoadDataDownloader
from main_road_sub2_class import OSMMainRoadDataDownloader
from railway_sub3_class import OSMRailwayDataDownloader
from urban_t_s_sub4_class import OSMUrbanRailDataDownloader
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
from market_place_sub15_class import OSMMarketplaceDataDownloader
from place_of_worship_sub16_class import OSMPlacesOfWorshipDataDownloader
from refugee_site_sub17_class import OSMRefugeeSitesDataDownloader
from border_control_sub18_class import OSMBorderControlDataDownloader
from settlement_sub19_class import OSMSettlementsDataDownloader
from buildings_sub20_class import OSMBuildingDataDownloader
from bridges_sub21_class   import OSMBridgeDataDownloader
from pipeline_sub22_class import OSMPipelineDataDownloader
from voltage_powerline_sub23_class import OSMPowerLinesDataDownloader
from pst_sub24_class import OSMPowerPlantDataDownloader
from pst_sub_sub25_class import OSMPowerSubstationDataDownloader
from military_sub26_class import OSMMilitaryDataDownloader
from waterbodies_sub27_class import OSMLakeDataDownloader
from large_river_sub28_class import OSMLargeRiverDataDownloader
from phy_river_sub29_class import OSMRiverDataDownloader
from canal_sub30_class import OSMCanalDataDownloader
from rail2_sub31_class import OSMRailwayStationDataDownloader
from em_as_sub32_class import OSMEmergencyAssemblyAreasDataDownloader
from wash_sub33_class import OSMWaterSourcesDataDownloader
from wash2_toilets_sub34_class import OSMToiletsDataDownloader


def get_crs_project(country_code):
    # Define a mapping of country codes to their CRS
    crs_mapping = {
        'afg': 4255,  
        'gha': 2136, 
        'swe': 3006,
        # Add more mappings as necessary
    }
    return crs_mapping.get(country_code.lower(), 4326) 

def process_geojson_file(geojson_path):
    country_code = os.path.basename(geojson_path).split('.')[0]
    crs_project = get_crs_project(country_code)
    crs_global = 4326

    downloader1 = OSMRoadDataDownloader(geojson_path, country_code)
    downloader2 = OSMMainRoadDataDownloader(geojson_path, country_code)
    downloader3 = OSMRailwayDataDownloader(geojson_path, country_code)
    downloader4 = OSMUrbanRailDataDownloader(geojson_path, country_code)
    downloader5 = OSMDamDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader6 = OSMSchoolDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader7 = OSMEducationDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader8 = OSMFerryTerminalDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader9 = OSMFerryRouteDataDownloader(geojson_path, crs_project, crs_project, country_code)
    downloader10 = OSMPortDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader11 = OSMBankDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader12 = OSMATMDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader13 = OSMHealthDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader14 = OSMHospitalDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader15 = OSMMarketplaceDataDownloader(geojson_path,crs_project, crs_global, country_code)
    downloader16 = OSMPlacesOfWorshipDataDownloader(geojson_path,crs_project, crs_global, country_code)
    downloader17 = OSMRefugeeSitesDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader18 = OSMBorderControlDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader19 = OSMSettlementsDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader20 = OSMBuildingDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader21 = OSMBridgeDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader22 = OSMPipelineDataDownloader(geojson_path,crs_project,crs_global, country_code)
    downloader23 = OSMPowerLinesDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader24 = OSMPowerPlantDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader25 = OSMPowerSubstationDataDownloader(geojson_path,crs_project, crs_global, country_code)
    downloader26 = OSMMilitaryDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader27 = OSMLakeDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader28 = OSMLargeRiverDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader29 = OSMRiverDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader30 = OSMCanalDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader31 = OSMRailwayStationDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader32 = OSMEmergencyAssemblyAreasDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader33 = OSMWaterSourcesDataDownloader(geojson_path, crs_project, crs_global, country_code)
    downloader34 = OSMToiletsDataDownloader(geojson_path, crs_project, crs_global, country_code)

    # Create threads for each download process
    threads = [
          threading.Thread(target=downloader1.download_data),
          threading.Thread(target=downloader2.download_data),
           threading.Thread(target=downloader3.download_and_process_data),
            threading.Thread(target=downloader4.download_and_process_data),
            threading.Thread(target=downloader5.download_and_process_data),
            threading.Thread(target=downloader6.download_and_process_data),
            threading.Thread(target=downloader7.download_and_process_data),
            threading.Thread(target=downloader8.download_and_process_data),
            threading.Thread(target=downloader9.download_and_process_data),
            threading.Thread(target=downloader10.download_and_process_data),
            threading.Thread(target=downloader11.download_and_process_data),
            threading.Thread(target=downloader12.download_and_process_data),
            threading.Thread(target=downloader13.download_and_process_data),
            threading.Thread(target=downloader14.download_and_process_data),
            threading.Thread(target=downloader15.download_and_process_data),
            threading.Thread(target=downloader16.download_and_process_data),
            threading.Thread(target=downloader17.download_and_process_data),
            threading.Thread(target=downloader18.download_and_process_data),
            threading.Thread(target=downloader19.download_and_process_data),
            threading.Thread(target=downloader20.download_and_process_data),
            threading.Thread(target=downloader21.download_and_process_data),
            threading.Thread(target=downloader22.download_and_process_data),
            threading.Thread(target=downloader23.download_and_process_data),
            threading.Thread(target=downloader24.download_and_process_data),
            threading.Thread(target=downloader25.download_and_process_data),
            threading.Thread(target=downloader26.download_and_process_data),
            threading.Thread(target=downloader27.download_and_process_data),
            threading.Thread(target=downloader28.download_and_process_data),
            threading.Thread(target=downloader29.download_and_process_data),
            threading.Thread(target=downloader30.download_and_process_data),
            threading.Thread(target=downloader31.download_and_process_data),
            threading.Thread(target=downloader32.download_and_process_data),
            threading.Thread(target=downloader33.download_and_process_data),
            threading.Thread(target=downloader34.download_and_process_data)

        ]
    
        # Start the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def main():
    geojson_dir = "/home/evangelos/Targets/Targets_OSM"
    for filename in os.listdir(geojson_dir):
        if filename.endswith(".json"):
            geojson_path = os.path.join(geojson_dir, filename)
            process_geojson_file(geojson_path)

if __name__ == "__main__":
    main()
