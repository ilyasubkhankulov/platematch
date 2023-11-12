import os

from dotenv import load_dotenv
from ftp import SingletonFTP

load_dotenv()
host = os.getenv('FTP_HOST')
username = os.getenv('FTP_USERNAME')
password = os.getenv('FTP_PASSWORD')


if __name__ == '__main__':
    ftp = SingletonFTP(host, username, password)
    ftp.download_all('/files', 'tmp')
