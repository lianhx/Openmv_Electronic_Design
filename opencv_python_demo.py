# -*- coding: utf-8 -*-
import cv2 as cv
from struct import pack

buf_x=[0,0,0]
buf_y=[0,0,0]
frame_time=100 * 0.02

def find_rect_and_ball(src,gray):
    u_flag = 1;d_flag = 1;l_flag = 1;r_flag = 1
    rect=[0,0,0,0]
    ret,thresh=cv.threshold(gray,100,255,cv.THRESH_BINARY)
    cv.imshow("gray", thresh)
    height = gray.shape[0];width = gray.shape[1]
    
    for row in range(int(0.5*height),0,-1):
        col = int(0.45*width)
        pv = thresh[row, col]
        if((pv>150)&(u_flag)):u_flag=0;rect[1]=row;cv.circle(src,(col,row),3,(0,0,213),-1)
            
    for row in range(int(0.5*height),height):
        col = int(0.55*width)
        pv = thresh[row, col]
        if((pv>150)&(d_flag)):d_flag=0;rect[3]=row;cv.circle(src,(col,row),3,(0,0,213),-1)
        
    for col in range(int(0.5*width),0,-1):
        row = int(0.45*height)
        pv = thresh[row, col]
        if((pv>150)&(l_flag)):l_flag=0;rect[0]=col;cv.circle(src,(col,row),3,(0,0,213),-1)
            
    for col in range(int(0.5*width),width):
        row = int(0.55*height)
        pv = thresh[row, col]
        if((pv>150)&(r_flag)):r_flag=0;rect[2]=col;cv.circle(src,(col,row),3,(0,0,213),-1)
    locate = [0,0]
    t_locate = [0,0]
    count = 0
    if(rect[2]-rect[0]<0.2*width):rect=[int(0.1*width),int(0.1*height),int(0.9*width),int(0.9*height)]
    if(rect[3]-rect[1]<0.2*height):rect=[int(0.1*width),int(0.1*height),int(0.9*width),int(0.9*height)]
    for col in range(rect[0]+15,rect[2]-15,2):
        for row in range(rect[1]+15,rect[3]-15,2):
            pv1 = [thresh[row-1, col-1],thresh[row-1, col],thresh[row-1, col+1]]
            pv2 = [thresh[row  , col-1],thresh[row  , col],thresh[row  , col+1]]
            pv3 = [thresh[row+1, col-1],thresh[row+1, col],thresh[row+1, col+1]]
            aver =  (int(pv1[0])+int(pv1[1])+int(pv1[2]))/9
            aver += (int(pv2[0])+int(pv2[1])+int(pv2[2]))/9
            aver += (int(pv3[0])+int(pv3[1])+int(pv3[2]))/9
            if(aver > 150):
                locate[0] += col
                locate[1] += row
                count = count + 1
    if(count > 0):
        locate[0]=int(locate[0]/count)
        locate[1]=int(locate[1]/count)
    cv.rectangle(src, (rect[0],rect[1]), (rect[2],rect[3]), (255,0,0),3)
    cv.circle(src,(locate[0],locate[1]),3,(0,0,233),-1)
    if(rect[2]-rect[0]<0.2*width):rect=[int(0.1*width),int(0.1*height),int(0.9*width),int(0.9*height)]
    if(rect[3]-rect[1]<0.2*height):rect=[int(0.1*width),int(0.1*height),int(0.9*width),int(0.9*height)]
    t_locate[0]=int(650*((locate[0]-rect[0])/(rect[2]-rect[0])))
    t_locate[1]=int(650*((locate[1]-rect[1])/(rect[3]-rect[1])))
    return t_locate

video_ = cv.VideoCapture("test.mp4")
while(1):
    ret, image = video_.read()
    if cv.waitKey(1) & 0xFF == ord('q'):break
    GrayImage=cv.cvtColor(image,cv.COLOR_BGR2GRAY)   
    located = find_rect_and_ball(image,GrayImage)#通过这个函数获得小球坐标  
    buf_x[0] = located[0]#x坐标
    buf_y[0] = located[1]#y坐标  
    speed_now_x=(buf_x[0]-buf_x[1])/frame_time
    speed_now_y=(buf_y[0]-buf_y[1])/frame_time
    speed_last_x=(buf_x[1]-buf_x[2])/frame_time
    speed_last_y=(buf_y[1]-buf_y[2])/frame_time
    a_speed_x=(speed_now_x-speed_last_x)/frame_time
    a_speed_y=(speed_now_y-speed_last_y)/frame_time  
    print("x ",located[0]);print("y ",located[1])
    print("x 速度：",speed_now_x);print("y 速度：",speed_now_y)
    print("x 加速度：",a_speed_x);print("y 加速度：",a_speed_y)
    #datap = pack('BBBBHHHHHH',0x35,0x46,0x57,0x24,buf_x[0],buf_y[0],int(speed_now_x),int(speed_now_y),int(a_speed_x),int(a_speed_y))
    #print('you send:',datap)
    cv.imshow("image", image)
cv.destroyAllWindows()
