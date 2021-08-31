   # Set the URL string to point to a specific data URL. Some generic examples are:
   #   https://servername/data/path/file
   #   https://servername/opendap/path/file[.format[?subset]]
   #   https://servername/daac-bin/OTF/HTTP_services.cgi?KEYWORD=value[&KEYWORD=value]
import requests
import os

class SessionWithHeaderRedirection(requests.Session):
 
    AUTH_HOST = 'urs.earthdata.nasa.gov'
 
    def __init__(self, username, password):
 
        super().__init__()
 
        self.auth = (username, password)
 
  
 
   # Overrides from the library to keep headers when redirected to or from
 
   # the NASA auth host.
 
    def rebuild_auth(self, prepared_request, response):
 
        headers = prepared_request.headers
 
        url = prepared_request.url
 
  
 
        if 'Authorization' in headers:
 
            original_parsed = requests.utils.urlparse(response.request.url)
 
            redirect_parsed = requests.utils.urlparse(url)
 
  
 
            if (original_parsed.hostname != redirect_parsed.hostname) and \
                    redirect_parsed.hostname != self.AUTH_HOST and \
                    original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
 
  
 
        return


filename = "enlaces.txt"
carpeta = "./resultados/"
user = "armandobarron"
password= "NASA482bdb2a0d"

try:
   os.stat(carpeta)
except:
   os.mkdir(carpeta)

with open(filename) as f:
   enlaces = f.readlines()


session = SessionWithHeaderRedirection(user, password)


for URL in enlaces:

   # Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name. 
   FILENAME = carpeta+URL.split("/")[-1]

   result = requests.get(URL,auth=('armandobarron', 'NASA482bdb2a0d'))
   print(URL)
   try:
      # submit the request using the session
      response = session.get(URL, stream=True)
      print(response.status_code)
      # raise an exception in case of http errors
      response.raise_for_status()  
      # save the file
      with open(FILENAME, 'wb') as fd:
         for chunk in response.iter_content(chunk_size=1024*1024):
               fd.write(chunk)
   
   except requests.exceptions.   HTTPError as e:
      # handle any errors here
      print(e)