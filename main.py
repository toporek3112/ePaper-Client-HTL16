import time, socket, uuid, subprocess, requests, urllib3, zipfile, os
from subprocess import DEVNULL, STDOUT

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://127.0.0.1:4000/ePaper/database/'

################################################################################
# Methodes
################################################################################

mac_num = hex(uuid.getnode()).replace('0x', '').upper()
mac = '-'.join(mac_num[i : i + 2] for i in range(0, 11, 2))

################################################################################
# Code
################################################################################

print("Starting script...")
print()

time.sleep(10)

while True:
        try:
                timetable_response = requests.get("%s/timetable/%s"%(url, mac), stream=True, verify=False)
                
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
                        # with zipfile.ZipFile("Image.zip", "r") as zip_ref:
                        #    zip_ref.extractall()
                        #    zip_ref.close()
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