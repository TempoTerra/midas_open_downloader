import os
import ftplib
import requests
import logging
import time
from typing import List

from ftp_downloader import FTPDownloader
from dap_downloader import HTTPDownloader
from abstract_downloader import DownloadError
from station_capabilities_parser import parse_station_capabilities, get_station_years

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_midas_open_station_capabilities(downloader, historic_county, station_id):
    try:
        file_path = downloader.get_station_capabilities_path(historic_county, station_id)
        logger.info(f"Downloading station capabilities file: {file_path}")
        local_file_path = downloader.download(file_path)
        logger.info(f"Downloaded station capabilities file: {local_file_path}")
        return local_file_path
    except DownloadError as e:
        logger.error(f"Error downloading station capabilities file: {file_path}. Error: {str(e)}")
        return None

def download_midas_open_hourly_files(downloader_cls, historic_county, station_ids: List[str], start_year: int, end_year: int, quality_control_version="1"):
    downloaded_files = []
    with downloader_cls() as downloader:
        for station_id in station_ids:
            capabilities_file = download_midas_open_station_capabilities(downloader, historic_county, station_id)
            if capabilities_file:
                capabilities = parse_station_capabilities(capabilities_file)
                src_id = station_id.split('_')[0]
                logger.info(f"Getting years from station id {src_id}")
                logger.info(f"{capabilities}")
                first_year, last_year = get_station_years(capabilities)
                if first_year is None or last_year is None:
                    logger.error('Can not parse station years')
                    continue
                if not (start_year >= int(first_year) and end_year <= int(last_year)):
                    logger.warning(f"Requested years are not within the available range for station {station_id}. Skipping the station")
                    continue # continue to next station

            # download each year from the station directory
            for year in range(start_year, end_year + 1):
                try:
                    file_path = downloader.get_hourly_path(historic_county, station_id, quality_control_version, year)
                    logger.info(f"Downloading file: {file_path}")
                    local_file_path = downloader.download(file_path)
                    logger.info(f"Downloaded file: {local_file_path}")
                    downloaded_files.append(local_file_path)
                except DownloadError as e:
                    logger.error(f"Error downloading file: {file_path}. Error: {str(e)}")
                downloader.cooldown()
    logger.info(f"Downloaded {len(downloaded_files)} files.")

if __name__ == '__main__':
    try:
        historic_county = "staffordshire"
        station_ids = ["00622_keele", "00623_oaken"]
        start_year = 2022
        end_year = 2022
        
        # Use FTPDownloader
        # download_midas_open_hourly_files(FTPDownloader, historic_county, station_ids, start_year, end_year)
        
        # Use HTTPDownloader
        download_midas_open_hourly_files(HTTPDownloader, historic_county, station_ids, start_year, end_year)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
