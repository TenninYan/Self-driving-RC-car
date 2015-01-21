#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys
import urllib
import socket

stream=urllib.urlopen('http://tenypi.local:8080/?action=stream')
# stream2 = cv2.VideoCapture(0)
# hight = stream2.shape[0]
# width = stream2.shape[1]
# stream = cv2.resize(stream2,(0,0))

#canny filter parameter
p1 = 60
p2 = 120

#HoughLines parameter
thresh = 5
minLineLength = 30
maxLineGap = 3


A=np.array([0,0,0,0,0])
num = 0
state = "stop"

TCP_IP = 'tenyPi.local'
TCP_PORT = 5005
BUFFER_SIZE = 1024


MID = 90

bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame_temp = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

        frame = cv2.medianBlur(frame_temp,11)

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,p1,p2,apertureSize = 3)

        # edges = cv2.medianBlur(edges_temp,5)


        canny_out = cv2.resize(edges,(0,0),fx=4,fy=4)
        cv2.imshow("canny",canny_out)

        #cv2.HoughLinesP(ソース、何ピクセルごとに読むか、何度ごとに見るか、閾値、ラインの長さ、1本の線と認識する最大の差)
        lines = cv2.HoughLinesP(edges,1,np.pi/180,thresh,minLineLength,maxLineGap)

        # if not any(lines):
        # if lines.any()==False:
        # if not lines:
        if lines==None:
            # print "no lines"
            # sys.exit()
            out = cv2.resize(frame,(0,0),fx=4,fy=4)
            cv2.imshow('result',out)
            continue
        else:
            lines_num = 0
            sum_of_degree = 0
            for x1,y1,x2,y2 in lines[0]:
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                # print  x1,y1,x2,y2 

                a=(np.arctan2(y1-y2,x2-x1))/np.pi*180
                if a<0:
                    a+=180
                # print "%f degree"%(a)

                if y1 > 100 and y2 > 100:
                    continue
                if a < 10 or a> 170:
                    continue
                else:
                    lines_num += 1
                    sum_of_degree += a
            A[num%5] = float(sum_of_degree) / lines_num
            num += 1

        if num > 4 and num%5 == 0:
            A_avr = np.average(A) 
            print A_avr
            if MID - 10 < A_avr and  A_avr < MID + 10:
                MESSAGE = "go"
            elif MID - 30 < A_avr and  A_avr< MID - 10:
                MESSAGE = "r1"
            elif MID + 10 < A_avr and  A_avr< MID + 30:
                MESSAGE = "l1"
            else:
                MESSAGE = "else"


            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(MESSAGE)
            state=MESSAGE
            print "%s message send!!"%(MESSAGE)
            





        out = cv2.resize(frame,(0,0),fx=4,fy=4)
        cv2.imshow('result',out)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('q'):
            cv2.imwrite('houghlines_x.jpg',frame)
            cv2.imwrite('canny_x.jpg',edges)
            cv2.destroyAllWindows()
            sys.exit()

        # elif k == ord('w'):
        #     p1 += 3
        #     print p1,p2
        #
        # elif k == ord('s'):
        #     p1 -= 3
        #     print p1,p2
        # elif k == ord('e'):
        #     p2 += 3
        #     print p1,p2
        # elif k == ord('d'):
        #     p2 -= 3
        #     print p1,p2


        # elif k == ord('r'):
        #     thresh += 3
        #     print thresh,minLineLength,maxLineGap
        # elif k == ord('f'):
        #     thresh -= 3
        #     print thresh,minLineLength,maxLineGap
        # elif k == ord('t'):
        #     minLineLength += 10
        #     print thresh,minLineLength,maxLineGap
        # elif k == ord('g'):
        #     minLineLength -= 10
        #     print thresh,minLineLength,maxLineGap
        # elif k == ord('y'):
        #     maxLineGap += 1
        #     print thresh,minLineLength,maxLineGap
        # elif k == ord('h'):
        #     maxLineGap -= 1
        #     print thresh,minLineLength,maxLineGap

        # cv2.imshow('i',frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     out = cv2.resize(i,(0,0),fx=4,fy=4)
        #     cv2.imwrite('line2.jpg',out)
        #     exit(0)


