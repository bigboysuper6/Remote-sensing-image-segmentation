Plugin Builder Results

Your plugin AIDetection was created in:
    C:/Users/Administrator/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins\ai_detection

Your QGIS plugin directory is located at:
    C:/Users/Administrator/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins

What's Next:

  * Copy the entire directory containing your new plugin to the QGIS plugin
    directory

  * Compile the resources file using pyrcc5

  * Run the tests (``make test``)

  * Test the plugin by enabling it in the QGIS plugin manager

  * Customize it by editing the implementation file: ``AI_Detection.py``

  * Create your own custom icon, replacing the default icon.png

  * Modify your user interface by opening AIDetection_dialog_base.ui in Qt Designer

  * You can use the Makefile to compile your Ui and resource files when
    you make changes. This requires GNU make (gmake)

For more information, see the PyQGIS Developer Cookbook at:
http://www.qgis.org/pyqgis-cookbook/index.html

(C) 2011-2018 GeoApt LLC - geoapt.com

核心文件有两个一个是AI_Detection.py，一个是predict.py,
其中AI_Detection.py是将模型与QGIS插件对接的文件，主要功能
是获取关键信息并调用各个文件。
predict.py则是deeplabv3网络的预测部分，主要负责模型的裁剪，拼接等。
model文件夹存储的是deeplabv3各个模块的pytorch代码
cut和comb文件夹分别存储裁剪后的图片，和裁剪后的图片预测结果，最终图像会存储在用户选择的文件夹中。
其他文件时QGIS二次开发的插件pyqt界面代码，或者自带的一些文件