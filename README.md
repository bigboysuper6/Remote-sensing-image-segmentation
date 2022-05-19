# Read Me

概述:利用插件的形式在 QGIS 中实现卫星图像分割,技术:python,pytorch,opencv,cuda,pyqt 用的是 deeplabv3 分割网络,其中主干网络是 resnet18,选择resnet18的原因是单张卫星图可能非常大,resnet108或其他的话可能导致分割速度很慢.

**操作视频展示**

[视频](https://github.com/bigboysuper6/Remote-sensing-image-segmentation/blob/main/ImgVideo/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91.mp4),点击 view raw 下载观看

**界面展示**
  
![](https://github.com/bigboysuper6/Remote-sensing-image-segmentation/blob/main/ImgVideo/%E5%9B%BE%E7%89%87%201.png)
  
![](https://github.com/bigboysuper6/Remote-sensing-image-segmentation/blob/main/ImgVideo/%E5%9B%BE%E7%89%87%202.png)
  
![](https://github.com/bigboysuper6/Remote-sensing-image-segmentation/blob/main/ImgVideo/%E5%9B%BE%E7%89%873.png)

需要更详细的说明请下载 说明.zip

[说明.zip]( https://wwd.lanzouf.com/iD4WB053eb6f ）

说明.zip下的 all_best.pkl需要放在 ai_detection 目录下，为权重文件。

同时还包含编译安装文档，ppt，操作手册，演示视频。
