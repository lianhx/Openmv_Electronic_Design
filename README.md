# Openmv_Electronic_Design
##### 上传几个往年国赛代码。。。这里注明一下来源：mengfanli / openmv_find_bool 
## 暂时不去处理边框了，初始化边框
### 在循环中不断地获取彩色帧，寻找小球，滤除边界框之外的检测结果，并发送相应的数据
### 找小球用了find_blobs()寻找色块，阈值的设定利用IDE里的工具->机器视觉->阈值选择器
```
import sensor, image, time, pyb
from pyb import UART
from struct import pack
sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) #320x240
sensor.set_auto_whitebal(False) #关闭白平衡
clock = time.clock() # 追踪帧率

buf_x=[0,0,0] # 坐标x的缓冲区
buf_y=[0,0,0] # 坐标y的缓冲区
frame_time=0.01 # FPS初始化(后面会更新成真实值)

uart = UART(3, 115200) # 设定好串口号，波特率

blob_thresholds=((85, 100, -12, 12, -12, 12)) # 白色

_rect = [60,20,260,220] # 边框的x1，y1，x2，y2
while(True):
    clock.tick()
    if find_once < 50 : # 50帧之前是搜索边框阶段
        find_once = find_once + 1
        find_rect()
    if find_once >= 50 : # 50帧之后是寻找小球阶段
        sensor.set_pixformat(sensor.RGB565) # 寻找小球使用RGB图像，设置合适的LAB阈值，用find_blobs()方法
        img = sensor.snapshot() # 从感光芯片获得一张图像
        blobs = img.find_blobs([blob_thresholds]) # 寻找色块
        for b in blobs:
            if b.w()>2 and b.w()<15: # 筛选宽度在3~14个像素之间的色块
                if b.h()>2 and b.h()<15: # 筛选高度在3~14个像素之间的色块
                    if b.x()>_rect[0] and b.x()<_rect[2]:        #这里是筛选小球可能出现的矩形区域
                        if b.y()>_rect[1] and b.y()<_rect[3]:    #这里是筛选小球可能出现的矩形区域
                            img.draw_rectangle(b[0:4],color=(0,0,255)) # rect #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy # 在目标颜色区域的中心画十字形标记
                            #print ("X= %d, Y=%d" %(b[5], b[6]))
                            buf_x[2] = buf_x[1];buf_x[1] = buf_x[0];
                            buf_y[2] = buf_y[1];buf_y[1] = buf_y[0];
                            buf_x[0] = int((b[5]-160)*650/200) # 将坐标先转化成毫米比例，再转化成int
                            buf_y[0] = int((b[6]-120)*650/200) # 将坐标先转化成毫米比例，再转化成int
                            speed_now_x=(buf_x[0]-buf_x[1])/frame_time #计算x方向的速度
                            speed_now_y=(buf_y[0]-buf_y[1])/frame_time #计算y方向的速度
                            speed_last_x=(buf_x[1]-buf_x[2])/frame_time #计算上一时刻x方向的速度
                            speed_last_y=(buf_y[1]-buf_y[2])/frame_time #计算上一时刻y方向的速度
                            a_speed_x=(speed_now_x-speed_last_x)/frame_time # 计算x方向的加速度
                            a_speed_y=(speed_now_y-speed_last_y)/frame_time # 计算y方向的加速度
                            print("x 位置：",buf_x[0]);print("y 位置：",buf_y[0])
                            print("x 速度：",int(speed_now_x));print("y 速度：",int(speed_now_y))
                            print("x 加速度：",int(a_speed_x));print("y 加速度：",int(a_speed_y))
                            # b是1字节 # h是short类型，2个字节，先发送低字节，再发送高字节
                            datap = pack('bbbbhhhhhh',0x35,0x46,0x57,0x24,buf_x[0],buf_y[0],int(speed_now_x),int(speed_now_y),int(a_speed_x),int(a_speed_y))
                            print('you send:',datap)
                            uart.write(datap)
    frame_time = clock.fps()
    print(frame_time)

```

主要设计思路.<br>
建立2个3帧的数组buf_x,buf_y.<br>
buf_x[0]是本时刻小球x坐标.<br>
buf_x[1]是上一时刻小球x坐标.<br>
buf_x[2]是上上一时刻小球x坐标.<br>
我们用(buf_x[0]-buf_x[1])/frame_time就得到了当前时刻速度.<br>
frame_time是帧间隔.<br>
同理，(buf_x[1]-buf_x[2])/frame_time是上一时刻速度.<br>
那么（当前时刻速度-上一时刻速度）/frame_time就得到了加速度.<br>

堆的简便设计：.<br>
当我们获得了小球当前时刻坐标，要对其更新的时候.<br>
我们首先使用move_()函数，move_()函数将buf_x[1]赋值给buf_x[2]，.<br>
将buf_x[0]赋值给buf_x[1]，这样，buf_x[0]的位置就空出来了，.<br>
之前的buf_x[2]因为数据过期被之前的buf_x[1]覆盖掉。.<br>

然后用find_blob()的方法检测色块.<br>

uart = UART(3, 115200)用来初始化串口.<br>
串口号在这里不重要.<br>
波特率为115200.<br>

uart.write(str)用来发送数据.<br>

img.draw_circle(),img.draw_string().<br>
这两个函数都是在图像上做标记.<br>
方便观察调试.<br>
