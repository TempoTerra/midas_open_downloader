import logging

from .downloader.ftp_downloader import FTPDownloader
from .downloader.dap_downloader import HTTPDownloader
from .downloader.errors import DownloadError
from .parser import StationCapabilities

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Repository:

    def __init__(self, downloader=None):
        self.downloader = downloader
        if not downloader:
            self.downloader = HTTPDownloader()
            # self.downloader = FTPDownloader()

    def initialize(self):
        self.downloader.init()

    def cleanup(self):
        self.downloader.cleanup()

    def cooldown(self):
        self.downloader.cooldown()

    def get_station_capabilities(self, historic_county, station_id):
        capabilities_file = self.download_station_capabilities(historic_county, station_id)
        if capabilities_file:
            return StationCapabilities(capabilities_file)
        return None

    def download_station_capabilities(self, historic_county, station_id):
        try:
            file_path = self.downloader.get_station_capabilities_path(historic_county, station_id)
            logger.info(f"Downloading station capabilities file: {file_path}")
            local_file_path = self.downloader.download(file_path)
            logger.info(f"Downloaded station capabilities file: {local_file_path}")
            return local_file_path
        except DownloadError as e:
            logger.error(f"Error downloading station capabilities file: {file_path}. Error: {str(e)}")
            return None

    def download_hourly_file(self, historic_county, station_id, year, quality_control_version):
        file_path = self.downloader.get_hourly_path(historic_county, station_id, quality_control_version, year)
        logger.info(f"Downloading file: {file_path}")
        local_file_path = self.downloader.download(file_path)
        logger.info(f"Downloaded file: {local_file_path}")
        return local_file_path

