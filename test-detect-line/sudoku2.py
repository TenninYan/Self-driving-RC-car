import cv2
import numpy as np
import sys

img = cv2.imread('line2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,10,500,apertureSize = 3)
# edges = cv2.Canny(gray,10,50,apertureSize = 3)
cv2.imwrite("canny_x.jpg",edges)
# cv2.imshow('canny',edges)

# test1 = cv2.Laplacian(gray,cv2.CV_16S,ksize=3,scale=1,delta=50)
# cv2.imwrite("laplacian.jpg",test1)

minLineLength = 10000
maxLineGap = 2
lines = cv2.HoughLinesP(edges,1,np.pi/180,4,minLineLength,maxLineGap)

if not lines:
    print "no lines"
    sys.exit()
else:
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    
    while True:
        cv2.imshow('result',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('houghlinesx.jpg',img)
            cv2.destroyAllWindows()
            break
