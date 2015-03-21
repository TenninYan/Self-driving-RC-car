# coding: UTF-8

#use usb camera connected to Rasbpery Pi to detect american stop sign
#used mjpeg-streamer in Rasbery Pi
#used cascade in this site http://www.cs.utah.edu/~turcsans/DUC/

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
 
import numpy as np
import cv2
import urllib


cascade_path = "cascade/haarcascade_stop.xml"

color = (255, 255, 255) #白

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

cap =cv2.VideoCapture("movie/drift9.avi")

fourcc = cv2.cv.CV_FOURCC('m','p','4', 'v')
out = cv2.VideoWriter('drift9-3.avi',fourcc,5,(640,480))

while (cap.isOpened()):
    # frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
    ret,frame = cap.read()
    
    tmp1 = cv2.resize(frame,(0,0),fx=0.5,fy=0.5)

    if ret == False:
        continue


    #グレースケール変換
    image_gray = cv2.cvtColor(tmp1, cv2.cv.CV_BGR2GRAY)

    #物体認識（顔認識）の実行
    #facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
    #facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

    #parameter tuned
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(facerect) > 0:
        #検出した顔を囲む矩形の作成
        for rect in facerect:
            cv2.rectangle(tmp1, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)

    # 画像を画面に出力する
    tmp2 = cv2.resize(tmp1,(0,0),fx=2,fy=2)
    cv2.imshow('frame',tmp2)
    out.write(tmp2)

    # "q"が押されたら抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 後始末
cap.release()
out.release()
cv2.destroyAllWindows()
