import os
import shutil
import random

ori_path = '/usb4t/Dataset1/Dataset1.0-6183/'
new_path = '/data3/QHL01/DATA_MSOD/data/maod_first/'
img_list = os.listdir(ori_path+'rgb/')
random.shuffle(img_list)
train_len = len(img_list) * 8 // 10
train_img_list = img_list[:train_len]
test_img_list = img_list[train_len:]

for i in range(len(train_img_list)):
    shutil.copy(ori_path+'rgb/'+train_img_list[i], new_path+'images/train/'+train_img_list[i])
    shutil.copy(ori_path+'label-3/'+train_img_list[i].replace('png','xml'), new_path+'labels/train/'+train_img_list[i].replace('png','xml'))

for i in range(len(test_img_list)):
    shutil.copy(ori_path+'rgb/'+test_img_list[i], new_path+'images/test/'+test_img_list[i])
    shutil.copy(ori_path+'label-3/'+test_img_list[i].replace('png','xml'), new_path+'labels/test/'+test_img_list[i].replace('png','xml'))