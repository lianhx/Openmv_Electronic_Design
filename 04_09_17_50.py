import sensor, image, time, pyb
from pyb import UART
from struct import pack
sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_whitebal(False)
clock = time.clock() # 追踪帧率

buf_x=[0,0,0]
buf_y=[0,0,0]
frame_time=0.01

uart = UART(3, 115200)

blob_thresholds=((85, 100, -12, 12, -12, 12))#白色
thresholds = [(160, 255)] # grayscale thresholds设置阈值

find_once = 0
search_rect = [5,5,310,230]
def find_rect():
    if(find_once < 20):
        sensor.set_pixformat(sensor.GRAYSCALE)
        thresh = sensor.snapshot().lens_corr(1.8)
        thresh.binary(thresholds)
        u_flag = 1;d_flag = 1;l_flag = 1;r_flag = 1
        height = thresh.height();width = thresh.width()
        rect=[int(0.2*width),int(0.1*height),int(0.8*width),int(0.9*height)]
        for row in range(int(0.5*height),0,-2):
            col = int(0.5*width)
            pv = thresh.get_pixel(col,row)
            if((pv>150)&(u_flag)):u_flag=0;rect[1]=row
            if(u_flag==1):rect[1]=5
        for row in range(int(0.5*height),height,2):
            col = int(0.5*width)
            pv = thresh.get_pixel(col,row)
            if((pv>150)&(d_flag)):d_flag=0;rect[3]=row
            if(d_flag==1):rect[3]=height-5
        for col in range(int(0.5*width),0,-2):
            row = int(0.5*height)
            pv = thresh.get_pixel(col,row)
            if((pv>150)&(l_flag)):l_flag=0;rect[0]=col
            if(l_flag==1):rect[0]=5
        for col in range(int(0.5*width),width,2):
            row = int(0.5*height)
            pv = thresh.get_pixel(col,row)
            if((pv>150)&(r_flag)):r_flag=0;rect[2]=col
            if(r_flag==1):rect[3]=width-5
        if(rect[2]-rect[0]<0.5*width):rect=[int(0.1*width),int(0.05*height),int(0.9*width),int(0.95*height)]
        if(rect[3]-rect[1]<0.5*height):rect=[int(0.1*width),int(0.05*height),int(0.9*width),int(0.95*height)]
        thresh.draw_rectangle(rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])
        print(search_rect[0],search_rect[1],search_rect[2],search_rect[3])
while(True):
    clock.tick()
    if find_once < 50 :
        find_once = find_once + 1
        find_rect()
    if find_once >= 50 :
        sensor.set_pixformat(sensor.RGB565)
        img = sensor.snapshot() # 从感光芯片获得一张图像
        blobs = img.find_blobs([blob_thresholds])
        for b in blobs:
            if b.w()>2 and b.w()<15:
                if b.h()>2 and b.h()<15:
                    if b.x()>20 and b.x()<300:        #这里是筛选小球可能出现的矩形区域
                        if b.y()>20 and b.y()<220:    #这里是筛选小球可能出现的矩形区域
                            img.draw_rectangle(b[0:4],color=(0,0,255)) # rect #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy#在目标颜色区域的中心画十字形标记
                            #print ("X= %d, Y=%d" %(b[5], b[6]))
                            buf_x[0] = int((b[5]-160)*600/230)
                            buf_y[0] = int((b[6]-120)*600/230)
                            speed_now_x=(buf_x[0]-buf_x[1])/frame_time
                            speed_now_y=(buf_y[0]-buf_y[1])/frame_time
                            speed_last_x=(buf_x[1]-buf_x[2])/frame_time
                            speed_last_y=(buf_y[1]-buf_y[2])/frame_time
                            a_speed_x=(speed_now_x-speed_last_x)/frame_time
                            a_speed_y=(speed_now_y-speed_last_y)/frame_time
                            print("x 位置：",buf_x[0]);print("y 位置：",buf_y[0])
                            print("x 速度：",int(speed_now_x));print("y 速度：",int(speed_now_y))
                            print("x 加速度：",int(a_speed_x));print("y 加速度：",int(a_speed_y))
                            datap = pack('bbbbhhhhhh',0x35,0x46,0x57,0x24,buf_x[0],buf_y[0],int(speed_now_x),int(speed_now_y),int(a_speed_x),int(a_speed_y))
                            print('you send:',datap)
                            uart.write(datap)
    frame_time = clock.fps()
    print(frame_time)
