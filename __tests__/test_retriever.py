import pytest
import os
from unittest.mock import MagicMock, patch
from midas_open_downloader.retriever import Retriever
from midas_open_downloader.repository import Repository
from midas_open_downloader.parser import StationCapabilities

current_dir = os.path.dirname(os.path.abspath(__file__))
test_capabilities_file = os.path.join(current_dir, "test_capabilities_file.txt")

@pytest.fixture
def mock_repository():
    with patch("midas_open_downloader.retriever.Repository") as mock_repo:
        yield mock_repo.return_value

@pytest.fixture
def retriever(mock_repository):
    return Retriever()

def test_validate_year_range_valid(retriever, mock_repository):
    mock_repository.get_station_capabilities.return_value = MagicMock(spec=StationCapabilities)
    mock_repository.get_station_capabilities.return_value.get_station_years.return_value = (1972, 2022)

    assert retriever._validate_year_range("station_id", "historic_county", 2021, 2022) == True
    mock_repository.get_station_capabilities.assert_called_with("historic_county", "station_id")


def test_validate_year_range_invalid(retriever, mock_repository):
    mock_repository.get_station_capabilities.return_value = MagicMock(spec=StationCapabilities)
    mock_repository.get_station_capabilities.return_value.get_station_years.return_value = (1972, 2022)

    assert retriever._validate_year_range("station_id", "historic_county", 2019, 2023) == False
    mock_repository.get_station_capabilities.assert_called_with("historic_county", "station_id")

def test_validate_year_range_missing_capabilities(retriever, mock_repository):
    mock_repository.get_station_capabilities.return_value = None

    assert retriever._validate_year_range("station_id", "historic_county", 2021, 2022) == False
    mock_repository.get_station_capabilities.assert_called_with("historic_county", "station_id")

def test_download_hourly_files_success(retriever, mock_repository):
    mock_repository.get_station_capabilities.return_value = StationCapabilities(test_capabilities_file)
    mock_repository.download_hourly_file.return_value = "local_file_path"

    historic_county = "staffordshire"
    station_ids = ["00622_keele", "00623_oaken"]
    start_year = 2022
    end_year = 2022

    downloaded_files = retriever.download_hourly_files(historic_county, station_ids, start_year, end_year)

    assert downloaded_files is not None
    assert len(downloaded_files) == 2
    assert downloaded_files == ["local_file_path", "local_file_path"]
    mock_repository.initialize.assert_called_once()
    mock_repository.get_station_capabilities.assert_any_call("staffordshire", "00622_keele")
    mock_repository.get_station_capabilities.assert_any_call("staffordshire", "00623_oaken")
    mock_repository.download_hourly_file.assert_any_call("staffordshire", "00622_keele", 2022, "1")
    mock_repository.download_hourly_file.assert_any_call("staffordshire", "00623_oaken", 2022, "1")
    mock_repository.cooldown.assert_called()
    mock_repository.cleanup.assert_called_once()

def test_download_hourly_files_invalid_years(retriever, mock_repository):
    mock_repository.get_station_capabilities.return_value = StationCapabilities(test_capabilities_file)

    historic_county = "staffordshire"
    station_ids = ["00622_keele", "00623_oaken"]
    start_year = 2019
    end_year = 2023

    downloaded_files = retriever.download_hourly_files(historic_county, station_ids, start_year, end_year)

    assert downloaded_files is not None
    assert len(downloaded_files) == 0
    mock_repository.initialize.assert_called_once()
    mock_repository.get_station_capabilities.assert_any_call("staffordshire", "00622_keele")
    mock_repository.get_station_capabilities.assert_any_call("staffordshire", "00623_oaken")
    mock_repository.download_hourly_file.assert_not_called()
    mock_repository.cooldown.assert_not_called()
    mock_repository.cleanup.assert_called_once()

