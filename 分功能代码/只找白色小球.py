import sensor, image, time, pyb
sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_whitebal(False)
clock = time.clock() # 追踪帧率
position_X=160
position_Y=120









while(True):
    blob_thresholds=((70, 100, -12, 12, -12, 12))#白色
    img = sensor.snapshot() # 从感光芯片获得一张图像
    clock.tick() # Track elapsed milliseconds between snapshots().

    blobs = img.find_blobs([blob_thresholds])
    for b in blobs:
        if b.w()>2 and b.w()<8:
            if b.h()>2 and b.h()<8:
                img.draw_rectangle(b[0:4],color=(0,0,255)) # rect #用矩形标记出目标颜色区域
                img.draw_cross(b[5], b[6]) # cx, cy#在目标颜色区域的中心画十字形标记
                print ("X= %d, Y=%d" %(b[5], b[6]))
                position_X=b[5]
                position_Y=b[6]
    print(clock.fps())

