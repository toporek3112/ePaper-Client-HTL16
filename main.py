# import requests, shutil, netifaces

import time, socket, socket, requests, shutil, uuid

url = 'https://127.0.0.1:4000/ePaper/database/'


################################################################################
# Methodes
################################################################################

def getIp():
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        return IPAddr

def getMac():
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = '-'.join(mac_num[i : i + 2] for i in range(0, 11, 2))
        return mac



################################################################################
# Code
################################################################################

while True:

        timetable_request = requests.get("%s/timetable/%s"%(url, getMac()), stream=True, verify=False)
        with open('./Timetable.bmp', 'wb') as f:
                if timetable_request.status_code != 401:
                        timetable_request.raw.decode_content = True
                        shutil.copyfileobj(timetable_request.raw, f)
                        print('successfully updated Timetable ');
                        time.sleep(900);
                else:
                        print('getting Timetable failed ');
                        authentication_request = requests.post("%s/authenticate"%(url), data={"macAdd": getMac(), "ipAdd": getIp()}, verify=False)
                        print('authentication ');
                        time.sleep(120)