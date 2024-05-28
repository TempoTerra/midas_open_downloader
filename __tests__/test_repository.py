import pytest
import os
from unittest.mock import MagicMock, patch
from midas_open_downloader.repository import Repository
from midas_open_downloader.errors import DownloadError
from midas_open_downloader.parser import StationCapabilities

current_dir = os.path.dirname(os.path.abspath(__file__))
test_capabilities_file = os.path.join(current_dir, "test_capabilities_file.txt")

@pytest.fixture
def mock_downloader():
    return MagicMock()

@pytest.fixture
def repository(mock_downloader):
    return Repository(mock_downloader)

def test_initialize(repository, mock_downloader):
    repository.initialize()
    mock_downloader.init.assert_called_once()

def test_cleanup(repository, mock_downloader):
    repository.cleanup()
    mock_downloader.cleanup.assert_called_once()

def test_cooldown(repository, mock_downloader):
    repository.cooldown()
    mock_downloader.cooldown.assert_called_once()

def test_get_station_capabilities_success(repository, mock_downloader):
    mock_downloader.get_station_capabilities_path.return_value = test_capabilities_file
    mock_downloader.download.return_value = test_capabilities_file

    station_capabilities = repository.get_station_capabilities("historic_county", "station_id")

    assert isinstance(station_capabilities, StationCapabilities)
    mock_downloader.get_station_capabilities_path.assert_called_with("historic_county", "station_id")
    mock_downloader.download.assert_called_with(test_capabilities_file)

def test_get_station_capabilities_failure(repository, mock_downloader):
    mock_downloader.get_station_capabilities_path.return_value = test_capabilities_file
    mock_downloader.download.side_effect = DownloadError("Download failed")

    station_capabilities = repository.get_station_capabilities("historic_county", "station_id")

    assert station_capabilities is None
    mock_downloader.get_station_capabilities_path.assert_called_with("historic_county", "station_id")
    mock_downloader.download.assert_called_with(test_capabilities_file)

def test_download_hourly_file_success(repository, mock_downloader):
    mock_downloader.get_hourly_path.return_value = "hourly_file_path"
    mock_downloader.download.return_value = "local_file_path"

    local_file_path = repository.download_hourly_file("historic_county", "station_id", 2022, "1")

    assert local_file_path == "local_file_path"
    mock_downloader.get_hourly_path.assert_called_with("historic_county", "station_id", "1", 2022)
    mock_downloader.download.assert_called_with("hourly_file_path")

def test_download_hourly_file_failure(repository, mock_downloader):
    mock_downloader.get_hourly_path.return_value = "hourly_file_path"
    mock_downloader.download.side_effect = DownloadError("Download failed")

    with pytest.raises(DownloadError):
        repository.download_hourly_file("historic_county", "station_id", 2022, "1")

    mock_downloader.get_hourly_path.assert_called_with("historic_county", "station_id", "1", 2022)
    mock_downloader.download.assert_called_with("hourly_file_path")
