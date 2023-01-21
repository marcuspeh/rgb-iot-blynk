import requests
from RequestException import RequestException
from static import RED_PIN, GREEN_PIN, BLUE_PIN
from static import POWER_PIN, POWER_OFF, POWER_ON
from static import MODE_PIN, MODE_MUSIC, MODE_RGB


######################## Update info #####################################


def deviceStatus(auth):
    url = f"https://blynk.cloud/external/api/isHardwareConnected?token={auth}"
    res = requests.get(url)
    
    if res.status_code == 400:
        raise RequestException(res.json()["error"]["message"])

    return res.json()


def updateStream(auth, pin, value):
    url = f"https://blynk.cloud/external/api/update?token={auth}&{pin}={value}"
    res = requests.get(url)
    
    if res.status_code == 400:
        raise RequestException(res.json()["error"]["message"])


def sendColor(auth, color):
    url = f"https://blynk.cloud/external/api/update?token={auth}&{RED_PIN}={color.red}&{GREEN_PIN}={color.green}&{BLUE_PIN}={color.blue}"
    res = requests.get(url)
    
    if res.status_code == 400:
        raise RequestException(res.json()["error"]["message"])


######################## Get info #####################################


def getPowerStatus(auth):
    url = f"https://blynk.cloud/external/api/get?token={auth}&{POWER_PIN}"
    res = requests.get(url)
    
    if res.status_code == 400:
        raise RequestException(res.json()["error"]["message"])

    return res.json()

def getModeStatus(auth):
    url = f"https://blynk.cloud/external/api/get?token={auth}&{MODE_PIN}"
    res = requests.get(url)
    
    if res.status_code == 400:
        raise RequestException(res.json()["error"]["message"])

    return res.json()