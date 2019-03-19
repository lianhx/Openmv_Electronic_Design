import sensor, image, time
from pyb import UART
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.HQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()
thresholds = [(210, 255)] # grayscale thresholds设置阈值

uart = UART(3, 115200)
while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    img.binary(thresholds)
    for c in img.find_circles(threshold = 4000, x_margin = 10, y_margin = 10, r_margin = 10,
            r_min = 2, r_max = 10, r_step = 2):
        img.draw_circle(c.x(), c.y(), c.r(), color = (0, 255, 0))#识别到的圆形用圆框出来
        img.draw_string(c.x(), c.y(), str(c.x())+" , "+str(c.y()),color=(0,255,0))
        output_str="[%d,%d]" % (c.x(),c.y())
        print('you send:',output_str)
        uart.write(output_str+'\r\n')
    print("FPS %f" % clock.fps())
