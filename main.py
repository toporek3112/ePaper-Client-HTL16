import time, socket, uuid, subprocess, requests, urllib3, zipfile, os
from subprocess import DEVNULL, STDOUT

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://10.59.97.25:4000/ePaper/database/'

################################################################################
# Methodes
################################################################################

def getIp():
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        return IPAddr

mac_num = hex(uuid.getnode()).replace('0x', '').upper()
mac = '-'.join(mac_num[i : i + 2] for i in range(0, 11, 2))

################################################################################
# Code
################################################################################

while True:
        timetable_response = requests.get("%s/timetable/%s"%(url, mac), stream=True, verify=False)
        
        if timetable_response.status_code == 200:
                print('[RETURN CODE 200]')
                print('Processing .zip file ...')
                
                print('Removing old .zip and .bmp ...')
                os.remove('Timetable.zip')
                for file in os.listdir('./'):
                        if file.endswith('.bmp'):
                                os.remove(file)
                                
                with open('./Timetable.zip', 'wb') as f:
                        timetable_response.raw.decode_content = True
                        f.write(timetable_response.content)
                        zipfile.ZipFile('./Timetable.zip').extractall('./')
                        print('Successfully unzipped Timetable!')
        
                        dir_array = os.listdir('./')
                        for file in dir_array:
                                if file.endswith('.bmp'):
                                        os.rename(file, 'Timetable.bmp')
                                        break

                        print('Refreshing ePaper-Image ...')
                        subprocess.check_call(["/home/pi/Desktop/IT8951/IT8951", "0", "0", "./Timetable.bmp"], stdout=DEVNULL, stderr=STDOUT)

                        print()
                        time.sleep(30)
        else:
                print('[RETURN CODE 403] Access denied, admin must authorize this device MAC', mac);
                authentication_request = requests.post("%s/register"%(url), data={"macAdd": mac, "ipAdd": getIp()}, verify=False)

                print()
                time.sleep(30)
