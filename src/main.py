import os
import time
import logging
import cProfile
import pstats
import io
from multiprocessing import Pool, cpu_count
from layers.road_sub1_class import OSMRoadDataDownloader
from layers.railway_sub3_class import OSMRailwayDataDownloader
from layers.dam_sub5_class import OSMDamDataDownloader
from layers.school_sub6_class import OSMSchoolDataDownloader
from layers.uni_sub7_class import OSMEducationDataDownloader
from layers.ferry_sub8_class import OSMFerryTerminalDataDownloader
from layers.ferry_sub9_class import OSMFerryRouteDataDownloader
from layers.port_sub10_class import OSMPortDataDownloader
from layers.bank_sub11_class import OSMBankDataDownloader
from layers.atm_sub12_class import OSMATMDataDownloader
from layers.health_fac_sub13_class import OSMHealthDataDownloader
from layers.hosp_sub14_class import OSMHospitalDataDownloader
from layers.border_control_sub18_class import OSMBorderControlDataDownloader
from layers.settlement_sub19_class import OSMSettlementsDataDownloader
from layers.waterbodies_sub27_class import OSMLakeDataDownloader
from layers.large_river_sub28_class import OSMLargeRiverDataDownloader
from layers.phy_river_sub29_class import OSMRiverDataDownloader
from layers.canal_sub30_class import OSMCanalDataDownloader
from layers.rail2_sub31_class import OSMRailwayStationDataDownloader

def get_crs_project(country_code):
    crs_mapping = {
        'afg': 4255,  
        'gha': 2136, 
        'swe': 3006,
        'irq': 3893,
        'ken': 4210,
    }
    return crs_mapping.get(country_code.lower(), 4326)

def process_downloader(downloader):
    pr = cProfile.Profile()
    pr.enable()
    try:
        start_time = time.time()
        downloader.download_and_process_data()
        end_time = time.time()
        duration = end_time - start_time

        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        result = f"Completed: {downloader.__class__.__name__} in {duration:.2f} seconds\n{s.getvalue()}"
    except Exception as e:
        result = f"Error in {downloader.__class__.__name__}: {e}"
    finally:
        pr.disable()
    return result

def process_geojson_file(geojson_path):
    country_code = os.path.basename(geojson_path).split('.')[0]
    crs_project = get_crs_project(country_code)
    crs_global = 4326

    downloaders_group1 = [
        OSMRoadDataDownloader(geojson_path, country_code),
        OSMRailwayDataDownloader(geojson_path, country_code),
        OSMLakeDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMRailwayStationDataDownloader(geojson_path, crs_project, crs_global, country_code),
    ]

    downloaders_group2 = [
        OSMDamDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMSchoolDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMEducationDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMFerryTerminalDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMFerryRouteDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMPortDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMBankDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMATMDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMHealthDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMHospitalDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMBorderControlDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMSettlementsDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMLargeRiverDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMRiverDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMCanalDataDownloader(geojson_path, crs_project, crs_global, country_code),
    ]

    for downloader in downloaders_group1:
        process_downloader(downloader)

    num_processes = cpu_count() * 2
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_downloader, downloaders_group2)
        for result in results:
            logging.info(result)

def main():
    geojson_dir = "/home/evangelos/Targets/Targets_OSM"
    geojson_files = [os.path.join(geojson_dir, f) for f in os.listdir(geojson_dir) if f.endswith(".json")]

    repo_dir = "/home/evangelos/data-pipeline/OSM-LAYERS"
    log_file = os.path.join(repo_dir, "logs", "processing_log.txt")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file, mode='a'),
                            logging.StreamHandler()
                        ])

    for geojson_file in geojson_files:
        try:
            process_geojson_file(geojson_file)
            logging.info(f"Successfully processed {geojson_file}")
        except Exception as e:
            logging.error(f"Failed to process {geojson_file}: {e}")

if __name__ == "__main__":
    main()
