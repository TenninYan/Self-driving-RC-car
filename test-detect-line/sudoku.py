import cv2
import numpy as np

img = cv2.imread('line1.jpg')
img2 = cv2.imread('line1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imwrite("canny.jpg",edges)
#
test1 = cv2.Laplacian(gray,cv2.CV_16S,ksize=3,scale=1,delta=50)
cv2.imwrite("laplacian.jpg",test1)


lines = cv2.HoughLines(edges,1,np.pi/180,200)
# lines2 = cv2.HoughLines(test1,1,np.pi/180,200)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
# for rho,theta in lines2[0]:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))
#
#     cv2.line(img2,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines1.jpg',img)
# cv2.imwrite('houghlines2.jpg',img2)
