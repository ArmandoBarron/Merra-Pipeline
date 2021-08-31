wget --content-disposition --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --content-disposition -i enlaces.txt 






Python using 'Requests'
'Requests' is a popular Python library that simplifies Python access to Internet-based resources. In the following code, we demonstrate how to use 'Requests' to access GES DISC data using cookies created by a host operating system.

Make sure you have setup your Earthdata account.
Create a .netrc file in your home directory.

On Mac/Linux:

cd ~ or cd $HOME
touch .netrc
echo "machine urs.earthdata.nasa.gov login <uid> password <password>" >> .netrc (where <uid> is your user name and <password> is your Earthdata Login password without the brackets)
chmod 0600 .netrc (so only you can access it)
On Windows:

Open Notepad
Enter (without quotes): machine urs.earthdata.nasa.gov login <uid> password <password>
Save as: C:\Users\<username>\.netrc
Install Requests library (we recommend version 2.22.0 or later).
Download GES DISC data using the following Python3 code:
   # Set the URL string to point to a specific data URL. Some generic examples are:
   #   https://servername/data/path/file
   #   https://servername/opendap/path/file[.format[?subset]]
   #   https://servername/daac-bin/OTF/HTTP_services.cgi?KEYWORD=value[&KEYWORD=value]
   URL = 'your_URL_string_goes_here'
   
   # Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name. 
   FILENAME = 'your_filename_string_goes_here'
   
   import requests
   result = requests.get(URL)
   try:
      result.raise_for_status()
      f = open(FILENAME,'wb')
      f.write(result.content)
      f.close()
      print('contents of URL written to '+FILENAME)
   except:
      print('requests.get() returned an error code '+str(result.status_code))
