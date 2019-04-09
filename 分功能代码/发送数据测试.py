import sensor, image, time, pyb
from pyb import UART
from struct import pack
sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_whitebal(False)
clock = time.clock() # 追踪帧率

blob_thresholds=((85, 100, -12, 12, -12, 12))#白色
thresholds = [(160, 255)] # grayscale thresholds设置阈值

find_once = 0
s_rect = [10,10,300,220]

buf_x=[0,0,0]
buf_y=[0,0,0]
frame_time=0.01

uart = UART(3, 115200)

while(True):
    clock.tick()

    #buf_x[0] = int((b[5] - 160) * 600 / 230)
    #[0] = int((b[6] - 120) * 600 /230)

    buf_x[0] = -150
    buf_y[0] = -560
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
    #print(clock.fps())

