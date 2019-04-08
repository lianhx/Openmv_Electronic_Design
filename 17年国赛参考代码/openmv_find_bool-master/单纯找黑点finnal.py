# ɫ���� ����
#
# �������չʾ�����ͨ��find_blobs()����������ͼ���е�ɫ��
# ������Ӳ��ҵ���ɫ������ɫ

import sensor, image, time, pyb
from pyb import UART
uart = UART(3, 57600)#timeout_char =10

# ��ɫ׷�ٵ����ӣ�һ��Ҫ���ƻ����Ĺ⣬���ֹ������ȶ��ġ�
green_threshold   = (   0,   80,  -70,   -10,   -0,   30)
black_threshold   = (0, 13, -128, 127, -128, 127)
thresholds=(150,255)
blob_thresholds=(0,100)#80 @��������  100@��ǿ����
#������ɫ����ֵ�������������ֵ�ֱ���L A B �����ֵ����Сֵ��minL, maxL, minA,
# maxA, minB, maxB����LAB��ֵ��ͼ�������������ͼ��ѡȡ������ǻҶ�ͼ����ֻ��
#���ã�min, max���������ּ��ɡ�


sensor.reset() # ��ʼ������ͷ
sensor.set_pixformat(sensor.GRAYSCALE) # ��ʽΪ RGB565.
sensor.set_framesize(sensor.QQVGA) # ʹ�� QQVGA �ٶȿ�һЩ
sensor.skip_frames(10) # ����10֡��ʹ��������Ч
sensor.set_auto_whitebal(False)
#�رհ�ƽ�⡣��ƽ����Ĭ�Ͽ����ģ�����ɫʶ���У�һ��Ҫ�رհ�ƽ�⡣
clock = time.clock() # ׷��֡��

def led_blink(x):
    led = pyb.LED(x)
    led.on()
    time.sleep(5)
    led.off()
#tim4 = pyb.Timer(4)              # create a timer object using timer 4
#tim4.init(freq=1)                # trigger at 2Hz
#tim.callback(lambda t:pyb.LED(1).toggle())
#tim4.callback(lambda t:led_blink(1))
position_X=80
position_Y=60
def send_position():
    uart.writechar(0xFF)
    uart.writechar(position_X)
    uart.writechar(position_Y)

tim4 = pyb.Timer(4)              # create a timer object using timer 4
tim4.init(freq=50)                # trigger at 50Hz
tim4.callback(lambda t:send_position())
while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # �Ӹй�оƬ���һ��ͼ��
#    img.lens_corr(strength=1.8, zoom=1.0)
#    img.binary([thresholds], invert=False)

    blobs = img.find_blobs([blob_thresholds])
    #find_blobs(thresholds, invert=False, roi=Auto),thresholdsΪ��ɫ��ֵ��
    #��һ��Ԫ�飬��Ҫ�����ţ� ����������invert=1,��ת��ɫ��ֵ��invert=FalseĬ��
    #����ת��roi������ɫʶ�����Ұ����roi��һ��Ԫ�飬 roi = (x, y, w, h)������
    #�����϶���(x,y)��ʼ�Ŀ�Ϊw��Ϊh�ľ�������roi�����õĻ�Ĭ��Ϊ����ͼ����Ұ��
    #�����������һ���б�[0]����ʶ�𵽵�Ŀ����ɫ�������϶����x���꣬��1�ݴ���
    #���϶���y���꣬��2�ݴ���Ŀ������Ŀ���3�ݴ���Ŀ������ĸߣ���4�ݴ���Ŀ��
    #�������ص�ĸ�������5�ݴ���Ŀ����������ĵ�x���꣬��6�ݴ���Ŀ���������ĵ�y���꣬
    #��7�ݴ���Ŀ����ɫ�������ת�Ƕȣ��ǻ���ֵ�������ͣ��б�����Ԫ�������ͣ���
    #��8�ݴ������Ŀ�����򽻲��Ŀ���������9�ݴ�����ɫ�ı�ţ������������ֱ����
    #���������ĸ���ɫ��ֵthresholdʶ������ģ���
    pixles_temp=0
    if blobs:
    #����ҵ���Ŀ����ɫ
        for b in blobs:
            if b.pixels()>pixles_temp:
                pixles_temp=b.pixels()
        #�����ҵ���Ŀ����ɫ����
#            if b[0]==0 or b[0]+b[2]==160 or b[1]==0 or b[1]+b[3]==120:
#                continue
        for b in blobs:
            if b.pixels()!=pixles_temp:
                continue
            if b.pixels()/(b.w()*b.h())<0.60:
                continue
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4],color=(0,0,255)) # rect
            #�þ��α�ǳ�Ŀ����ɫ����
            img.draw_cross(b[5], b[6]) # cx, cy
            #��Ŀ����ɫ��������Ļ�ʮ���α��
            print ("�ڵ�λ��X= %d,Y=%d" %(b[5], b[6]))
#            print ("ƫ�ƽǶ�= %f" %(b.rotation()))
#            print ("�����ܶ�= %f\n" %(b.pixels()/(b.w()*b.h())))
            position_X=b[5]
            position_Y=b[6]
            led_blink(3)
            break
    print(clock.fps()) # ע��: ���OpenMV�������Ժ�֡�ʴ��Ϊԭ����һ��
    #����Ͽ����ԣ�֡�ʻ�����
