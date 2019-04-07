# -*- coding: utf-8 -*-
import cv2 as cv
def find_rect(src,gray):
    up_flag = 1
    down_flag = 1
    left_flag = 1
    right_flag = 1
    rect=[0,0,0,0]
    ret,thresh=cv.threshold(gray,100,255,cv.THRESH_BINARY)
    height = gray.shape[0]
    width = gray.shape[1]
    
    for row in range(int(0.5*height),0,-1):
        col = int(0.5*width)
        pv = thresh[row, col]
        if((pv>150)&(up_flag)):
            up_flag=0
            rect[1]=row
            cv.circle(src,(col,row),3,(0,0,213),-1)
            
    for row in range(int(0.5*height),height):
        col = int(0.5*width)
        pv = thresh[row, col]
        if((pv>150)&(down_flag)):
            down_flag=0
            rect[3]=row
            cv.circle(src,(col,row),3,(0,0,213),-1)
        
    for col in range(int(0.5*width),0,-1):
        row = int(0.5*height)
        pv = thresh[row, col]
        if((pv>150)&(left_flag)):
            left_flag=0
            rect[0]=col
            cv.circle(src,(col,row),3,(0,0,213),-1)
            
    for col in range(int(0.5*width),width):
        row = int(0.5*height)
        pv = thresh[row, col]
        if((pv>150)&(right_flag)):
            right_flag=0
            rect[2]=col
            cv.circle(src,(col,row),3,(0,0,213),-1)
    for col in range(rect[0]+5,rect[2]-5,2):
        for row in range(rect[1]+5,rect[3]-5,2):
            pv1 = [thresh[row-1, col-1],thresh[row-1, col],thresh[row-1, col+1]]
            pv2 = [thresh[row  , col-1],thresh[row  , col],thresh[row  , col+1]]
            pv3 = [thresh[row+1, col-1],thresh[row+1, col],thresh[row+1, col+1]]
            aver =  (int(pv1[0])+int(pv1[1])+int(pv1[2]))/9
            aver += (int(pv2[0])+int(pv2[1])+int(pv2[2]))/9
            aver += (int(pv3[0])+int(pv3[1])+int(pv3[2]))/9
            if(aver > 240):
                cv.circle(src,(col,row),3,(0,0,213),-1)
        cv.rectangle(src, (rect[0],rect[1]), (rect[2],rect[3]), (255,0,0),3)
    cv.imshow("bin", thresh)
    cv.imshow("src", src)
    
    
image = cv.imread("demo.jpg")
GrayImage=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
find_rect(image,GrayImage)


cv.waitKey(0)
cv.destroyAllWindows()
