import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()
LAB_Ball=(91, 100, 127, -128, -128, 127)#使用IDE自带工具箱设计阈值
while(True):
    clock.tick()
    img = sensor.snapshot()
    Ball_blobs=img.find_blobs([LAB_Ball])
    for Ball_blob in Ball_blobs:
        img.draw_rectangle(Ball_blob.rect(),color=(0,0,0),thickness=2,fill=False)
    print(clock.fps())
