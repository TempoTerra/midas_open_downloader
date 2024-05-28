from typing import Dict, List, Tuple
import os
import logging
from midas_open_parser import parse_badc_csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class StationCapabilities:
    def __init__(self, capabilities_file):
        self.capabilities = parse_station_capabilities(capabilities_file)

    def get_station_years(self):
        first_year, last_year = get_station_years(self.capabilities)
        return first_year, last_year


def parse_station_capabilities(file_path: str) -> Dict[str, Dict[str, str]]:
    """
    Parse the station capabilities file and extract the capabilities for each station.

    Args:
        file_path (str): The path to the station capabilities file.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary containing the capabilities for each station.
        The key is a combination of id, id_type, and met_domain_name.
        The value is a dictionary containing the id, id_type, met_domain_name, first_year, and last_year for the station.
    """
    capabilities = {}
    data_rows = parse_badc_csv(file_path)

    for row in data_rows:
        _id = row['id']
        id_type = row['id_type']
        met_domain_name = row['met_domain_name']
        key = f"{_id}_{id_type}_{met_domain_name}"
        capabilities[key] = {
            'id': _id,
            'id_type': id_type,
            'met_domain_name': met_domain_name,
            'first_year': row['first_year'],
            'last_year': row['last_year']
        }

    return capabilities

def get_station_years(capabilities: Dict[str, Dict[str, str]]) -> Tuple[int, int]:
    """
    Get the range of years from station capabilities.

    Args:
        capabilities (Dict[str, Dict[str, str]]): The parsed station capabilities.

    Returns:
        Tuple[int, int]: A tuple containing the first year and last year of data for the station.
        If the station is not found or there are no valid years, returns (None, None).
    """
    first_years = []
    last_years = []
    for capability_key in capabilities:
        station_capability = capabilities[capability_key]
        first_year = station_capability.get('first_year')
        last_year = station_capability.get('last_year')
        if first_year is not None and last_year is not None:
            first_years.append(int(first_year))
            last_years.append(int(last_year))
    if first_years and last_years:
        return min(first_years), max(last_years)
    else:
        return None, None
