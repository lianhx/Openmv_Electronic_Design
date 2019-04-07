# -*- coding: utf-8 -*-

#import sensor, image, time
#from pyb import UART

#sensor.reset()
#sensor.set_pixformat(sensor.GRAYSCALE)
#sensor.set_framesize(sensor.HQVGA)
#sensor.skip_frames(time = 2000)
#sensor.set_auto_gain(False) # must be turned off for color tracking
#sensor.set_auto_whitebal(False) # must be turned off for color tracking
#clock = time.clock()
from struct import pack

thresholds = [(210, 255)] # grayscale thresholds设置阈值
buf_x=[256,121,32]
buf_y=[560,450,235]
frame_time=0.10

def move_():
    buf_x[2]=buf_x[1]
    buf_x[1]=buf_x[0]
    buf_y[2]=buf_y[1]
    buf_y[1]=buf_y[0]

#uart = UART(3, 115200)

#while(True):
    #clock.tick()
    #img = sensor.snapshot().lens_corr(1.8)
    #img.binary(thresholds)
    #for c in img.find_circles(threshold = 4000, x_margin = 10, y_margin = 10, r_margin = 10,
    #        r_min = 2, r_max = 10, r_step = 2):
    #    img.draw_circle(c.x(), c.y(), c.r(), color = (0, 255, 0))#识别到的圆形用圆框出来
    #    img.draw_string(c.x(), c.y(), str(c.x())+" , "+str(c.y()),color=(0,255,0))
    #    move_()
    #    buf_x[0]=c.x()
    #    buf_y[0]=c.y()
    #print(buf_x,buf_y)

speed_now_x=(buf_x[0]-buf_x[1])/frame_time
speed_now_y=(buf_y[0]-buf_y[1])/frame_time
speed_last_x=(buf_x[1]-buf_x[2])/frame_time
speed_last_y=(buf_y[1]-buf_y[2])/frame_time
a_speed_x=(speed_now_x-speed_last_x)/frame_time
a_speed_y=(speed_now_y-speed_last_y)/frame_time

datap=pack('bbbbhhhhhh',0x35,0x46,0x57,0x24,buf_x[0],buf_y[0],int(speed_now_x),int(speed_now_y),int(a_speed_x),int(a_speed_y))
print('you send:',datap)
#uart.write(datap+'\r\n')
#print("FPS %f" % clock.fps())
