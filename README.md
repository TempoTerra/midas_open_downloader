# MIDAS Open Dataset Downloader

This project provides a mechanism for retrieving the MIDAS Open dataset from the Centre for Environmental Data Analysis (CEDA) Archive. The dataset is available in the BADC-CSV format and can be downloaded using either FTP or DAP (Data Access Protocol).

## Thirdparty Resources

* [Create CEDA account](https://services.ceda.ac.uk/cedasite/register/info/)
* [DAP Directory](https://dap.ceda.ac.uk/badc/ukmo-midas-open/data/uk-hourly-weather-obs/dataset-version-202308/)
* [FTP Directory](ftp://ftp.ceda.ac.uk/badc/ukmo-midas-open/data/uk-hourly-weather-obs/dataset-version-202308/)
* [Official CEDA repository](https://github.com/cedadev/midas-extract)

## Features

- Supports downloading MIDAS Open dataset files using FTP or DAP.
- Retrieves station capabilities files to determine the available years of data for each station.
- Downloads hourly weather observation files for specified stations and years.

## Prerequisites

- Python 3.x
- Required Python packages: `ftplib`, `requests`, `beautifulsoup4`, `cryptography`, `ContrailOnlineCAClient`, `midas_open_parser`

## Installation

1. Clone the repository:

```
git clone https://github.com/TempoTerra/midas_open_downloader.git
```

2. Install the required Python packages:

```
pip install -r requirements.txt
```

3. Set up the configuration files:

   - Create a `conf` directory in the project root.
   - Create a file named `ftp_account.txt` in the `conf` directory and add your FTP username and password, one per line.
   - Create a file named `dap_account.txt` in the `conf` directory and add your DAP username and password, one per line.

## Usage

1. Import the necessary modules in your Python script:

```python
from downloader import download_midas_open_hourly_files
from ftp_downloader import FTPDownloader
from dap_downloader import HTTPDownloader
```

2. Specify the historic county, station IDs, start year, and end year for the data you want to retrieve:

```python
historic_county = "staffordshire"
station_ids = ["00622_keele", "00623_oaken"]
start_year = 2022
end_year = 2022
```

3. Call the `download_midas_open_hourly_files` function with the desired downloader (FTP or DAP):

```python
# Use FTPDownloader
download_midas_open_hourly_files(FTPDownloader, historic_county, station_ids, start_year, end_year)

# Use HTTPDownloader (DAP)
download_midas_open_hourly_files(HTTPDownloader, historic_county, station_ids, start_year, end_year)
```

4. The downloaded files will be saved in the current directory.

## Sequence Diagram

The following sequence diagram illustrates the high-level interactions and flow of the MIDAS Open dataset retrieval process:


## Project Structure

- `downloader.py`: The main module for downloading MIDAS Open dataset files.
- `abstract_downloader.py`: An abstract base class for the downloader implementations.
- `ftp_downloader.py`: The FTP downloader implementation.
- `dap_downloader.py`: The DAP downloader implementation.
- `station_capabilities_parser.py`: A module for parsing station capabilities files.
- `conf/`: Directory for storing configuration files.
  - `ftp_account.txt`: File containing FTP username and password.
  - `dap_account.txt`: File containing DAP username and password.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE.txt).
