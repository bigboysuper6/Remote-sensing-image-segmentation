#获取标记区域
    def ReadBlock(self):
        print("读取区域")
        i = self.iface.activeLayer()
        for feat in i.getFeatures():
            geom = feat.geometry()
            t = geom.asPolygon()
            pxlist = []
            pylist = []
            for p in t[0]:
                pxlist.append(p.x())
                pylist.append(p.y())
            print('--------')
            print(self.PWd)
            print(self.PHg)
            # 像素值
            pminX=(float(float(min(pxlist))-self.StartX)/self.Wd)*self.PWd#min x
            pmaxX=(float(float(max(pxlist))-self.StartX)/self.Wd)*self.PWd #max x
            pminY=(float(float(min(pylist))- self.StartY)/self.Hg)*self.PHg #min y
            pmaxY = (float(float(max(pylist)) - self.StartY) / self.Hg) * self.PHg  # max y
            print("compute finished")
            self.PblockminX.append(pminX)
            self.PblockmaxX.append(pmaxX)
            self.PblockminY.append(pminY)
            self.PblockmaxY.append(pmaxY)
            print('min x y:', min(pxlist), max(pylist))  # 先验区左上xy坐标
            print('min x y px:', self.PblockminX, self.PblockminY)  # 先验区左上px xy坐标
            print('max x y:', max(pxlist), min(pylist))  # 先验区右下xy坐标
            print('max x y px:', self.PblockmaxX,self.PblockmaxY)  # 先验区右下px xy坐标
            #剪切圖片
            path = self.iFilepath  # 读取文件地址
            save_path = self.oFolderpath  # 保存文件地址
            img = cv2.imread(path, 1)
            print(img)
            print(self.PblockminX)
            # 坐标1
            x1 = int(self.PblockminX[0])
            y1 = int(self.PHg - self.PblockminY[0])
            # 坐标2
            x2 = int(self.PblockmaxX[0])
            y2 = int(self.PHg - self.PblockmaxY[0])
            # 计算宽，高
            w = x2 - x1
            h = y2 - y1
            print(w)
            print(h)
            img = img[y2:y1, x1:x2, :]
            cv2.imshow(img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # print(img)
            # cv2.imwrite(save_path + '/1.png', img)
            # # 原始图片展示
            # img = QPixmap(self.oFolderpath + '/1.png')
            # scarePixmap = img.scaled(471, 321, aspectRatioMode=Qt.KeepAspectRatio)
            # self.dlg.showP.setPixmap(scarePixmap)
    #获取数据============

    # 获取点的坐标值
    def readPoint(self):
        print("获取点的坐标")
        # 获取点集坐标
        i = self.iface.activeLayer()
        if i.providerType() == 'memory':
            xlist=[]
            ylist=[]
            pxlist = []
            pylist = []
            for feat in i.getFeatures():
                geom = feat.geometry()
                t = geom.asMultiPoint()
                xlist.append(t[0][0])
                ylist.append(t[0][1])
                pxlist.append(float(float(t[0][0]-self.StartX)/self.Wd)*self.PWd)
                pylist.append(float(float(t[0][1]-self.StartY)/self.Hg)*self.PHg)
            print("地理坐标系：")
            print(xlist)  # 所有点的x坐标
            print(ylist)  # 所有点的y坐标
            print("起始点X Y")
            print(self.StartX)
            print(self.StartY)
            print("宽 高：")
            print(self.Wd)
            print(self.Hg)
            print("像素宽 高：")
            print(self.PWd)
            print(self.PHg)
            print("像素点：")
            print(pxlist)  # 所有点的x坐标
            print(pylist)  # 所有点的y坐标
            self.PpointminX.append(int(min(pxlist)))
            self.PpointminY.append(int(min(pylist)))
            self.PpointmaxX.append(int(max(pxlist)))
            self.PpointmaxY.append(int(max(pylist)))


            # 显示剪切图像
            path = self.iFilepath  # 读取文件地址
            print(path)
            save_path = self.oFolderpath  # 保存文件地址
            print(save_path)
            img = cv2.imread(path)
            print(self.PpointminX)            # 坐标1
            x1 = int(self.PpointminX[0])
            y1 = int(self.PHg - self.PpointminY[0])
            # 坐标2
            x2 = int(self.PpointmaxX[0])
            y2 = int(self.PHg - self.PpointmaxY[0])
            # 计算宽，高
            w = x2 - x1
            h = y2 - y1
            print(w)
            print(h)
            img = img[y2:y1, x1:x2, :]
            print(img)
            cv2.imwrite(save_path + '/2.png', img)
            # 原始图片展示
            img = QPixmap(save_path + '/2.png')
            scarePixmap = img.scaled(471, 321, aspectRatioMode=Qt.KeepAspectRatio)
            self.dlg.showP.setPixmap(scarePixmap)


