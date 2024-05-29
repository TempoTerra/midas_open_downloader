import logging
import time
from abc import ABC, abstractmethod
from .errors import DownloadError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MidasOpenDownloader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def setup_credentials(self):
        pass

    @abstractmethod
    def download(self, file_path):
        pass

    def cooldown(self):
        """Cooldown between downloads"""
        logger.info("Cooldown...")
        time.sleep(3)

    def get_hourly_path(self, historic_county, station, qcv, year, dataset_version="202308"):
        filebasename = "midas-open_uk-hourly-weather-obs"
        file_path = f"{self.base_path}/dataset-version-{dataset_version}/{historic_county}/{station}/qc-version-{qcv}/{filebasename}_dv-{dataset_version}_{historic_county}_{station}_qcv-{qcv}_{year}.csv"
        return file_path

    def get_station_capabilities_path(self, historic_county, station_id, dataset_version="202308"):
        filebasename = "midas-open_uk-hourly-weather-obs"
        file_path = f"{self.base_path}/dataset-version-{dataset_version}/{historic_county}/{station_id}/{filebasename}_dv-{dataset_version}_{historic_county}_{station_id}_capability.csv"
        return file_path

