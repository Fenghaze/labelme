# -*- encoding: utf-8 -*-
"""
@File    : label2gray.py
@Time    : 2020/12/16 9:36
@Author  : Zhl
@Desc    : 
"""

import os
import PIL.Image
import numpy as np
from skimage import io, data, color
from skimage.io import imread, imsave
from PIL import Image
import pandas as pd
from sklearn.model_selection import train_test_split
import os.path as osp

# 为生成的label上色
def draw_color(label_path):
    img_lst = os.listdir(label_path)
    for img in img_lst:
        save_path = os.path.join(label_path, img)
        img_path = os.path.join(label_path, img)
        img = PIL.Image.open(img_path)
        img = np.array(img)
        dst = color.label2rgb(img, bg_label=0, bg_color=(0, 0, 0))  # 背景的标签为0，颜色为黑色。分割多个类别时，查看skimage原函数
        io.imsave(save_path, dst)
        #edit_pixel_color(img_path, save_path)

# 修改目标的像素颜色
def edit_pixel_color(img, save_path):
    i = 1
    j = 1
    img = Image.open(img)  # 读取系统的内照片
    width = img.size[0]  # 长度
    height = img.size[1]  # 宽度
    for i in range(0, width):  # 遍历所有长度的点
        for j in range(0, height):  # 遍历所有宽度的点
            data = (img.getpixel((i, j)))  # 打印该图片的所有点
            if (data[0]==1):  # 判断RGBA的R值
                # 判断条件就是一个像素范围范围
                img.putpixel((i,j),(255,0,0))#则这些像素点的颜色改成白色
    img = img.convert("RGB")  # 把图片强制转成RGB
    img.save(save_path)  # 保存修改像素点后的图片

# 将RGB转为灰度图
def convert_from_color_segmentation(img):
  arr_2d = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
  palette = {
    (  0,   0,   0) : 0 ,   # class：背景；  color：0,0,0；   label：0
    (255,   0,   0) : 1     # class：ship;  color：255,0,0； label：1
    }
  for c, i in palette.items():
    m = np.all(img == np.array(c).reshape(1, 1, 3), axis=2)
    arr_2d[m] = i
  return arr_2d

# 生成灰度图
def rgb2gray(label_path, gray_path):
    img_lst = os.listdir(label_path)
    for img in img_lst:
        gray_label_path = os.path.join(gray_path, img)
        img = imread(os.path.join(label_path, img))
        if len(img.shape) > 2:
            img_gray = convert_from_color_segmentation(img)
            imsave(os.path.join(gray_label_path), img_gray)

# 测试生成的灰度图是否成功
def test_gray(label_img):
    img = Image.open(label_img)
    img = np.array(img)
    print(np.unique(img))

def mkdir(dir):
    if not osp.exists(dir):
        os.mkdir(dir)

if __name__ == '__main__':
    label_path = './ship_waterline/out/label'
    gray_path = './ship_waterline/out/gray'
    mkdir(gray_path)
    draw_color(label_path)
    rgb2gray(label_path, gray_path)