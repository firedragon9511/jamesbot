import requests
import re
import os

class DownloadManager:
    def __init__(self) -> None:

        pass


    def get_filename_from_cd(self, cd): # https://www.codementor.io/@aviaryan/downloading-files-from-urls-in-python-77q3bs0un
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]
    
    
    def download_file(self, url: str, output: str, type_verify='image'):
        r = requests.get(url, allow_redirects=True)
        content_type = r.headers.get('content-type')

        if type_verify != '' and not content_type.startswith:
            return
        
        filename_from_url = None

        if url.find('/'):
            filename_from_url = url.rsplit('/', 1)[1]
        
        filename = self.get_filename_from_cd(r.headers.get('content-disposition'))

        if filename is None:
            filename = filename_from_url

        open(output + "/" + filename, 'wb').write(r.content)
        return True
    

if __name__ == "__main__":
    #print(DownloadManager().download_file('http://127.0.0.1:8080/obter_imagem', output='tmp'))
    #print(os.path.join("tmp", "../test"))
    pass
