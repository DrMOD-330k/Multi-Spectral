操作手册

1、下载mmrotate源码，并按照readme配置环境
2、在主目录下创建data文件夹，放入maod数据集，格式如下：
data
    maod
        images
            test
                ****.png
            train
                ****.png
        labels
            test
                ****.xml
            train
                ****.xml
3、新增文件
/data/users/qinhaolin01/MSOD/mmrotate/configs/_base_/datasets/maod.py
4、选择要使用的模型，并新增config文件，这里选择了roi_trans
因此新增 /data/users/qinhaolin01/MSOD/mmrotate/configs/roi_trans/roi_trans_r50_fpn_6x_maod_le90.py
5、新增文件
/data/users/qinhaolin01/MSOD/mmrotate/mmrotate/datasets/maod.py
6、在/data/users/qinhaolin01/MSOD/mmrotate/mmrotate/datasets/__init__.py中
注册新增的数据集
7、训练模型
不加载预训练模型：
CUDA_VISIBLE_DEVICES=0,1,2,3 bash ./tools/dist_train.sh /data/users/qinhaolin01/MSOD/mmrotate/configs/roi_trans/roi_trans_r50_fpn_6x_maod_le90.py 4 --work-dir /data/users/qinhaolin01/MSOD/mmrotate/work/maod_1203
最好的结果是42.pth，后面开始过拟合了
加载预训练模型：
先在/data/users/qinhaolin01/MSOD/mmrotate/tools/train.py中新增一个arg
再根据readme中的链接下载预训练模型到checkpoints
parser.add_argument(
        '--load-from', help='the checkpoint file to load from')
CUDA_VISIBLE_DEVICES=0,1,2,3 bash ./tools/dist_train.sh /data/users/qinhaolin01/MSOD/mmrotate/configs/roi_trans/roi_trans_r50_fpn_6x_maod_le90.py 4 --work-dir /data/users/qinhaolin01/MSOD/mmrotate/work/maod_1203_pre --load-from /data/users/qinhaolin01/MSOD/mmrotate/checkpoints/roi_trans_r50_fpn_1x_dota_le90-d1f0b77a.pth
效果不如不加
8、可视化，并保存结果为txt
在work下新建txt文件夹
更改/data/users/qinhaolin01/anaconda3/envs/open-mmlab/lib/python3.7/site-packages/mmdet/apis/test.py
for i, (img, img_meta) in enumerate(zip(imgs, img_metas)):
    h, w, _ = img_meta['img_shape']
    img_show = img[:h, :w, :]

    ori_h, ori_w = img_meta['ori_shape'][:-1]
    img_show = mmcv.imresize(img_show, (ori_w, ori_h))

    if out_dir:
        out_file = osp.join(out_dir, img_meta['ori_filename'])
    else:
        out_file = None
    
    class_name = ['car', 'van', 'truck', 'bus', 'tricycle', 'motor', 'bicycle', 'awning-motor', 'pedestrian', 'person']
    txt_path = "/data/users/qinhaolin01/MSOD/mmrotate/work/txt/"
    txt_file = osp.join(txt_path, img_meta['ori_filename']).replace('png','txt')
    f_files = open(txt_file,'w')
    for cls in range(len(result[i])):
        if len(result[i][cls]) == 0:
            continue
        name = class_name[cls]
        for det in range(len(result[i][cls])):
            obb = result[i][cls][det]
            f_files.write(str(obb[0]) + ' ' + str(obb[1]) + ' ' + str(obb[2]) + ' ' + str(obb[3]) + ' ' + str(obb[4]) + ' ' + name + '\n')
        
    # f_files.writelines(str(result[i]))
    f_files.close()

    model.module.show_result(
        img_show,
        result[i],
        bbox_color=PALETTE,
        text_color=PALETTE,
        mask_color=PALETTE,
        show=show,
        out_file=out_file,
        score_thr=show_score_thr)
可通过注释的方式关闭可视化或者关闭保存txt
python ./tools/test.py configs/roi_trans/roi_trans_r50_fpn_6x_maod_le90.py work/maod_1203/epoch_42.pth --show-dir work/vis_maod_1203
9、将txt转换为xml
在work下新建xml文件夹
创建/data/users/qinhaolin01/MSOD/mmrotate/txt2xml.py并运行，注意路径设置

