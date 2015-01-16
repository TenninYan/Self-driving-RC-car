# coding: UTF-8
#use usb camera to get face and recognize face


import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import numpy as np
import cv2

#HAAR分類器の顔検出用の特徴量
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml"

color = (255, 255, 255) #白

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

# カメラからのキャプチャ指定
cap = cv2.VideoCapture(0)

# カメラオープン中はずっと処理する
while(cap.isOpened()):

    # キャプチャ画像を取り出す
    ret, frame = cap.read()

    # データがなければ抜ける
    if ret==False:
        break

    #グレースケール変換
    image_gray = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)

    #物体認識（顔認識）の実行
    #facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
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
