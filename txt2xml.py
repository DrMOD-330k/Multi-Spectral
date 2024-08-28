
import os
import math
from xml.dom.minidom import Document


def readlabeltxt(txtpath):
    with open(txtpath, 'r') as f_in:  # 打开txt文件
        lines = f_in.readlines()
        splitlines = [x.strip().split(' ') for x in lines]  # 根据空格分割
    return splitlines


def writeXml(tmp, name_id, w, h, d, bboxes):
    doc = Document()
    # owner
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    # owner
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder_txt = doc.createTextNode("rgb_pad")
    folder.appendChild(folder_txt)

    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename_txt = doc.createTextNode(name_id)
    filename.appendChild(filename_txt)
    
    path = doc.createElement('path')
    annotation.appendChild(path)
    path_name = os.path.join("C:/Users/chenmu/Desktop/Dataset_400/pyy-97/rgb_pad/", name_id + ".png")
    path_txt = doc.createTextNode(path_name)
    path.appendChild(path_txt)
    
    # ones #
    source = doc.createElement('source')
    annotation.appendChild(source)
    database = doc.createElement('database')
    source.appendChild(database)
    database_txt = doc.createTextNode("Unknow")
    database.appendChild(database_txt)
    # onee #
    
    # twos #
    size = doc.createElement('size')
    annotation.appendChild(size)

    width = doc.createElement('width')
    size.appendChild(width)
    width_txt = doc.createTextNode(str(w))
    width.appendChild(width_txt)

    height = doc.createElement('height')
    size.appendChild(height)
    height_txt = doc.createTextNode(str(h))
    height.appendChild(height_txt)

    depth = doc.createElement('depth')
    size.appendChild(depth)
    depth_txt = doc.createTextNode(str(d))
    depth.appendChild(depth_txt)
     
    segmented = doc.createElement('segmented')
    annotation.appendChild(segmented)
    segmented_txt = doc.createTextNode("0")
    segmented.appendChild(segmented_txt)
    # twoe #
    
    # threes #
    for bbox in bboxes:
        if float(bbox[5]) < 0.5:
            continue
        object_new = doc.createElement("object")
        annotation.appendChild(object_new)
        
        type = doc.createElement('type')
        object_new.appendChild(type)
        type_txt = doc.createTextNode("robndbox")
        type.appendChild(type_txt)

        name = doc.createElement('name')
        object_new.appendChild(name)
        name_txt = doc.createTextNode(str(bbox[-1]) + " 0 0")
        name.appendChild(name_txt)

        pose = doc.createElement('pose')
        object_new.appendChild(pose)
        pose_txt = doc.createTextNode("Unspecified")
        pose.appendChild(pose_txt)

        truncated = doc.createElement('truncated')
        object_new.appendChild(truncated)
        truncated_txt = doc.createTextNode("0")
        truncated.appendChild(truncated_txt)

        difficult = doc.createElement('difficult')
        object_new.appendChild(difficult)
        difficult_txt = doc.createTextNode("0")
        difficult.appendChild(difficult_txt)
         
        robndbox = doc.createElement('robndbox')
        object_new.appendChild(robndbox)
        
        cx = doc.createElement('cx')
        robndbox.appendChild(cx)
        cx_value = float(bbox[0]) + 100.00
        cx_txt = doc.createTextNode(str(cx_value))
        cx.appendChild(cx_txt)
        
        cy = doc.createElement('cy')
        robndbox.appendChild(cy)
        cy_value = float(bbox[1]) + 100.00
        cy_txt = doc.createTextNode(str(cy_value))
        cy.appendChild(cy_txt)
        
        w = doc.createElement('w')
        robndbox.appendChild(w)
        w_txt = doc.createTextNode(bbox[2])
        w.appendChild(w_txt)
        
        h = doc.createElement('h')
        robndbox.appendChild(h)
        h_txt = doc.createTextNode(bbox[3])
        h.appendChild(h_txt)
        
        angle = doc.createElement('angle')
        robndbox.appendChild(angle)
        angle_value = float(bbox[4])
        if angle_value < 0.0:
            angle_value += math.pi
        angle_txt = doc.createTextNode(str(angle_value))
        angle.appendChild(angle_txt)

    xmlname = os.path.splitext(name_id)[0]
    tempfile = os.path.join(tmp, xmlname + '.xml')
    with open(tempfile, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    return


if __name__ == '__main__':
    labeltxt_path = '/data3/QHL01/DATA_MSOD/data/label_txt/'   # txt标签的所在路径
    labelxml_path = '/data3/QHL01/DATA_MSOD/data/label_xml/'   # xml格式存储位置
    if not os.path.exists(labelxml_path):
        os.makedirs(labelxml_path)
    filenames = os.listdir(labeltxt_path)  # 获取每一个txt的名称
    for filename in filenames:
        filepath = labeltxt_path + filename  # 每一个标签的具体路径
        name_id = filename[:-4]
        (W, H, D) = (1400, 1100, 3)  # 样本的大小
        boxes = readlabeltxt(filepath)  # 读取txt内容
        if len(boxes) == 0:
            print('文件为空', filepath)
            continue
        writeXml(labelxml_path, name_id, W, H, D, boxes)  # 书写xml
        # print('正在处理%s' % filename)
