import os
import ftplib
import logging
from typing import List

from abstract_downloader import DownloadError, MidasOpenDownloader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FTPDownloader(MidasOpenDownloader):
    def __init__(self):
        super().__init__()
        self.ftp_server = "ftp.ceda.ac.uk"
        self.base_path = "/badc/ukmo-midas-open/data/uk-hourly-weather-obs"
        self.ftp = None

    def setup_credentials(self):
        with open("./conf/ftp_account.txt", "r") as f:
            lines = f.readlines()
            self.username = lines[0].strip()
            self.password = lines[1].strip()

    def __enter__(self):
        self.setup_credentials()
        self.ftp = ftplib.FTP(self.ftp_server)
        self.ftp.login(self.username, self.password)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.ftp:
            self.ftp.close()

    def download(self, file_path):
        filename = file_path.rsplit('/', 1)[-1]
        with open(filename, 'wb') as file_object:
            try:
                self.ftp.retrbinary(f'RETR {file_path}', file_object.write)
            except ftplib.error_perm as e:
                logger.error(f"Error downloading file: {file_path}. Error: {str(e)}")
                raise DownloadError(e)
        return filename


