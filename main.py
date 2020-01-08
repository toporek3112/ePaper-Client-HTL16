import time, socket, uuid, subprocess, requests, urllib3, zipfile, os
from subprocess import DEVNULL, STDOUT

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://10.59.97.25:4000/ePaper/database/'
#!/usr/bin/python3

import time, uuid, subprocess, requests, urllib3, os, threading, socket
from termcolor import colored
from wireless import Wireless
from subprocess import DEVNULL, STDOUT

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://193.170.162.23:4000/ePaper/database/'
networks = [
        {'Name': 'projete_psk', 'Password': ''},
        {'Name': 'Karol', 'Password': 'janina123'},
        {'Name': 'ePaperBackup', 'Password': 'Topor3112'},
        {'Name': 'UPC3984DE9', 'Password': 'Kynydats4nbp'}
]
connected = True
black = lambda text: '\033[0;30m' + text + '\033[0m'
red = lambda text: '\033[0;31m' + text + '\033[0m'
>>>>>>> b0debc5fda2e09c7eb52fa962e4983a024f7233e

################################################################################
# Methodes
################################################################################

mac_num = hex(uuid.getnode()).replace('0x', '').upper()
mac = ':'.join(mac_num[i : i + 2] for i in range(0, 11, 2))

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def connectToWifi():
        while(True):
                for network in networks:
                        print(" [WIFI] connecting to " + network['Name'] + ' '*50)
                        if wireless.connect(ssid=network['Name'], password=network['Password']):
                                print(" [WIFI] connection successful \n")
                                break
                        print(" [WIFI] failure " + network['Name'])
                else:
                        print(" [system] next try to connect in 30s ")
                        time.sleep(30)

                        continue
                break

################################################################################
# Code
################################################################################

print()
print("*****************************************************************************************")
print("*********" +  red("~~~~~~~~~~") + "*****" + red("~~~~~~~~~~") + "***" + red("~~~~~~~~~~~~~~~~~~~") + "***" + red("~~~~~") + "*************************")
print("*********" + red("\         " + chr(92) )+ "****" + red("\         " + chr(92) )+ "**" + red("\                  " + chr(92) )+ "**" + red("\    " + chr(92)) + "************************")
print("**********" + red("\         " + chr(92) )+ "****" + red("\         " + chr(92) )+ "**" + red("~~~~~~~     ~~~~~~~") + "***" + red("\    " + chr(92)) + "***********************")
print("***********" + red("\         " + chr(92) )+ "****" + red("\         " + chr(92) )+ "********" + red("\    " + chr(92)) + "**********" + red("\    " + chr(92)) + "**********************")
print("************" + red( "\         ~~~~~          " + chr(92)) + "********" + red("\    " + chr(92)) + "**********" + red("\    " + chr(92)) + "*********************")
print("*************" + red("\                        " + chr(92)) + "********" + red("\    " + chr(92)) + "**********" + red("\    " + chr(92)) + "********************")
print("**************" + red( "\         ~~~~~          " + chr(92)) + "********" + red("\    " + chr(92)) + "**********" + red("\    " + chr(92)) + "*******************")
print("***************" + red("\         " + chr(92) )+ "****" + red("\         " + chr(92) )+ "********" + red("\    " + chr(92)) + "**********" + red("\    " + chr(92)) + "******************")
print("****************" + red("\         " + chr(92) )+ "****" + red("\         " + chr(92) )+ "********" + red("\    " + chr(92)) + "**********" + red("\    \~~~~~~~ ") + "*********")
print("*****************" + red("\         " + chr(92) )+ "****" + red("\         " + chr(92) )+ "********" + red("\    " + chr(92)) + "**********" + red("\           " + chr(92)) + "*********")
print("******************" +  red("~~~~~~~~~~") + "*****" + red("~~~~~~~~~~") + "*********" + red("~~~~~") + "***********" + red("~~~~~~~~~~~~") + "*********")
print("*****************************************************************************************")

wireless = Wireless()
#connectToWifi()

print("Starting script...")
print()

time.sleep(10)

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
        try:
                timetable_response = requests.get("%s/timetable/%s/%s"%(url, mac, get_ip()), stream=True, verify=False)
                
                print(' [request] getting new timetable for mac ' + mac)

                if timetable_response.status_code == 200:
                        print(' [request] successful')

                        print(' [system] removing old zip and bmp!')
                        #print(' [system] removing old zip file')
                        if(os.path.isfile('./Image.zip')):
                            os.remove("Image.zip")

                        #print(' [system] removing old bmp file')
                        for file in os.listdir('./'):
                                if file.endswith('.bmp'):
                                        os.remove('./'+file)
                                        
                        print(' [system] Successfully removed old zip and bmp!')
                        
                        print(' [system] saving new zip file')
                        with open(os.path.abspath('Image.zip'), 'wb') as f:
                            timetable_response.raw.decode_content = True
                            f.write(timetable_response.content) #writing Image.zip
                            f.close()

                        print(' [system] unzipping file')
                        subprocess.check_call(["unzip", "Image.zip"], stdout=DEVNULL, stderr=STDOUT)

                        for file in os.listdir('./'):
                                if file.endswith('.bmp') or file.endswith('.BMP'):
                                        print(' [system] renaming ' + file + ' to Image.bmp')
                                        os.rename('./'+file, './Image.bmp')
                                        break

                        print(' [ePaper] refreshing ePaper')
                        
                        subprocess.check_call(["/home/pi/Desktop/IT8951/IT8951", "0", "0", "./Image.bmp"], stdout=DEVNULL, stderr=STDOUT)
                        print(' [ePaper] successfully refreshed')
                        
                        print()
                        time.sleep(30)
                else:
                        print(' [RETURN CODE 403] Access denied, admin must authorize this device MAC: ', mac);
                        authentication_request = requests.post("%s/register"%(url), data={"macAdd": mac}, verify=False)

                        print()
                        time.sleep(30)
        except Exception as e:
                print("[ERROR] Script will restart due to the following Exception: ")
                print(e)
                
                print()
                time.sleep(30)
