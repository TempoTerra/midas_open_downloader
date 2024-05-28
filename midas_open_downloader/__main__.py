import argparse
from .retriever import Retriever

def main():
    parser = argparse.ArgumentParser(
        description='Download hourly weather data from MIDAS Open.',
        epilog='''
Example:
  python -m midas_open_downloader staffordshire "00622_keele,00623_oaken" 2022 2022
'''
    )
    parser.add_argument('historic_county', type=str, help='Historic county name')
    parser.add_argument('station_ids', type=str, help='Comma-separated list of station IDs')
    parser.add_argument('start_year', type=int, help='Start year')
    parser.add_argument('end_year', type=int, help='End year')

    args = parser.parse_args()

    # Split the comma-separated station IDs into a list
    station_ids = [station_id.strip() for station_id in args.station_ids.split(',')]

    try:
        retriever = Retriever()
        retriever.download_hourly_files(args.historic_county, station_ids, args.start_year, args.end_year)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
