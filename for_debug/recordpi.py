# coding: UTF-8
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
 
import numpy as np
import cv2
import urllib

stream=urllib.urlopen('http://tenypi.local:8080/?action=stream')
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.cv.CV_FOURCC('i','Y','U', 'V')
fourcc = cv2.cv.CV_FOURCC('m','p','4', 'v')
out = cv2.VideoWriter('drift9.avi',fourcc,5,(640,480))
bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        out.write(i)
        #out = cv2.resize(i,(0,0),fx=4,fy=4)
        cv2.imshow('result',i)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # cv2.imwrite('line2.jpg',out)
            break
out.release()
cv2.destroyAllWindows()
