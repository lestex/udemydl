import os
import sys
import subprocess
import requests

class DLException(Exception):
    pass

class Downloader:
    def download(self, link, filename):
        try:
            self.curl_dl(link, filename)
        except OSError:
            if not os.path.exists(filename):
                import wget
                wget.download(link, filename)
            else:
                raise DLException('Failed to download this lecture')


    def curl_dl(self, link, filename):
        command = ['curl', '-C', '-', link, '-o', filename]

        cert_path = requests.certs.where()
        if cert_path:
            command.extend(['--cacert', cert_path])
        else:
            command.extend(['--insecure'])
        subprocess.call(command)


    def dl_progress(self, num_blocks, block_size, total_size):
        progress = num_blocks * block_size * 100 / total_size
        if num_blocks != 0:
            sys.stdout.write(4 * '\b')
        sys.stdout.write('%3d%%' % (progress))
