# 用于将obb格式转为ploy，已经用不到了

import glob
import xml.etree.ElementTree as ET
import numpy as np
import math
import os.path as osp

def Srotate(angle,valuex,valuey,pointx,pointy):
    valuex = np.array(valuex)
    valuey = np.array(valuey)
    sRotatex = (valuex-pointx)*math.cos(angle) + (valuey-pointy)*math.sin(angle) + pointx
    sRotatey = (valuey-pointy)*math.cos(angle) - (valuex-pointx)*math.sin(angle) + pointy
    return sRotatex,sRotatey


ann_folder = "/data/users/qinhaolin01/MSOD/mmrotate/data/msod/labels"
txt_folder = "/data/users/qinhaolin01/MSOD/mmrotate/data/msod/txts/"
ann_files = glob.glob(ann_folder + '/*.xml')
for ann_file in ann_files:
    img_id = osp.split(ann_file)[1][:-4]
    txt_name = txt_folder + img_id + '.txt'
    f_files = open(txt_name,'w')
    tree = ET.parse(ann_file)
    root = tree.getroot()
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)
    for obj in root.findall('object'):
        name = obj.find('name').text
        cls_name = name.split(' ')[0]
        if cls_name == 'pedestrain':
            cls_name = 'pedestrian'
        if obj.find('robndbox') == None:
            bbox = np.array([[
                float(obj.find('bndbox/xmin').text),
                float(obj.find('bndbox/ymin').text),
                float(obj.find('bndbox/xmax').text),
                float(obj.find('bndbox/ymin').text),
                float(obj.find('bndbox/xmin').text),
                float(obj.find('bndbox/ymax').text),
                float(obj.find('bndbox/xmax').text),
                float(obj.find('bndbox/ymax').text)
                ]],dtype=np.float32)
        else:
            cx = float(obj.find('robndbox/cx').text)
            cy = float(obj.find('robndbox/cy').text)
            w = float(obj.find('robndbox/w').text)
            h = float(obj.find('robndbox/h').text)
            a = float(obj.find('robndbox/angle').text)
            
            # xmin = min((cx - w/2), 0)
            # xmax = max((cx + w/2), width)
            # ymin = min((cy - h/2), 0)
            # ymax = max((cy + h/2), height)
            
            xmin = (cx - w/2)
            xmax = (cx + w/2)
            ymin = (cy - h/2)
            ymax = (cy + h/2)
            
            x0, y0 = Srotate(a, xmin, ymin, cx, cy)
            x1, y1 = Srotate(a, xmax, ymin, cx, cy)
            x2, y2 = Srotate(a, xmax, ymax, cx, cy)
            x3, y3 = Srotate(a, xmin, ymax, cx, cy)
            
            bbox = np.array([[
                x0,
                y0,
                x1,
                y1,
                x2,
                y2,
                x3,
                x3
                ]],dtype=np.float32)
        # print(bbox[0])
        bbox = bbox[0]
        f_files.write(str(bbox[0]) + ' ' + str(bbox[1]) + ' ' + str(bbox[2]) + ' ' + str(bbox[3]) + ' ' + str(bbox[4]) + ' ' + str(bbox[5]) + ' ' + str(bbox[6]) + ' ' + str(bbox[7]) + ' ' + cls_name + '\n')
        # f_files.write(str(bbox[0][:]) + ' ' + cls_name + '\n')
    f_files.close()
    