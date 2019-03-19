import requests, shutil, netifaces
netifaces.ifaddresses('eth0')
ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
mac = netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr']
print(ip)
print(mac)

# payload = { "macAdd": , "ipAdd": }
# url = 'https://127.0.0.1:4000/ePaper/database/timetable/FF:AA:FF:FF:FA:BF'



# def download_file(url):
#     r = requests.get(url, stream=True, verify=False)
#     with open('./Timetable.bmp', 'wb') as f:
#         r.raw.decode_content = True
#         shutil.copyfileobj(r.raw, f)

# download_file(url)