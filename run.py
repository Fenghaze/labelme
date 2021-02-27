# -*- encoding: utf-8 -*-
"""
@File    : run.py
@Time    : 2020/12/16 9:07
@Author  : Zhl
@Desc    : 
"""

import os
import argparse
import base64
import json
import os
import os.path as osp

import imgviz
import PIL.Image

from labelme.logger import logger
from labelme import utils

def mkdir(dir):
    if not osp.exists(dir):
        os.mkdir(dir)

def json2img(json_file, out, index):
    if out is None:
        out_dir = osp.basename(json_file).replace(".", "_")
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    else:
        out_dir = out
    mkdir(out_dir)
    data = json.load(open(json_file))
    imageData = data.get("imageData")

    if not imageData:
        imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
        with open(imagePath, "rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode("utf-8")
    img = utils.img_b64_to_arr(imageData)

    label_name_to_value = {"_background_": 0}
    for shape in sorted(data["shapes"], key=lambda x: x["label"]):
        label_name = shape["label"]
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value
    lbl, _ = utils.shapes_to_label(
        img.shape, data["shapes"], label_name_to_value
    )

    label_names = [None] * (max(label_name_to_value.values()) + 1)
    for name, value in label_name_to_value.items():
        label_names[value] = name

    lbl_viz = imgviz.label2rgb(
        label=lbl, img=imgviz.asgray(img), label_names=label_names, loc="rb"
    )
    img_name = str(index) + '.jpg'
    out_dir_raw  = out_dir + '/raw'
    out_dir_label = out_dir + '/label'
    mkdir(out_dir_raw)
    mkdir(out_dir_label)
    PIL.Image.fromarray(img).save(osp.join(out_dir_raw, img_name))  #保存图片 1.jpg
    utils.lblsave(osp.join(out_dir_label, img_name.replace('.jpg', '.png')), lbl) #保存标签 1.png
    #PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, "label_viz.png"))

    with open(osp.join(out_dir, "label_names.txt"), "w") as f:
        for lbl_name in label_names:
            f.write(lbl_name + "\n")

    logger.info("Saved to: {}".format(out_dir))

if __name__ == '__main__':

    json_path = './ship_waterline/json'
    out = './ship_waterline/out'
    json_files = os.listdir(json_path)

    for (index, file) in enumerate(json_files):
        json_file = os.path.join(json_path, file)
        json2img(json_file, out, index+1)
