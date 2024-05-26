import os
import requests
import datetime
import logging
from typing import List
from bs4 import BeautifulSoup

from abstract_downloader import DownloadError, MidasOpenDownloader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import third-party libraries
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from contrail.security.onlineca.client import OnlineCaClient


CERTS_DIR = os.path.expanduser('./.certs')
if not os.path.isdir(CERTS_DIR):
    os.makedirs(CERTS_DIR)

TRUSTROOTS_DIR = os.path.join(CERTS_DIR, 'ca-trustroots')
CREDENTIALS_FILE_PATH = os.path.join(CERTS_DIR, 'credentials.pem')

TRUSTROOTS_SERVICE = 'https://slcs.ceda.ac.uk/onlineca/trustroots/'
CERT_SERVICE = 'https://slcs.ceda.ac.uk/onlineca/certificate/'

def _cert_is_valid(cert_file, min_lifetime=0):
    """
    Returns boolean - True if the certificate is in date.
    Optional argument min_lifetime is the number of seconds
    which must remain.

    :param cert_file: certificate file path.
    :param min_lifetime: minimum lifetime (seconds)
    :return: boolean
    """
    try:
        with open(cert_file, 'rb') as f:
            crt_data = f.read()
    except IOError:
        return False

    try:
        cert = x509.load_pem_x509_certificate(crt_data, default_backend())
    except ValueError:
        return False

    now = datetime.datetime.now()

    now = datetime.datetime.now(datetime.timezone.utc)
    return (cert.not_valid_before_utc <= now
            and cert.not_valid_after_utc > now + datetime.timedelta(seconds=min_lifetime))

def fallback_signin(session, username, password):
    login_url = 'https://auth.ceda.ac.uk/account/signin/'

    # Get the CSRF token
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    # Prepare login data
    login_data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': username,
        'password': password
    }
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Referer': login_url
    }
    
    # Submit the login form
    login_response = session.post(login_url, data=login_data, headers=headers)
    
    # Check if login was successful
    if login_response.ok:
        logger.info("Login successful")
        # You can now use `session` to make further requests while logged in
        return True
    else:
        logger.error("Login failed")
        return False


class HTTPDownloader(MidasOpenDownloader):
    def __init__(self):
        super().__init__()
        self.base_url = "https://dap.ceda.ac.uk/badc/ukmo-midas-open/data/uk-hourly-weather-obs"
        self.base_path = self.base_url
        self.session = None

    def setup_credentials(self):
        # only re-get credentials if it doesn't exist
        if _cert_is_valid(CREDENTIALS_FILE_PATH):
            logger.info('Security credentials already set up.')
            try:
              self.download('/dataset-version-202308/00README_catalogue_and_licence.txt')
              return False
            except:
              logger.info('Security credentials are invalid. Updating...')
              pass
    
        with open("./conf/dap_account.txt","r") as f:
            lines = f.readlines()
            username = lines[0].strip()
            password = lines[1].strip()
    
        onlineca_client = OnlineCaClient()
        onlineca_client.ca_cert_dir = TRUSTROOTS_DIR
    
        # Set up trust roots
        trustroots = onlineca_client.get_trustroots(
            TRUSTROOTS_SERVICE,
            bootstrap=True,
            write_to_ca_cert_dir=True)
    
        # Write certificate credentials file
        key_pair, certs = onlineca_client.get_certificate(
            username,
            password,
            CERT_SERVICE,
            pem_out_filepath=CREDENTIALS_FILE_PATH)
    
        logger.info('Security credentials set up.')
        try:
          self.download('/dataset-version-202308/00README_catalogue_and_licence.txt')
          return True
        except:
          logger.info('Dap authentication failed, using fallback sign in')
          if fallback_signin(self.session, username, password):
              logger.info('Fallback sign in finished...')
              return True
        return False

        pass

    def __enter__(self):
        self.session = requests.Session()
        self.setup_credentials()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session:
            self.session.close()

    def download(self, uri):
        filename = uri.rsplit('/', 1)[-1]
        try:
            response = self.session.get(uri, cert=(CREDENTIALS_FILE_PATH))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise DownloadError(e)

        with open(filename, 'wb') as file_object:
            file_object.write(response.content)
        return filename
