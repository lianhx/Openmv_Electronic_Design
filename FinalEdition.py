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

thresholds = [(210, 255)] # grayscale thresholds设置阈值
buf_x=[0,0,0]
buf_y=[0,0,0]
frame_time=0.10

def find_rect_and_ball(thresh):
    u_flag = 1;d_flag = 1;l_flag = 1;r_flag = 1
    rect=[0,0,0,0]
    height = thresh.height();width = thresh.width() 
    for row in range(int(0.5*height),0,-1):
        col = int(0.5*width)
        pv = thresh.get_pixel(col,row)
        if((pv>150)&(u_flag)):u_flag=0;rect[1]=row   
    for row in range(int(0.5*height),height):
        col = int(0.5*width)
        pv = thresh.get_pixel(col,row)
        if((pv>150)&(d_flag)):d_flag=0;rect[3]=row
    for col in range(int(0.5*width),0,-1):
        row = int(0.5*height)
        pv = thresh.get_pixel(col,row)
        if((pv>150)&(l_flag)):l_flag=0;rect[0]=col
    for col in range(int(0.5*width),width):
        row = int(0.5*height)
        pv = thresh.get_pixel(col,row)
        if((pv>150)&(r_flag)):r_flag=0;rect[2]=col
    locate = [0,0]
    t_locate = [0,0]
    count = 0
    for col in range(rect[0]+5,rect[2]-5,2):
        for row in range(rect[1]+5,rect[3]-5,2):
            pv1 = [thresh[row-1, col-1],thresh[row-1, col],thresh[row-1, col+1]]
            pv2 = [thresh[row  , col-1],thresh[row  , col],thresh[row  , col+1]]
            pv3 = [thresh[row+1, col-1],thresh[row+1, col],thresh[row+1, col+1]]
            aver =  (int(pv1[0])+int(pv1[1])+int(pv1[2]))/9
            aver += (int(pv2[0])+int(pv2[1])+int(pv2[2]))/9
            aver += (int(pv3[0])+int(pv3[1])+int(pv3[2]))/9
            if(aver > 240):
                locate[0] += col
                locate[1] += row
                count = count + 1
    if(count > 0):
        locate[0]=int(locate[0]/count)
        locate[1]=int(locate[1]/count)    
    thresh.draw_rectangle(rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])
    thresh.draw_circle(locate[0], locate[1], 2)
    t_locate[0]=int(650*((locate[0]-rect[0])/(rect[2]-rect[0])))
    t_locate[1]=int(650*((locate[1]-rect[1])/(rect[3]-rect[1])))
    return t_locate

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
    located = find_rect_and_ball(img)
    move_()
    buf_x[0] = located[0]
    buf_y[0] = located[1]

    speed_now_x=(buf_x[0]-buf_x[1])/frame_time
    speed_now_y=(buf_y[0]-buf_y[1])/frame_time
    speed_last_x=(buf_x[1]-buf_x[2])/frame_time
    speed_last_y=(buf_y[1]-buf_y[2])/frame_time
    a_speed_x=(speed_now_x-speed_last_x)/frame_time
    a_speed_y=(speed_now_y-speed_last_y)/frame_time

    print("x 速度：",speed_now_x)
    print("x 加速度：",a_speed_x)

    datap = pack('BBBBHHHHHH',0x35,0x46,0x57,0x24,buf_x[0],buf_y[0],int(speed_now_x),int(speed_now_y),int(a_speed_x),int(a_speed_y))
    print('you send:',datap)
    uart.write(datap)
    print("FPS %f" % clock.fps())
