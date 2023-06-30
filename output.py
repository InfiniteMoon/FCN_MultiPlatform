import os
import cv2
import numpy as np
import json
with open("data.json", "r") as f: # 打开json文件
    data = json.load(f) # 读取并解码json数据
    
#im1 原图  im2 mask图(背景是黑色，前景是白色)
im1_path = 'input'
im2_path = 'outmask'
print(data["color"])


#透明
if(data["color"]=="none"):
    num = len(os.listdir(im1_path))
    for i in range(num):
        img1 = cv2.imread(os.path.join(im1_path, os.listdir(im1_path)[i]))
        img2 = cv2.imread(os.path.join(im2_path, os.listdir(im2_path)[i]), cv2.IMREAD_GRAYSCALE)
        h, w, c = img1.shape
        # 反转mask图
        if (data["back"] == "true"):
            img2 = cv2.bitwise_not(img2)
        img3 = np.zeros((h, w, 4))
        img3[:, :, 0:3] = img1
        img3[:, :, 3] = img2
        # 这里命名随意，但是要注意使用png格式
        cv2.imwrite(os.path.join('output', '%s' % os.listdir(im1_path)[i]), img3)

#黑
if(data["color"]=="black"):
    num = len(os.listdir(im1_path))
    for i in range(num):
        img1 = cv2.imread(os.path.join(im1_path, os.listdir(im1_path)[i]))
        img2 = cv2.imread(os.path.join(im2_path,os.listdir(im2_path)[i]), cv2.IMREAD_GRAYSCALE)
        h,w,c = img1.shape
        # 反转mask图
        if (data["back"] == "true"):
            img2 = cv2.bitwise_not(img2)
        # 将mask图转化为灰度图
        img2 = img2 / 255.0
        # 将人像抠出来
        img1[:, :, 0] = img1[:, :, 0] * img2
        img1[:, :, 1] = img1[:, :, 1] * img2
        img1[:, :, 2] = img1[:, :, 2] * img2
        # 这里命名随意，但是要注意使用png格式
        cv2.imwrite(os.path.join('output', '%s' % os.listdir(im1_path)[i]), img1)

#白
if(data["color"]=="white"):
    num = len(os.listdir(im1_path))
    for i in range(num):
        img1 = cv2.imread(os.path.join(im1_path, os.listdir(im1_path)[i]))
        img2 = cv2.imread(os.path.join(im2_path,os.listdir(im2_path)[i]), cv2.IMREAD_GRAYSCALE)
        h,w,c = img1.shape
        # 反转mask图
        if (data["back"] == "true"):
            img2 = cv2.bitwise_not(img2)
        # 用255减去反转后的mask图
        img3 = 255 - img2
        # 把mask图扩展到三通道
        img3 = cv2.cvtColor(img3, cv2.COLOR_GRAY2BGR)
        # 把mask图和原图相加
        img4 = cv2.add(img1, img3)
        # 这里命名随意，但是要注意使用png格式
        cv2.imwrite('output/' + '%s' % os.listdir(im1_path)[i], img4)
