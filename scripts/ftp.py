import ftplib
import os
from ftplib import error_perm


class SingletonFTP:
    _instance = None

    def __new__(cls, host, username, password):
        if cls._instance is None:
            cls._instance = super(SingletonFTP, cls).__new__(cls)

            cls._instance.connection = ftplib.FTP(host, username, password)
        return cls._instance

    def get_connection(self):
        return self.connection

    def download_all(self, path, dest):
        try:
            self.connection.cwd(path)
        except error_perm as e:
            print(f"FTP error: {e}")
            # This is a file, not a directory.
            # Flatten the path into a filename.
            local_file_path = os.path.join(dest, path.replace('/', '_'))
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            # Check if the file already exists in the destination
            if os.path.exists(local_file_path):
                print(
                    f"File {local_file_path} already exists, skipping download.")
            else:
                with open(local_file_path, 'wb') as f:
                    self.connection.retrbinary('RETR ' + path, f.write)
            return

        # Ensure the destination directory exists.
        if not os.path.exists(dest):
            os.makedirs(dest)

        # List the files/directories in the current directory.
        items = self.connection.nlst()

        for item in items:
            print('Downloading file: ', os.path.join(path, item))
            # Recursively download files/directories.
            self.download_all(path + '/' + item, dest)

        # Go back to the parent directory.
        self.connection.cwd('..')
