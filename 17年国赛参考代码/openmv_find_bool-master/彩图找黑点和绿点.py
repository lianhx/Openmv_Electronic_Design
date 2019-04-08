import sensor, image, time, pyb
from pyb import UART
uart = UART(3, 57600)#timeout_char =10
from pyb import Pin
p8_pin = pyb.Pin.board.P8
p8_pin.init(Pin.IN,Pin.PULL_UP)

sensor.reset() # ��ʼ������ͷ
sensor.set_pixformat(sensor.GRAYSCALE) # ��ʽΪ RGB565.
sensor.set_framesize(sensor.QQVGA) # ʹ�� QQVGA �ٶȿ�һЩ
sensor.set_auto_whitebal(False)
clock = time.clock() # ׷��֡��
a=1
position_X=80
position_Y=60
new_point_ready = 0
detect_mode = 1#   1��ɫ   0��ɫ

def led_blink(x):
    led = pyb.LED(x)
    led.on()
    time.sleep(5)
    led.off()

def send_position():
    if (new_point_ready == 1):
        uart.writechar(0xFF)
        uart.writechar(position_X)
        uart.writechar(position_Y)
        
        if (detect_mode == 0):
            uart.writechar(0xFD)
            led_blink(3)
        else:
            led_blink(2)
    else:
        if (detect_mode == 0):
            uart.writechar(0xFE)

tim4 = pyb.Timer(4)              # create a timer object using timer 4
tim4.init(freq=50)                # trigger at 50Hz
tim4.callback(lambda t:send_position())

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob
while(True):
    if p8_pin.value()==0:
        detect_mode = 1
        blob_thresholds(0, 54, -15, 17, 5, 24)#��ɫ

    else:
        detect_mode = 0
        blob_thresholds=(14, 73, -70, -21, -5, 53)#��ɫ

    img = sensor.snapshot() # �Ӹй�оƬ���һ��ͼ��
    clock.tick() # Track elapsed milliseconds between snapshots().

    blobs = img.find_blobs([blob_thresholds])
    if blobs:
        new_point_ready = 1
        b=find_max(blobs)
 #       if b.pixels()/(b.w()*b.h())<0.60:
  #          continue
        img.draw_rectangle(b[0:4],color=(0,0,255)) # rect
        #�þ��α�ǳ�Ŀ����ɫ����
        img.draw_cross(b[5], b[6]) # cx, cy
        #��Ŀ����ɫ��������Ļ�ʮ���α��
        print ("�ڵ�λ��X= %d,Y=%d" %(b[5], b[6]))
        position_X=b[5]
        position_Y=b[6]
    else:
        new_point_ready = 0

    print(clock.fps())

