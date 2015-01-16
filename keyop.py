#use usb camera connected to Rasbpery Pi to detect american stop sign
#used mjpeg-streamer in Rasbery Pi
#used cascade in this site http://www.cs.utah.edu/~turcsans/DUC/


# coding: UTF-8
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
 
import numpy as np
import cv2
import urllib
import time

import commands

check = os.system("ssh pi@tenyPi.local")

if check==0:
    print "unable to connect to tenyPi"
    sys.exit()
else:
    print "connection succeed!"

sleep(5)

check = os.system("cd mjpeg-streamer")

if check==0:
    print "unable to go to mjpeg-streamer directory"
    sys.exit()

sleep(1)

 check = os.system("./mjpeg-streamer ") 

if check==0:
    print "unable to start mjpeg-streamer"
    sys.exit()
else:
    print "mjpeg-streamer started"


#HAAR分類器の顔検出用の特徴量
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml"

cascade_path = "cascade/haarcascade_stop.xml"

color = (255, 255, 255) #白

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

#teny-Nexus7用
#stream=urllib.urlopen('http://192.168.43.101:8080/?action=stream')
#TP-LINK用
stream=urllib.urlopen('http://192.168.3.7:8080/?action=stream')
bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

        #グレースケール変換
        image_gray = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)

        #物体認識（顔認識）の実行
        #facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
        #facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        
        #parameter tuned
        facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(facerect) > 0:
            #検出した顔を囲む矩形の作成
            for rect in facerect:
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)

        # 画像を画面に出力する
        cv2.imshow('frame',frame)

    # "q"が押されたら抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 後始末
cap.release()
out.release()
cv2.destroyAllWindows()
