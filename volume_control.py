import cv2
import time
import numpy as np
import handRecog as hr
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
 
################################
################################
 
cap = cv2.VideoCapture(0)
 
detector = hr.handDetector(detectionConfi=0.8, maxHands=1, trackConfi=0.7)
 
######## 
#  Audio Control
########

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]
vol = 0

while True:
    s, img = cap.read()
    img = detector.findHands(img)
    landmarkList = detector.findHandPosition(img, draw=False)
    if len(landmarkList) != 0:

 
        x1, y1 = landmarkList[4][1], landmarkList[4][2]
        x2, y2 = landmarkList[8][1], landmarkList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        cv2.circle(img, (x1, y1), 12, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 12, (255, 200, 255), cv2.FILLED)
 
        length = math.hypot(x2 - x1, y2 - y1)
 
        vol = np.interp(length, [35, 260], [minVol, maxVol])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
 
        if length < 35:
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)
        
        time.sleep(0.2)
 
    cv2.imshow("Img", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break