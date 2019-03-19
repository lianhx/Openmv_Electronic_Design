# -*- coding: utf-8 -*-

buf_x=[0,0,0]
buf_y=[0,0,0]
index=0
frame_time=0.12
def move_(index):
    temp_x=buf_x[2]
    buf_x[2]=buf_x[1]
    buf_x[1]=buf_x[0]
    buf_x[0]=temp_x
    temp_y=buf_y[2]
    buf_y[2]=buf_y[1]
    buf_y[1]=buf_y[0]
    buf_y[0]=temp_y
    

while(True):
    x=int(input())
    if(x==6666):break
    y=int(input())
    move_(index)
    buf_x[0]=x
    buf_y[0]=y
    index=index+1
    if(index>2):index=0
    print(buf_x,buf_y)
    speed_now_x=(buf_x[0]-buf_x[1])/frame_time
    speed_now_y=(buf_x[0]-buf_x[1])/frame_time
    speed_last_x=(buf_x[1]-buf_x[2])/frame_time
    speed_last_y=(buf_x[1]-buf_x[2])/frame_time
    a_speed_x=(speed_now_x-speed_last_x)/frame_time
    a_speed_y=(speed_now_y-speed_last_y)/frame_time
    print("速度：",speed_now_x)
    print("加速度：",a_speed_x)
