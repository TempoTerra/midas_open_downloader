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
- Provides a command-line interface to easily run the downloader as a standalone module.

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

### Command-line Interface

You can use the command-line interface to run the downloader as a standalone module:

```
python -m midas_open_downloader historic_county "station_id1,station_id2" start_year end_year
```

Examples:

```
python -m midas_open_downloader staffordshire "00622_keele,00623_oaken" 2022 2022
python -m midas_open_downloader lancashire "01121_shuttleworth,01122_helmshore" 2021 2023
```

### Python Script

1. Import the necessary modules in your Python script:

```python
from midas_open_downloader.retriever import Retriever
```

2. Create an instance of the `Retriever` class:

```python
retriever = Retriever()
```


3. Call the `download_hourly_files` method with the desired arguments:

```python
historic_county = "staffordshire"
station_ids = ["00622_keele", "00623_oaken"]
start_year = 2022
end_year = 2022

retriever.download_hourly_files(historic_county, station_ids, start_year, end_year)
```


## Sequence Diagram

The following sequence diagram illustrates the high-level interactions and flow of the MIDAS Open dataset retrieval process:


## Project Structure

- `midas_open_downloader/`: The main package directory.
  - `__main__.py`: The entry point for running the package as a module.
  - `retriever.py`: The main module for downloading MIDAS Open dataset files.
  - `repository.py`: The module for interacting with the data repository.
  - `abstract_downloader.py`: An abstract base class for the downloader implementations.
  - `ftp_downloader.py`: The FTP downloader implementation.
  - `dap_downloader.py`: The DAP downloader implementation.
  - `parser.py`: A module for parsing station capabilities files.
- `conf/`: Directory for storing configuration files.
  - `ftp_account.txt`: File containing FTP username and password.
  - `dap_account.txt`: File containing DAP username and password.
- `__tests__/`: Directory for test files.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE.txt).
