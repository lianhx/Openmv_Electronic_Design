import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 500)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

thresholds = [(160, 255)] # grayscale thresholds设置阈值
find_once = 0
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

while(True):
    clock.tick()
    find_rect()
    if find_once < 20 :
        find_once = find_once + 1
    if find_once >= 20 :
        img = sensor.snapshot().lens_corr(1.8)






    print("FPS %f" % clock.fps())
    frame_time = 1/clock.fps()
