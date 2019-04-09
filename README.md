# Openmv_Electronic_Design
##### 上传几个往年国赛代码。。。这里注明一下来源：mengfanli / openmv_find_bool 
## 重新修订一下处理过程
### 先对图像二值化，然后精准地寻找一次边框
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
thresholds = [(160, 255)] # 二值化设置阈值

find_once = 0 # 搜索边框计数变量
search_rect = [5,5,310,230] # 边框的x1，y1，x2，y2
def find_rect():
    if(find_once < 50):
        sensor.set_pixformat(sensor.GRAYSCALE) # 设置成灰度图像读取
        thresh = sensor.snapshot().lens_corr(1.8) # 读取图像
        thresh.binary(thresholds) # 二值化处理
        u_flag = 1;d_flag = 1;l_flag = 1;r_flag = 1 # 设置4个边界的查找状态变量，若查找成功为0，否则为1
        height = thresh.height();width = thresh.width() # 获取图像的高度和宽度
        rect=[int(0.2*width),int(0.1*height),int(0.8*width),int(0.9*height)] # 初始化一个矩形变量
        # col是列的意思，row是行的意思，width是列的数量，height是行的数量
        for row in range(int(0.5*height),0,-2): # 向上寻找上边界
            col = int(0.5*width)
            pv = thresh.get_pixel(col,row) # 获取(col,row)这个点的像素值
            if((pv>150)&(u_flag)):u_flag=0;rect[1]=row
            if(u_flag==1):rect[1]=5
                
        for row in range(int(0.5*height),height,2): # 向下寻找下边界
            col = int(0.5*width)
            pv = thresh.get_pixel(col,row) # 获取(col,row)这个点的像素值
            if((pv>150)&(d_flag)):d_flag=0;rect[3]=row
            if(d_flag==1):rect[3]=height-5
                
        for col in range(int(0.5*width),0,-2): # 向左寻找左边界
            row = int(0.5*height)
            pv = thresh.get_pixel(col,row) # 获取(col,row)这个点的像素值
            if((pv>150)&(l_flag)):l_flag=0;rect[0]=col
            if(l_flag==1):rect[0]=5
                
        for col in range(int(0.5*width),width,2): # 向右寻找右边界
            row = int(0.5*height)
            pv = thresh.get_pixel(col,row) # 获取(col,row)这个点的像素值
            if((pv>150)&(r_flag)):r_flag=0;rect[2]=col
            if(r_flag==1):rect[3]=width-5
        # 如果搜索得到的矩形太小，很可能不符合要求，仍认为矩形大小为初始化的矩形大小
        if(rect[2]-rect[0]<0.5*width):rect=[int(0.1*width),int(0.05*height),int(0.9*width),int(0.95*height)]
        if(rect[3]-rect[1]<0.5*height):rect=[int(0.1*width),int(0.05*height),int(0.9*width),int(0.95*height)]
        thresh.draw_rectangle(rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1]) # 绘制矩形框
        print(search_rect[0],search_rect[1],search_rect[2],search_rect[3]) # 打印矩形框坐标
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
            if b.w()>2 and b.w()<15: # 筛选宽度在3~14之间的色块
                if b.h()>2 and b.h()<15: # 筛选宽度在3~14之间的色块
                    if b.x()>20 and b.x()<300:        #这里是筛选小球可能出现的矩形区域
                        if b.y()>20 and b.y()<220:    #这里是筛选小球可能出现的矩形区域
                            img.draw_rectangle(b[0:4],color=(0,0,255)) # rect #用矩形标记出目标颜色区域
                            img.draw_cross(b[5], b[6]) # cx, cy # 在目标颜色区域的中心画十字形标记
                            #print ("X= %d, Y=%d" %(b[5], b[6]))
                            buf_x[0] = int((b[5]-160)*600/230) # 将坐标先转化成毫米比例，再转化成int
                            buf_y[0] = int((b[6]-120)*600/230) # 将坐标先转化成毫米比例，再转化成int
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

thresholds = [(210, 255)] .<br>
这里意思是我们按照灰度值对每个像素进行二值化处理（非黑即白）.<br>
当灰度值在(0,210)之间认为是黑色.<br>
当灰度值在(210，255)之间认为是白色.<br>

然后用find_blob()的方法检测色块.<br>

uart = UART(3, 115200)用来初始化串口.<br>
串口号在这里不重要.<br>
波特率为115200.<br>

uart.write(str)用来发送数据.<br>

img.draw_circle(),img.draw_string().<br>
这两个函数都是在图像上做标记.<br>
方便观察调试.<br>
