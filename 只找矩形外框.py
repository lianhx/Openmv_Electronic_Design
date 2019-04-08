import sensor, image, time
from pyb import UART
from struct import pack

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.HQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

thresholds = [(185, 255)] # grayscale thresholds设置阈值
buf_x=[0,0,0]
buf_y=[0,0,0]
frame_time=0.05

def find_rect(thresh):
    u_flag = 1;d_flag = 1;l_flag = 1;r_flag = 1
    height = thresh.height();width = thresh.width()
    rect=[int(0.2*width),int(0.1*height),int(0.8*width),int(0.9*height)]
    for row in range(int(0.5*height),0,-2):
        col = int(0.5*width)
        pv = thresh.get_pixel(col,row)
        if((pv>150)&(u_flag)):u_flag=0;rect[1]=row
    for row in range(int(0.5*height),height,2):
        col = int(0.5*width)
        pv = thresh.get_pixel(col,row)
        if((pv>150)&(d_flag)):d_flag=0;rect[3]=row
    for col in range(int(0.5*width),0,-2):
        row = int(0.5*height)
        pv = thresh.get_pixel(col,row)
        if((pv>150)&(l_flag)):l_flag=0;rect[0]=col
    for col in range(int(0.5*width),width,2):
        row = int(0.5*height)
        pv = thresh.get_pixel(col,row)
        if((pv>150)&(r_flag)):r_flag=0;rect[2]=col
    if(rect[2]-rect[0]<0.5*width):rect=[int(0.2*width),int(0.1*height),int(0.8*width),int(0.9*height)]
    if(rect[3]-rect[1]<0.5*height):rect=[int(0.2*width),int(0.1*height),int(0.8*width),int(0.9*height)]
    thresh.draw_rectangle(rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])


def move_():
    buf_x[2]=buf_x[1]
    buf_x[1]=buf_x[0]
    buf_y[2]=buf_y[1]
    buf_y[1]=buf_y[0]

uart = UART(3, 115200)
while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    img.binary(thresholds)
    located = find_rect(img)





    move_()
    buf_x[0] = 0
    buf_y[0] = 0

    speed_now_x=(buf_x[0]-buf_x[1])/frame_time
    speed_now_y=(buf_y[0]-buf_y[1])/frame_time
    speed_last_x=(buf_x[1]-buf_x[2])/frame_time
    speed_last_y=(buf_y[1]-buf_y[2])/frame_time
    a_speed_x=(speed_now_x-speed_last_x)/frame_time
    a_speed_y=(speed_now_y-speed_last_y)/frame_time

    datap = pack('bbbbhhhhhh',0x35,0x46,0x57,0x24,buf_x[0],buf_y[0],int(speed_now_x),int(speed_now_y),int(a_speed_x),int(a_speed_y))
    uart.write(datap)
    print("FPS %f" % clock.fps())
    frame_time = 1/clock.fps()