使用前改变三个路径
1：/data/users/qinhaolin01/MSOD/mmrotate/configs/_base_/datasets/maod.py
test ann_file 和 img_prefix
2：/data/users/qinhaolin01/MSOD/mmrotate/txt2xml.py
labeltxt_path 和 labelxml_path
3：/data/users/qinhaolin01/anaconda3/envs/open-mmlab/lib/python3.7/site-packages/mmdet/apis/test.py
txt_path


通道3到8
1、/data/users/qinhaolin01/MSOD/mmrotate/configs/_base_/datasets/maod.py
img_norm_cfg
2、/data/users/qinhaolin01/anaconda3/envs/open-mmlab/lib/python3.7/site-packages/mmdet/apis/test.py
注释png，取消mat的注释
3、/data/users/qinhaolin01/MSOD/mmrotate/configs/roi_trans/roi_trans_r50_fpn_6x_maod_le90.py
img_norm_cfg
4、/data/users/qinhaolin01/anaconda3/envs/open-mmlab/lib/python3.7/site-packages/mmcv/image/photometric.py
45行，取消注释（不确定是否需要）
5、/data/users/qinhaolin01/anaconda3/envs/open-mmlab/lib/python3.7/site-packages/mmdet/models/backbones/resnet.py
371行 in_channels
6、/data/users/qinhaolin01/MSOD/mmrotate/mmrotate/datasets/maod.py
78、79行注释
7、/data/users/qinhaolin01/anaconda3/envs/open-mmlab/lib/python3.7/site-packages/mmcv/fileio/file_client.py
539行，写了if判断文件结尾是否为mat，因此不需要改动（加了判断是否为mat的条件句）
8、/data/users/qinhaolin01/anaconda3/envs/open-mmlab/lib/python3.7/site-packages/mmcv/image/io.py
264行注释


8通道数据跑测试集/data/users/chenzhenxiang01/mmrotate2/tools/test.py
笔记：陈震香，2024/05/16
1、/data/users/chenzhenxiang01/anaconda3/envs/mmrotate/lib/python3.8/site-packages/mmdet/apis/test.py
40行，提取三通道合成伪彩色，img_tensor = img_tensor[:, [4, 2, 1], :, :]
2、/data/users/chenzhenxiang01/anaconda3/envs/mmrotate/lib/python3.8/site-packages/mmcv/image/misc.py
48行，修改三个通道相应的归一化值和方差
mean = mean[[4,2,1]]
std  = std[[4,2,1]]
3、/data/users/chenzhenxiang01/mmrotate2/mmrotate/core/visualization/image.py
262行，修改图像后缀，out_file = out_file.replace('.npy', '.png')


8通道抽3通道伪彩色训练
笔记：陈震香，2024/05/17
1、/data/users/chenzhenxiang01/mmrotate2/configs/rotated_faster_rcnn/rotated_faster_rcnn_r50_fpn_1x_dota_le90.py
19行，修改预训练权重，3通道训练时使用原始的ResNet50预训练权重
119行，修改归一化值，3通道训练时使用8抽3的归一化值！！！
129行，img_scale=(1200, 900)  # 原图是1200*900
2、/data/users/chenzhenxiang01/mmrotate2/configs/_base_/datasets/maod.py
5行，一定要修改mean和std，不然测试的时候会报错
3、/data/users/chenzhenxiang01/anaconda3/envs/mmrotate/lib/python3.8/site-packages/mmcv/fileio/file_client.py
550行，data = data_8[[4,2,1],:,:]，8通道抽取三通道伪彩色，顺序RGB
4、/data/users/chenzhenxiang01/anaconda3/envs/mmrotate/lib/python3.8/site-packages/mmdet/models/backbones/resnet.py
371行，通道数改为3
注意修改训练轮次：12,36？关闭了预处理的随机裁剪


在3通道基础上，逐个增加通道
笔记：陈震香，2024/08/11
1、/data/users/chenzhenxiang01/mmrotate2/configs/oriented_rcnn/oriented_rcnn_r50_fpn_1x_dota_le90.py
19行，修改对应的预训练权重
135行，匹配归一化值
2、/data/users/chenzhenxiang01/mmrotate2/configs/_base_/datasets/maod.py
15行，匹配归一化值
3、/data/users/chenzhenxiang01/anaconda3/envs/mmrotate/lib/python3.8/site-packages/mmcv/fileio/file_client.py
550行，data = data_8[[0,1,2,4],:,:]
4、/data/users/chenzhenxiang01/anaconda3/envs/mmrotate/lib/python3.8/site-packages/mmdet/models/backbones/resnet.py
371行，通道数改为4