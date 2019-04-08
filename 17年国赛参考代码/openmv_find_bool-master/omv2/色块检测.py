# ɫ���� ����
#
# �������չʾ�����ͨ��find_blobs()����������ͼ���е�ɫ��
# ������Ӳ��ҵ���ɫ������ɫ

import sensor, image, time

# ��ɫ׷�ٵ����ӣ�һ��Ҫ���ƻ����Ĺ⣬���ֹ������ȶ��ġ�
green_threshold   = (   0,   80,  -70,   -10,   -0,   30)
black_threshold   = (0, 60, -128, 127, -128, 127)
#������ɫ����ֵ�������������ֵ�ֱ���L A B �����ֵ����Сֵ��minL, maxL, minA,
# maxA, minB, maxB����LAB��ֵ��ͼ�������������ͼ��ѡȡ������ǻҶ�ͼ����ֻ��
#���ã�min, max���������ּ��ɡ�

sensor.reset() # ��ʼ������ͷ
sensor.set_pixformat(sensor.GRAYSCALE) # ��ʽΪ RGB565.
#sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # ʹ�� QQVGA �ٶȿ�һЩ
sensor.skip_frames(10) # ����10֡��ʹ��������Ч
#sensor.set_auto_gain(False) #�Զ�����
sensor.set_auto_whitebal(False)
#�رհ�ƽ�⡣��ƽ����Ĭ�Ͽ����ģ�����ɫʶ���У�һ��Ҫ�رհ�ƽ�⡣
clock = time.clock() # ׷��֡��

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # �Ӹй�оƬ���һ��ͼ��

    blobs = img.find_blobs([black_threshold])
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
    if blobs:
    #����ҵ���Ŀ����ɫ
        for b in blobs:
        #�����ҵ���Ŀ����ɫ����
            if b[4]>200:
                # Draw a rect around the blob.
                img.draw_rectangle(b[0:4]) # rect
                #�þ��α�ǳ�Ŀ����ɫ����
                img.draw_cross(b[5], b[6]) # cx, cy
                #��Ŀ����ɫ��������Ļ�ʮ���α��

    print(clock.fps()) # ע��: ���OpenMV�������Ժ�֡�ʴ��Ϊԭ����һ��
    #����Ͽ����ԣ�֡�ʻ�����
