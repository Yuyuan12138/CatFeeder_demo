# 实现猫脸识别



yolov3猫脸识别模型

https://aistudio.baidu.com/aistudio/projectdetail/5417377?contributionType=1



我们的步骤依次为

1. 标注数据集
2. 生成训练集和验证集
3. 生成标签文档
4. 安装相关包
   1. 安装`PaddleDetection`
   2. 对`PaddleDetection`中`pip`进行更新,并下载相关依赖
   3. 安装`PaddleDet`
   4. 编辑`voc`文件

5. 使用训练集训练模型
6. 验证集验证训练效果





```python
!unzip -qoa data/data1877550/EasyDL_Dataset_ds-a0wss6d3fb_VOC.zip
```

这是我们在`EasyDL`中事先已经标注好的数据集,这里我们要先将他解压放在`work`文件夹中,方便后续使用

```python
!unzip -qoa data/data1877550/EasyDL_Dataset_ds-a0wss6d3fb_VOC.zip -d work/
```

下面我们要去生成训练集和验证集

```python
import random
import os
random.seed(2020)
xml_dir ='/home/aistudio/EasyDL_ds-a0wss6d3fb-VOC/Annotations'#标签文件的地址
img_dir ='/home/aistudio/EasyDL_ds-a0wss6d3fb-VOC/JPEGImages'#图像文件的地址
path_list = list()#新建存放路径的列表
for img in os.listdir(img_dir,img):
    img_path =os.path.join(img_dir,img)#图像路径
    xml_path =os.path.join(xml_dir,img.replace('jpg','xml'))#标签路径
    path_list.append((img_path,xml_path))#生成图片路径列表
random.shuffle(path_list)#打乱数据集
ratio =0.9#确定训练集和验证集的比例大小9:1
train_f =open('/home/aistudio/work/train.txt','w')#生成训练文件
val_f =open('/home/aistudio/work/val.txt','w')#生成验证文件
for i,content in enumerate(path_list):
    img,xml=content
    text=img+''+xml+'\n'
    if i<len(path_list)*ratio:
        train_f.write(text)#将图片路径写入并生成训练文档
    else:
        val_f.write(text)#将图片路径写入并生成验证文档
train_f.close()  # 关闭训练文档
val_f.close()  #关闭验证文档
```

这里我们首先引入需要的函数与操作系统,图片包括图像和标签两部分,确定了`xml`和`img`的位置后,定义出他们的路径,`img_path`,`xml_path`,二者组合成为图片路径列表`path_list`,这里包含了我们数据集中所有的图片,`ratio`代表比例系数,我们将按照比例将数据集划分为训练文件`train_f`和验证文件`val_f`两部分,这样我们的训练集和数据集就已经准备好了



接下来建立标签文档

```python 
label = ['cat']#设置类别标签,这里的标签为猫
with open('/home/aistudio/work/label_list.text','w') as f:#建立一个标签文档
    for text in label:
        f.write(text+'\n')
```

接着安装猫脸识别所需要

1. 安装`PaddleDetection`

```python
%cd /home/aistudio
!git clone https://gitee.com/PaddlePaddle/PaddleDetection.git -b develop --depth 1
```

2. 对`PaddleDetection`中`pip`进行更新,并下载相关依赖

```python
%cd ~/PaddleDetection
!pip install -U pip --user#对pip进行更新
!pip install --user -r requirements.txt#下载相关依赖
```

2. 安装`PaddleDet`

```!
!python setup.py install
!pip install paddleslim==2.1.1
```

在此过程中,可能会需要下载一个压缩包`!unzip -qoa filterpy-1.4.5.zip`

3. 编辑`voc`文件

```python
%cd 
!cp voc.yml ~/PaddleDetection/configs/datasets/voc.yml#指出voc所在位置
```

这里的`voc`文件是位于`/PaddleDetection/configs/datasets/`中,我们需要将其中的训练集,验证集,标签集的名字进行更改



调用我们的模型,进入模型训练阶段

```python
%cd ~/PaddleDetection/#进入PaddleDetection环境下
!export CUDA_VISIBLE_DEVICES=0#windows,Mac不需要执行该命令
!python tools/train.py -c configs/picodet/picodet_s_416_coco_lcnet.yml#训练模型的配置文件 --eval#开启边训练边测试的模式--use_vdl=True#打开VisualDL来记录训练数据 --vdl_log_dir="./output"#指定训练数据的存储路径
```

我们建立的训练模型中训练轮数`epoch`, 快照轮数`snapshot_epoch`  学习率`learningrate`,最大轮数`max epoch`,开始的权重系数`start factor`,梯度更新的次数`steps`均可以根据模型训练的实际情况进行更改



模型训练完毕后,我们继续进行模型的评估

```python
!python -u tools/eval.py -c configs/picodet/picodet_s_320_coco_lcnet.yml#评估模型的配置文件 -o weights=output/picodet_s_320_coco_lcnet/best_model.pdparams#最优模型的储存位置
```



这里我们首先调用我们事先存储的进行模型验证的代码来进行评估,评估较好的模型将自动储存在`PadddleDetection/output/picodet_s_320_coco_lcnet/best_model.pdparams`文件夹下

评估完成以后,我们也可以手动去进行一些图像的检测来查看模型的效果

```python
%cd ~PaddleDetection
!python -u tools/eval.py -c configs/picodet/picodet_s_320_coco_lcnet.yml#配置文件 -o weights=output/picodet_s_320_coco_lcnet/best_model.pdparams#配置文件的参数 --infer_img=/home/aistudio/....#这里填入图片名称jpg
```



这里我们要选择模型`configs/picodet/picodet_s_320_coco_lcnet.yml`,模型参数就选用`best_model.pdparams`,然后就可以填入自己准备的照片进行图像的检测