#!/usr/bin/env python3 

import time, uuid, subprocess, requests, urllib3, os, threading, socket, traceback
from termcolor import colored
from wireless import Wireless
from subprocess import DEVNULL, STDOUT

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

path = '/home/ePaper/Documents'
log = open("/root/ePaperScript.log", "w")
url = 'https://192.168.43.247:4000/ePaper/database/'
networks = [
        {'Name': 'projete_psk', 'Password': ''},
        {'Name': 'ePaperBackup', 'Password': ''}
]
connected = True
black = lambda text: '\033[0;30m' + text + '\033[0m'
red = lambda text: '\033[0;31m' + text + '\033[0m'

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

time.sleep(10)
print("Starting script...")
print()


while True:
        try:
                timetable_response = requests.get("%s/timetable/%s/%s"%(url, mac, get_ip()), stream=True, verify=False)
                
                print(' [request] getting new timetable for mac ' + mac)

                if timetable_response.status_code == 200:
                        print(' [request] successful')

                        print(' [system] removing old zip and bmp!')
                        if(os.path.isfile(path + 'Image.zip')):
                            os.remove(path + "Image.zip")

                        for file in os.listdir(path + '.'):
                                if file.endswith('.bmp'):
                                    print(path + file)
                                    os.remove(path + file)
                                        
                        print(' [system] Successfully removed old zip and bmp!')
                        
                        print(' [system] saving new zip file')
                        with open(path + 'Image.zip', 'wb') as f:
                            timetable_response.raw.decode_content = True
                            f.write(timetable_response.content) #writing Image.zip
                            f.close()

                        print(' [system] unzipping file')
                        subprocess.check_call(["unzip", path + "Image.zip", "-d", path], stdout=DEVNULL, stderr=STDOUT)

                        for file in os.listdir(path + '.'):
                                if file.endswith('.bmp') or file.endswith('.BMP'):
                                        print(' [system] renaming ' + file + ' to Image.bmp')
                                        os.rename( path +file, path + 'Image.bmp')
                                        break

                        print(' [ePaper] refreshing ePaper')
                        
                        subprocess.check_call(["/bin/IT8951/IT8951", "0", "0", path + "Image.bmp"], stdout=DEVNULL, stderr=STDOUT)
                        print(' [ePaper] successfully refreshed')
                        
                        print()
                        time.sleep(30)
                else:
                        print(' [RETURN CODE 403] Access denied, admin must authorize this device MAC: ', mac);
                        authentication_request = requests.post("%s/register"%(url), data={"macAdd": mac}, verify=False)

                        print()
                        time.sleep(30)
        except Exception as e:
                print("[ERROR]")
                print(e)
               
                #with open("/root/ePaperScript.log") as f:
                #    f.write(str(e))
    
                traceback.print_exc(file=log)

                print()
                time.sleep(30)
#thats the last test