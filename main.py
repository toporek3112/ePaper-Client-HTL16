import requests, shutil

url = 'https://127.0.0.1:4000/ePaper/database/timetable/FF:AA:FF:FF:FA:BF'

def download_file(url):
    r = requests.get(url, stream=True, verify=False)
    with open('./Timetable.bmp', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

download_file(url)