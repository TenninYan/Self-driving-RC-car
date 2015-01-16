# coding: UTF-8

#use usb camera connected to Rasbpery Pi to detect american stop sign
#used mjpeg-streamer in Rasbery Pi
#used cascade in this site http://www.cs.utah.edu/~turcsans/DUC/

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
 
import numpy as np
import cv2
import urllib
import socket
import sys


cascade_path = "cascade/haarcascade_stop.xml"

color = (255, 255, 255) #白

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

stream=urllib.urlopen('http://tenypi.local:8080/?action=stream')
bytes=''

A=np.array([0,0,0,0,0])
num = 0
state = "go"

TCP_IP = 'tenyPi.local'
TCP_PORT = 5005
BUFFER_SIZE = 1024
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))


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
            # np.array[num%5]=1
            A[num%5]=1
            # print "stop_sign find"
            #検出した顔を囲む矩形の作成
            for rect in facerect:
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
        else:
            # array[num%5]=0
            A[num%5]=0


        # 画像を画面に出力する
        cv2.imshow('frame',frame)
        num += 1

        if np.sum(A)>4 and state=="go":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            MESSAGE = "stop"
            s.send(MESSAGE)
            state="stop"
            print "stop message send!!"
        elif np.sum(A)<1 and state=="stop":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            MESSAGE = "go"
            s.send(MESSAGE)
            state="go"
            print "go message send!!"

    # "q"が押されたら抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 後始末
cap.release()
out.release()
cv2.destroyAllWindows()
