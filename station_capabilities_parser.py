from typing import Dict, List, Tuple
from midas_open_parser import parse_badc_csv

def parse_station_capabilities(file_path: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Parse the station capabilities file and extract the capabilities for each station.

    Args:
        file_path (str): The path to the station capabilities file.

    Returns:
        Dict[str, Dict[str, Dict[str, str]]]: A dictionary containing the capabilities for each station.
            The outer dictionary uses the instrument's id as the key.
            The inner dictionary uses the id_type as the key and contains the capability details.
    """
    capabilities = {}
    data_rows = parse_badc_csv(file_path)

    for row in data_rows:
        _id = row['id']
        id_type = row['id_type']

        if _id not in capabilities:
            capabilities[_id] = {}

        capabilities[_id][id_type] = {
            'met_domain_name': row['met_domain_name'],
            'first_year': row['first_year'],
            'last_year': row['last_year']
        }

    return capabilities

def get_station_years(capabilities: Dict[str, Dict[str, Dict[str, str]]]) -> Tuple[int, int]:
    """
    Get the range of years from station capabilities.

    Args:
        capabilities (Dict[str, Dict[str, Dict[str, str]]]): The parsed station capabilities.

    Returns:
        Tuple[int, int]: A tuple containing the first year and last year of data for the station.
            If the station is not found, returns (None, None).
    """
    first_years = []
    last_years = []
    for _id in capabilities:
        station_capabilities = capabilities[_id]
        first_years += [int(cap['first_year']) for cap in station_capabilities.values()]
        last_years += [int(cap['last_year']) for cap in station_capabilities.values()]
    try:
        return min(first_years), max(last_years)
    except:
        return None, None

def get_station_ids(capabilities: Dict[str, Dict[str, Dict[str, str]]]) -> List[str]:
    """
    Get the list of station src_ids from the parsed capabilities.

    Args:
        capabilities (Dict[str, Dict[str, Dict[str, str]]]): The parsed station capabilities.

    Returns:
        List[str]: A list of station src_ids.
    """
    return list(capabilities.keys())
