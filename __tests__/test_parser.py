import pytest
import os

from midas_open_downloader.parser import parse_station_capabilities, get_station_years, StationCapabilities

current_dir = os.path.dirname(os.path.abspath(__file__))
test_capabilities_file = os.path.join(current_dir, "test_capabilities_file.txt")
test_empty_file = os.path.join(current_dir, "test_empty_file.txt")

example_capabilities = {
    "4617_DCNN_DLY3208": {
        "id": "4617",
        "id_type": "DCNN",
        "met_domain_name": "DLY3208",
        "first_year": "1972",
        "last_year": "2006"
    },
    "4617_DCNN_AWSHRLY": {
        "id": "4617",
        "id_type": "DCNN",
        "met_domain_name": "AWSHRLY",
        "first_year": "2006",
        "last_year": "2022"
    }
}

def test_parse_station_capabilities_valid_file():
    file_path = test_capabilities_file
    expected_output = example_capabilities
    assert parse_station_capabilities(file_path) == expected_output

def test_parse_station_capabilities_empty_file():
    file_path = test_empty_file
    assert parse_station_capabilities(file_path) == {}

def test_get_station_years_valid_capabilities():
    capabilities = example_capabilities
    assert get_station_years(capabilities) == (1972, 2022)

def test_get_station_years_empty_capabilities():
    capabilities = {}
    assert get_station_years(capabilities) == (None, None)

def test_station_capabilities_init():
    file_path = test_capabilities_file
    station_capabilities = StationCapabilities(file_path)
    assert station_capabilities.capabilities == example_capabilities

def test_station_capabilities_get_station_years():
    file_path = test_capabilities_file
    station_capabilities = StationCapabilities(file_path)
    assert station_capabilities.get_station_years() == (1972, 2022)
