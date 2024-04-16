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

# function 'get_crs_project' that takes a country code as input and returns the corresponding
# coordinate Reference System (CRS) code. CRS codes are used to translate between geographic locations
# and map coordinates.
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

def process_downloader(downloader):
    pr = cProfile.Profile()
    pr.enable()  # Start profiling
    try:
        start_time = time.time()
        downloader.download_and_process_data()
        end_time = time.time()
        duration = end_time - start_time

        pr.disable()  # Stop profiling
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        result = f"Completed: {downloader.__class__.__name__} in {duration:.2f} seconds\n{s.getvalue()}"
    except Exception as e:
        result = f"Error in {downloader.__class__.__name__}: {e}"
    finally:
        pr.disable()
    return result


# Define a function 'process_geojson_file' that takes the path of a geojson file as input.
def process_geojson_file(geojson_path):
    # Extract the country code from the filename of the geojson file. This assumes the file is named using the country code.
    country_code = os.path.basename(geojson_path).split('.')[0]
    # Call 'get_crs_project' function with the extracted country code to get the appropriate CRS code for the country.
    crs_project = get_crs_project(country_code)
    # Define a variable 'crs_global' with a value of 4326, representing the global CRS code (WGS 84).
    crs_global = 4326

    # Initialisee a list 'downloaders' with instances of various data downloader classes,
    # each initialised with parameters like the geojson path, country code, and CRS codes.
    # These instances are responsible for downloading and processing specific types of geographic data.
    downloaders = [
        OSMRoadDataDownloader(geojson_path, country_code),
        OSMRailwayDataDownloader(geojson_path, country_code),
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
        OSMLakeDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMLargeRiverDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMRiverDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMCanalDataDownloader(geojson_path, crs_project, crs_global, country_code),
        OSMRailwayStationDataDownloader(geojson_path, crs_project, crs_global, country_code),

    ]

    num_processes = cpu_count() * 2

    with Pool(processes=num_processes) as pool:
        results = pool.map(process_downloader, downloaders)
        for result in results:
            logging.info(result)
  

# The 'main' function, which serves as the entry point for the script execution.
def main():
    # Configure the logging system to display the current time, logging level, and the message in the logs.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # Create a list 'geojson_files' by listing all files in 'geojson_dir' that end with '.json' extension,
    # and joining their full path with the directory path.
    geojson_dir = "/home/evangelos/Targets/Targets_OSM"
    geojson_files = [os.path.join(geojson_dir, f) for f in os.listdir(geojson_dir) if f.endswith(".json")]

    # log txt logic
    repo_dir = "/home/evangelos/data-pipeline/OSM-LAYERS"
    log_file = os.path.join(repo_dir, "logs", "processing_log.txt")
    # Ensures log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configures logging to write to a file and print to console
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])

    # Instead of using multiprocessing, we use a simple for loop to process each file sequentially.
    for geojson_file in geojson_files:
        try:
            # Process each file using the process_geojson_file function.
            process_geojson_file(geojson_file)
            logging.info(f"Successfully processed {geojson_file}")
        except Exception as e:
            logging.error(f"Failed to process {geojson_file}: {e}")


if __name__ == "__main__":
    main()
