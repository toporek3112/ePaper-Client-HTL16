from uuid import getnode as get_mac
import time, socket, socket, requests, shutil, uuid, json, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://10.0.0.16:4000/ePaper/database/'

################################################################################
# Methodes
################################################################################

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

mac = get_mac()
mac = '-'.join(("%012X" % mac)[i : i + 2] for i in range(0, 12, 2))

################################################################################
# Code
################################################################################


while True:
        # timetable_response = requests.get("%s/timetable/%s"%(url, getMac()), stream=True, verify=False)
        timetable_response = requests.get(url+"timetable/:"+mac, stream=True, verify=False)

        # print(url+"timetable/:"+getMac())
        try:
                json_timetable_response = json.loads(timetable_response.text)
        except:
                print("wtf")
        if json_timetable_response['message'] != "not registered":
                with open('./Timetable.bmp', 'wb') as f:
                        timetable_response.raw.decode_content = True
                        f.write(timetable_response.content)
                        print('successfully updated Timetable ')
                        # time.sleep(900)
                        time.sleep(60)
        else:
                print('getting Timetable failed ')
                authentication_request = requests.post("%s/authenticate"%(url), data={"macAdd": mac, "ipAdd": IPAddr}, verify=False)
                print('authentication ')
                
                # time.sleep(120)
                time.sleep(30)