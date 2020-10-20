import os
import errno
import sys
import zipfile
import io

import requests
from appdirs import *

URL_CHROMEDRIVER = 'http://chromedriver.storage.googleapis.com/'
APP_DATA = user_data_dir('cromdriver')

def get_latest_release_web():
    response = requests.get(URL_CHROMEDRIVER + 'LATEST_RELEASE')
    if response.ok:
        return response.text

def create_release_directory(version):
    path = os.path.join(APP_DATA, 'RELEASE', version)
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

def get_release_directory(version):
    return os.path.join(APP_DATA, 'RELEASE', version)

def get_chromedriver_url(version, platform): #TODO : some update
    if platform is None:
        if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
            platform = 'linux'
            architecture = '64'
        elif sys.platform == 'darwin':
            platform = 'mac'
            architecture = '64'
        elif sys.platform.startswith('win'):
            platform = 'win'
            architecture = '32'
        else:
            raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    else:
        if platform == 'linux':
            platform = 'linux'
            architecture = '64'
        elif platform == 'darwin':
            platform = 'mac'
            architecture = '64'
        elif platform == 'win':
            platform = 'win'
            architecture = '32'
        else:
            raise RuntimeError('Could not determine chromedriver download URL for this platform.')

    return URL_CHROMEDRIVER + version + '/chromedriver_' + platform + architecture + '.zip'

def download_binary(url, target_location):
    response = requests.get(url)
    if response.ok:
        z_file = zipfile.ZipFile(io.BytesIO(response.content))
        z_file.extractall(target_location)
    else:
        print('Impossible to download zip from url : {}'.format(url))

def set_latest_release_file(version):
    path = os.path.join(APP_DATA, 'RELEASE', 'LATEST_RELEASE')
    with open(path, 'w') as outfile:
        outfile.write(version)

def get_latest_release_file():
    path = os.path.join(APP_DATA, 'RELEASE', 'LATEST_RELEASE')
    try:
        with open(path, 'r') as infile:
            return infile.read()
    except FileNotFoundError:
        return None
    
def updating_path(path):
    if sys.platform.startswith('win'):
        os.environ['PATH'] += ';'+ path
    else:
        os.environ['PATH'] += ':'+ path

def test_url(url):
    if requests.get(url).ok:
        return True
    return False

def download_chromedriver(version, platform=None):
    """Download the chromedriver from website

    Args:
        version (str): version of chromedriver to download
    """
    url = get_chromedriver_url(version, platform)
    
    if test_url(url):
        print('Downloading version : {}'.format(version))
        create_release_directory(version)
        target_location = get_release_directory(version)
        download_binary(url, target_location)
    else:
        raise RuntimeError('URL {} doesn\'t exists'.format(url))

def updating_chromedriver():

    latest_release_web = get_latest_release_web()
    latest_release_file = get_latest_release_file()

    if latest_release_web == latest_release_file:
        updating_path(get_release_directory(latest_release_file))
    else:

        download_chromedriver(latest_release_web)
        
        set_latest_release_file(latest_release_web)
        latest_release_file = get_latest_release_file()

        updating_path(get_release_directory(latest_release_file))