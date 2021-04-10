from datetime import datetime, timedelta
import os
from urllib.request import urlretrieve
import urllib.error

def download_pdf(url, file_name):

    try:
        conn = urllib.request.urlopen(url)
    except urllib.error.HTTPError as err:
    # Return code error (e.g. 404, 501, ...)
        print('[ERROR] HTTPError: {}'.format(err.code))
    except urllib.error.URLError as err:
    # Not an HTTP-specific error (e.g. connection refused)
        print('[ERROR] URLError: {}'.format(err.reason))
    else:
    # HTTP response 200!
        print("[INFO] Downloading --" + file_name + "--")
        urlretrieve(url, "pdfs/" + file_name)
        print("[INFO] Download of --" + file_name + "-- COMPLETE!")


if __name__ == '__main__':

    now = datetime.now() + timedelta(days=-1)
    year = str(now.year)

    if now.month < 10:
        month = "0" + str(now.month)
    else:
        month = str(now.month)

    if now.day < 10:
        day = "0" + str(now.day)
    else:
        day = str(now.day)

    YMD = year + month + day
    #print("\nYMD:", YMD) #TEST

    file_name = "covid-gr-daily-report-" + YMD + ".pdf"
    #print("file_name:", file_name) #TEST
    url = "https://eody.gov.gr/wp-content/uploads/" + year + "/" + month + "/" + file_name

    print("URL:", url)

    if os.path.isfile('pdfs/' + file_name):
        print("[INFO]", file_name, "EXISTS on the local file system.\n[INFO] Download not required.")
    else:
        print("[INFO] File is NOT present on the local file system.\n[INFO] Starting download.")
        download_pdf(url, file_name)
