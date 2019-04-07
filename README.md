# Openmv_Electronic_Design
FinalEdition.py
===========================================================
工作基本完成<br>

更新一波：<br>
调用霍夫圆检测的算法会使得算力不够，效率降低<br>
期望采用图像块遍历的方法进行快速搜索定位<br>
具体任务有：<br>
1、木板边界定位<br>
2、小球定位<br>
目前这两个任务已经在Windows端使用opencv实现，接下来移植成python代码即可<br>
![Image text](https://github.com/ssmem/Openmv_Electronic_Design/blob/master/demo.jpg)
![Image text](https://github.com/ssmem/Openmv_Electronic_Design/blob/master/demo.PNG)

OKmain.py
===========================================================
OKmain.py就是说这是功能合成后的脚本文件了.<br>
其他的文件都是只作模块化学习.<br>
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


cal_speed_aspeed.py
===========================================================
1.设计了一个3帧的堆.<br>
遵循数据先进先出的原则.<br>
即我们的数据时时刻刻都是最新3帧并且按顺序排好的.<br>
2.给出了计算速度和加速度的方法.<br>
frame_time是两帧之间的间隔时间.<br>


detect_send_ball_position.py
============================================================
初始化相机，设置一些有利于我们的参数.<br>

thresholds = [(210, 255)] .<br>
这里意思是我们按照灰度值对每个像素进行二值化处理（非黑即白）.<br>
当灰度值在(0,210)之间认为是黑色.<br>
当灰度值在(210，255)之间认为是白色.<br>

然后用find_circles()的方法检测圆形.<br>
find_circles()的第一个参数是threshold.<br>
值越大对圆形的标准程度要求越高.<br>

uart = UART(3, 115200)用来初始化串口.<br>
串口号在这里不重要.<br>
波特率为115200.<br>

uart.write(str)用来发送数据.<br>

img.draw_circle(),img.draw_string().<br>
这两个函数都是在图像上做标记.<br>
方便观察调试.<br>
