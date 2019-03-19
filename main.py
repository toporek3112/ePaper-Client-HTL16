import requests, shutil, netifaces
netifaces.ifaddresses('enp0s3')
ip = netifaces.ifaddresses('enp0s3')[netifaces.AF_INET][0]['addr']
mac = netifaces.ifaddresses('enp0s3')[netifaces.AF_LINK][0]['addr']
print(ip)
print(mac)

payload = { "macAdd": mac, "ipAdd": ip}
url = 'https://172.16.34.239:4000/ePaper/database/authenticate'
r = requests.post(url, json=payload, verify=False)

print(r.text)

# wait for 2 minutes after message: wait
# send timetable request, if "not authenticated" resend /authenticate


# def download_file(url):
#     r = requests.get(url, stream=True, verify=False)
#     with open('./Timetable.bmp', 'wb') as f:
#         r.raw.decode_content = True
#         shutil.copyfileobj(r.raw, f)

# download_file(url)