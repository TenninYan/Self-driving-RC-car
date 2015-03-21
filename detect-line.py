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

#parameter of line degree
degree1 = 25
degree2 = 35
degree3 = 45
degree4 = 70

#canny filter parameter
# p1 =60
# p2 = 130

p1= 40
p2 = 70

#HoughLines parameter
thresh = 3
minLineLength = 50
maxLineGap = 3


A=np.array([0,0])
num = 0
state = "init"

TCP_IP = 'tenyPi.local'
TCP_PORT = 5006
BUFFER_SIZE = 1024


MID = 90


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

fourcc = cv2.cv.CV_FOURCC('m','p','4', 'v')
# rec = cv2.VideoWriter('line2_4.avi',fourcc,5,(640,480))
rec = cv2.VideoWriter('line2_7.avi',fourcc,5,(160,120))

font = cv2.FONT_HERSHEY_PLAIN

MESSAGE = "start"

# x_grav = 90
# y_grav = 60
# x_grav2 = 90
# y_grav2 = 60

bytes=''
while True:
    # grav = []
    # grav2 = []
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

        # canny_out = cv2.resize(edges,(0,0),fx=4,fy=4)
        cv2.imshow("canny",edges)

        #cv2.HoughLinesP(ソース、何ピクセルごとに読むか、何度ごとに見るか、閾値、ラインの長さ、1本の線と認識する最大の差)
        lines = cv2.HoughLinesP(edges,1,np.pi/180,thresh,minLineLength,maxLineGap)

        #線分がなければ表示のみ
        if lines==None:
            # print "no lines"
            # sys.exit()
            continue
        #線分があれば描画して表示
        else:
            lines_num = 0
            grav2_num = 0
            sum_of_degree = 0
            for x1,y1,x2,y2 in lines[0]:
                #cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                # print  x1,y1,x2,y2 

                a=(np.arctan2(y1-y2,x2-x1))/np.pi*180
                if a==0:
                    continue
                elif a<0:
                    a+=180
                # print "%f degree"%(a)

                #画像の上下の線分と水平な線分を除去
                if y1  < 35 and y2 < 35:
                    # temp = [(x1+x2)/2,(y1+y2)/2]
                    # grav2.append(temp) 
                    # grav2_num +=1


                    continue
                elif y1 > 90 and y2 > 90:
                    continue
                elif a < 10 or a> 170:
                    continue
                else:
                    # temp = [(x1+x2)/2,(y1+y2)/2]
                    # grav.append(temp) 
                    cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                    lines_num += 1
                    sum_of_degree += a
            if lines_num == 0:
                continue
            else:
                A[num%2] = float(sum_of_degree) / lines_num
                # x_sum = 0
                # y_sum = 0
                # for mid in range(0,lines_num):
                #     x_sum += grav[mid][0]
                #     y_sum += grav[mid][1] 
                # x_grav = x_sum/lines_num
                # y_grav = y_sum/lines_num
                # print x_sum/lines_num ,y_sum/lines_num
                num += 1
            # if grav2_num == 0:
            #     continue
            # else:
            #     x_sum = 0
            #     y_sum = 0
            #     for mid in range(0,grav2_num):
            #         x_sum += grav2[mid][0]
            #         y_sum += grav2[mid][1] 
            #     x_grav2 = x_sum/grav2_num
            #     y_grav2 = y_sum/grav2_num


        if num > 4 and num%2 == 0:
            A_avr = np.average(A) 
            # print "%f degress"%(A_avr)
            # if x_grav2 < 30:
            #     MESSAGE = "l2"
            #     print "grav2"
            #     print x_grav2
            # elif x_grav2 > 130:
            #     MESSAGE = "r2"
            #     print "grav2"
            #     print x_grav2
            # if x_grav < 30:
            #     MESSAGE = "l3"
            #     print x_grav
            # elif x_grav > 130:
            #     MESSAGE = "r3"
            #     print x_grav

            if MID - degree1 < A_avr and  A_avr < MID + degree1:
                MESSAGE = "go"

            elif MID - degree2 < A_avr and  A_avr< MID - degree1:
                MESSAGE = "r1"
            elif MID -  degree3< A_avr and  A_avr< MID - degree2:
                MESSAGE = "r2"
            elif MID -  degree4< A_avr and  A_avr< MID - degree3:
                MESSAGE = "r3"

            elif MID +  degree1< A_avr and  A_avr< MID + degree2:
                MESSAGE = "l1"
            elif MID +  degree2< A_avr and  A_avr< MID + degree3:
                MESSAGE = "l2"
            elif MID +  degree3< A_avr and  A_avr< MID + degree4:
                MESSAGE = "l3"

            else:
                MESSAGE = "else"


            s.send(MESSAGE)
            state=MESSAGE
            print "%s message send!!"%(MESSAGE)


        # out = cv2.resize(frame,(0,0),fx=4,fy=4)
        cv2.putText(frame,MESSAGE,(30,40),font,3.0,(0,0,0))
        cv2.imshow('result',frame)
        rec.write(frame)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('a'):
            cv2.imwrite('houghlines_x.jpg',frame)
            cv2.imwrite('canny_x.jpg',edges)
            cv2.destroyAllWindows()
            sys.exit()
        elif k == ord('q'):
            cv2.imwrite('houghlines_x.jpg',frame)
            cv2.imwrite('canny_x.jpg',edges)
            cv2.destroyAllWindows()
            MESSAGE = "exit"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(MESSAGE)
            state=MESSAGE
            print "%s message send!!"%(MESSAGE)
            sys.exit()

        elif k == ord('w'):
            p1 += 10
            print p1,p2

        elif k == ord('s'):
            p1 -= 10
            print p1,p2
        elif k == ord('e'):
            p2 += 10
            print p1,p2
        elif k == ord('d'):
            p2 -= 10
            print p1,p2


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


