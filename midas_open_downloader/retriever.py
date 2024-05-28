import os
import logging
from typing import List

from .repository import Repository
from .errors import DownloadError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Retriever:

    def __init__(self):
        self.repository = Repository()

    def _validate_year_range(self, station_id, historic_county, start_year, end_year):
        capabilities = self.repository.get_station_capabilities(historic_county, station_id)
        if capabilities:
            logger.info(f"Getting years from station id {station_id}")
            first_year, last_year = capabilities.get_station_years()
            if first_year is None or last_year is None:
                logger.error(f"Can not parse station years for station {station_id}")
                return False
            if not (start_year >= int(first_year) and end_year <= int(last_year)):
                logger.warning(f"Requested years are not within the available range for station {station_id}")
                return False
            return True 
        return False
        

    def download_hourly_files(self, historic_county, station_ids: List[str], start_year: int, end_year: int, quality_control_version="1"):
        downloaded_files = []
        self.repository.initialize()
        try:
            for station_id in station_ids:
                if not self._validate_year_range(station_id, historic_county, start_year, end_year):
                    logger.warning(f"Requested years are not within the available range for station {station_id}")
                    continue

                # download each year from the station directory
                for year in range(start_year, end_year + 1):
                    try:
                        local_file_path = self.repository.download_hourly_file(historic_county, station_id, year, quality_control_version)
                        downloaded_files.append(local_file_path)
                    except DownloadError as e:
                        logger.error(f"Error downloading file: {file_path}. Error: {str(e)}")
                    self.repository.cooldown()
        except Exception as e:
            logger.error(f"Error downloading stations. Error: {e}")
        self.repository.cleanup()
        logger.info(f"Downloaded {len(downloaded_files)} files.")
        return downloaded_files

if __name__ == '__main__':
    try:
        historic_county = "staffordshire"
        station_ids = ["00622_keele", "00623_oaken"]
        start_year = 2022
        end_year = 2022

        retriever = Retriever()
        retriever.download_hourly_files(historic_county, station_ids, start_year, end_year)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
