import time, socket, requests, uuid

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

        timetable_response = requests.get("%s/timetable/%s"%(url, getMac()), stream=True, verify=False)
        
        if timetable_response.status_code == 200:
                with open('./Timetable.bmp', 'wb') as f:
                        timetable_response.raw.decode_content = True
                        f.write(timetable_response.content)
                        print('successfully updated Timetable ');
                        time.sleep(900);
        else:
                print('getting Timetable failed ');
                authentication_request = requests.post("%s/register"%(url), data={"macAdd": getMac(), "ipAdd": getIp()}, verify=False)
                print('authentication ');
                time.sleep(120)