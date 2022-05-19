from PIL import Image
import numpy as np
import os
import cv2
np.seterr(divide='ignore', invalid='ignore')
import torch
import torchvision.transforms as transforms
from .model.deeplabv3.model.deeplabv3 import DeepLabV3
import shutil

#调色板，15种颜色
palette = [0, 200, 0,
           150, 250, 0,
           150, 200, 150,
           200, 0, 200,
           150, 0, 250,
           150, 150, 250,
           250, 200, 0,
           200, 200, 0,
           200, 0, 0,
           250, 0, 150,
           200, 150, 150,
           250, 150, 150,
           0, 0, 200,
           0, 150, 200,
           0, 200, 250,
           0, 0, 0]
zero_pad = 256 * 3 - len(palette)
for i in range(zero_pad):
    palette.append(0)

# 利用PIL的函数，将预测出来的图像分别上色，0-15对应15种不同的颜色
def colorize_mask(mask):
    mask_color = Image.fromarray(mask.astype(np.uint8)).convert('P')
    mask_color.putpalette(palette)
    return mask_color

def predict(net, im): # 预测结果
    with torch.no_grad():
        im = im.unsqueeze(0).cuda()
        out = net(im)
        pred = out.max(1)[1].squeeze().cpu().data.numpy()
        pred = colorize_mask(pred)
    return pred
#图像预处理
def img_transforms(img):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])
        ])
    img = transform(img)
    return img
#将一副大图像裁剪为224*224的若干小图像
def image_cut(input,output):
    data_list =[]
    path = input
    path_out = output
    img = cv2.imread(path)
    img_exp = np.pad(img, pad_width=((56, 224), (56, 224), (0, 0)), mode="constant", constant_values=(0, 0))
    img_shape = img.shape
    img_exp_shape = img_exp.shape
    h_step = img.shape[0] // 112
    w_step = img.shape[1] // 112
    #print(h_step, w_step)
    h_rest = -(img.shape[0] - 112 * h_step)
    w_rest = -(img.shape[1] - 112 * w_step)
    #print(h_rest, w_rest)
    image_list = []
    for h in range(h_step):
        for w in range(w_step):
            image_sample = img_exp[(h * 112):(h * 112 + 224),
                           (w * 112):(w * 112 + 224), :]
            image_list.append(image_sample)
        # if ori_image[(h * 112):(h * 112 + 224), -224:, :].shape == (224, 224, 3):
        image_list.append(img_exp[(h * 112):(h * 112 + 224), -224:, :])
    for w in range(w_step-1):
        image_list.append(img_exp[-224:, (w * 112):(w * 112 + 224), :])
    image_list.append(img_exp[-224:, -224:, :])
    for i in range(len(image_list)):
        cv2.imwrite(path_out + '/' + str(i) + '.png', image_list[i])
        data_list.append(str(i) + '.png')
    print("cut images saved in :" + path_out)
    return h_step,w_step,h_rest,w_rest,img_shape,img_exp_shape,data_list


#将224*224的若干小图像拼接成与原图大小相等的大图像
def image_comb(h_step,w_step,h_rest,w_rest,img_shape,img_exp_shape,outname,inpath):
    path = inpath
    ori_image = img_exp_shape
    predict_list = []
    files = os.listdir(path)
    for file in range(len(files)):
        file_path = path + '/' + str(file) + '.png'+"_result.png"
        im = cv2.imread(file_path)
        # predict_list.append(im[:, :, :])
        predict_list.append(im[:, :, :])
    count_temp = 0
    tmp = np.ones([ori_image[0] - 112, ori_image[1] - 112, ori_image[2]])
    for h in range(h_step):
        for w in range(w_step):
            tmp[h * 112:(h + 1) * 112, w * 112:(w + 1) * 112, :] = predict_list[count_temp][56:56 + 112, 56:56 + 112, :]
            count_temp += 1
        tmp[h * 112:(h + 1) * 112, w_rest:, :] = predict_list[count_temp][56:56 + 112, w_rest:, :]
        count_temp += 1
    for w in range(w_step - 1):
        tmp[h_rest:, (w * 112):(w * 112 + 112), :] = predict_list[count_temp][h_rest:, 56:56 + 112, :]
        count_temp += 1
    tmp[h_rest:, w_rest:, :] = predict_list[count_temp][h_rest:, w_rest:, :]
    print("combined image saved in :" + outname)
    img = tmp[:img_shape[0], :img_shape[1], :img_shape[2]]
    cv2.imwrite(outname,img )#存储拼接完后的图像

#预测函数
def run(img_path,master):
    #输出cuda是否可用
    print(torch.cuda.is_available())
    #获取计算机用户名
    path = r'C:\Users'
    a = os.listdir(path)[0]
    print(a)

    #预测部分
    net = DeepLabV3()
    #加载模型
    net.load_state_dict(torch.load(r'C:\Users\{}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\ai_detection\all_best.pkl'.format(a)))
    master.dlg.progressBar.setValue(20)
    #设置gpu加速
    net.cuda()   
    net.eval()
    in_path = img_path
    print('cutting......')
    #存储剪切图片的路径
    cut_path = r'C:\Users\{}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\ai_detection/cut'.format(a)
    #存储拼接图片的路径
    comb_path = r'C:\Users\{}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\ai_detection/comb'.format(a)
    #每预测一张大图像需要删除原本的文件夹并重新建一个新的文件夹
    shutil.rmtree(cut_path)
    shutil.rmtree(comb_path)
    os.mkdir(cut_path)
    os.mkdir(comb_path)
    #最终预测图的保存路径
    outname = in_path + '_predict.png'
    #开始裁剪大图像
    h_step,w_step,h_rest,w_rest,img_shape,img_exp_shape,data_list = image_cut(in_path,cut_path)
    master.dlg.progressBar.setValue(50)
    print('predicting......')
    #将文件夹中小图像放入网络进行预测
    for file in os.listdir(cut_path):
        img = cv2.imread(r'C:\Users\{}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\ai_detection//cut/{}'.format(a,file))
        img = img_transforms(img)
        pred = predict(net,img)
        pred.save(comb_path + "/" + file + "_result.png")
    master.dlg.progressBar.setValue(75)
    print('combining......')
    #调用拼接函数
    image_comb(h_step,w_step,h_rest,w_rest,img_shape,img_exp_shape,outname,comb_path)
