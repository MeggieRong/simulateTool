# coding:utf-8

import tkinter
import tkinter as tk
from tkinter import ttk, E, W
from tkinter import Menu
from tkinter import messagebox as mBox
from tkinter.filedialog import askdirectory, askopenfilename

from mapTool.pointToLine import pointToLine
from order.orderConvert import orderConvert
from stock.stockCreate import stockCreate, mirStockCreate
from yamlOperate.yamlOperate import yamlUpdate

win = tk.Tk()

win.title("SimulateTool")
win.resizable(1059, 762)
tabControl = ttk.Notebook(win)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='首页')

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='地图数据')

tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='订单转换')

tab4 = ttk.Frame(tabControl)
tabControl.add(tab4, text='库存生成')

tab5 = ttk.Frame(tabControl)
tabControl.add(tab5, text='参数配置')
path = tkinter.StringVar()

tab6 = ttk.Frame(tabControl)
tabControl.add(tab6, text='文件分类')

tab7 = ttk.Frame(tabControl)
tabControl.add(tab7, text='日志解析')

path = tkinter.StringVar()
path1 = tkinter.StringVar()
path2 = tkinter.StringVar()
path3 = tkinter.StringVar()
path4 = tkinter.StringVar()

tabControl.pack(expand=1, fill="both")

# ---------------Tab1控件------------------#
# ---------------Tab1控件------------------#

# ---------------Tab3控件--订单转换------------------#
monty2 = ttk.LabelFrame(tab3, text='基础参数')
monty2.grid(column=0, row=0, padx=8, pady=4)
monty2.grid(sticky=E + W)


def selectFile():
    global file_
    file_ = askopenfilename()
    path1.set(file_)


ttk.Label(monty2, width=18, text="源文件地址:").grid(column=0, row=1, sticky='W')
infoText1 = tkinter.Entry(monty2, textvariable=path1, width=18).grid(column=1,
                                                                     row=1)
tkinter.Button(monty2, text="文件选择", command=selectFile).grid(column=2, row=1)


def selectPath():
    global path_
    path_ = askdirectory()
    path2.set(path_)


ttk.Label(monty2, width=18, text="转换存放地址:").grid(column=0, row=2, sticky='W')
infoText2 = tkinter.Entry(monty2, textvariable=path2, width=18).grid(column=1,
                                                                     row=2)
tkinter.Button(monty2, text="路径选择", command=selectPath).grid(column=2, row=2)

monty22 = ttk.LabelFrame(tab3, text='订单参数')
monty22.grid(column=0, row=3, padx=8, pady=4)
monty22.grid(sticky=E + W)

ttk.Label(monty22, width=18, text="间隔时段:").grid(column=0, row=4, sticky='W')
intervalTime1 = tkinter.Entry(monty22, width=18)
intervalTime1.insert(0, '1')
intervalTime1.grid(column=1, row=4)

ttk.Label(monty22, width=18, text="间隔时长:").grid(column=0, row=5, sticky='W')
interval1 = tkinter.Entry(monty22, width=18)
interval1.insert(0, '5')
interval1.grid(column=1, row=5)

ttk.Label(monty22, width=18, text="截单时长:").grid(column=0, row=6, sticky='W')
deadline1 = tkinter.Entry(monty22, width=18)
deadline1.insert(0, '25')
deadline1.grid(column=1, row=6)

ttk.Label(monty22, width=18, text="是否组单:").grid(column=0, row=7, sticky='W')
reconbineChoose = tkinter.Entry(monty22, width=18)
reconbineChoose.insert(0, '0')
reconbineChoose.grid(column=1, row=7)


def clickMe7():
    sourceFile = file_
    targetFile = path_
    intervalTime = int(intervalTime1.get())
    interval = int(interval1.get())
    deadline = int(deadline1.get())
    ifRecombine = int(reconbineChoose.get())

    isFlag = orderConvert(sourceFile, targetFile, intervalTime, interval,
                          deadline, ifRecombine)

    if isFlag == True:
        mBox.showinfo('消息框', '订单和SKU映射文件转换完成，存放地址：{}'.format(targetFile))
    else:
        mBox.showinfo('消息框', '订单输入参数有错误，请检查！')


action = tkinter.Button(monty22, text="订单转换", command=clickMe7)
action.grid(column=2, row=7)

style = ttk.Style()
# ---------------Tab3控件--订单转换------------------#

# ---------------Tab4控件--库存生成------------------#
monty3 = ttk.LabelFrame(tab4, text='基础参数')
monty3.grid(column=0, row=0, padx=8, pady=4)
monty3.grid(sticky=E + W)


def selectFile():
    global file1_
    file1_ = askopenfilename()
    path1.set(file1_)


ttk.Label(monty3, width=18, text="订单文件地址:").grid(column=0, row=1, sticky='W')
fileText1 = tkinter.Entry(monty3, textvariable=path1, width=18).grid(column=1,
                                                                     row=1)
tkinter.Button(monty3, text="文件选择", command=selectFile).grid(column=2, row=1)


def selectFile():
    global file4_
    file4_ = askopenfilename()
    path4.set(file4_)


ttk.Label(monty3, width=18, text="sku映射文件地址:").grid(column=0,
                                                    row=2,
                                                    sticky='W')
fileText4 = tkinter.Entry(monty3, textvariable=path4, width=18).grid(column=1,
                                                                     row=2)
tkinter.Button(monty3, text="文件选择", command=selectFile).grid(column=2, row=2)


def selectLocFile():
    global file2_
    file2_ = askopenfilename()
    path2.set(file2_)


ttk.Label(monty3, width=18, text="货位文件地址:").grid(column=0, row=3, sticky='W')
fileText2 = tkinter.Entry(monty3, textvariable=path2, width=18).grid(column=1,
                                                                     row=3)
tkinter.Button(monty3, text="文件选择", command=selectLocFile).grid(column=2,
                                                                row=3)


def selectStockFile():
    global file3_
    file3_ = askopenfilename()
    path3.set(file3_)


ttk.Label(monty3, width=18, text="库存文件地址:").grid(column=0, row=4, sticky='W')
fileText3 = tkinter.Entry(monty3, textvariable=path3, width=18).grid(column=1,
                                                                     row=4)
tkinter.Button(monty3, text="文件选择", command=selectStockFile).grid(column=2,
                                                                  row=4)


def selectPath():
    global path_
    path_ = askdirectory()
    path.set(path_)


ttk.Label(monty3, width=18, text="转换存放地址:").grid(column=0, row=5, sticky='W')
fileText4 = tkinter.Entry(monty3, textvariable=path, width=18).grid(column=1,
                                                                    row=5)
tkinter.Button(monty3, text="路径选择", command=selectPath).grid(column=2, row=5)

ttk.Label(monty3, width=18, text="浮动范围（%）:").grid(column=0, row=6, sticky='W')
floatWideNum = tkinter.Entry(monty3, width=18)
floatWideNum.insert(0, '20')
floatWideNum.grid(column=1, row=6)

monty32 = ttk.LabelFrame(tab4, text='库存模型')
monty32.grid(column=0, row=7, padx=8, pady=4)
monty32.grid(sticky=E + W)

monty321 = ttk.LabelFrame(monty32, text='不混模式')
monty321.grid(column=0, row=8, padx=8, pady=4)
monty321.grid(sticky=E + W)

ttk.Label(monty321, width=16, text="固定数量:").grid(column=0, row=9, sticky='W')
nfixedNums = tkinter.Entry(monty321, width=18)
nfixedNums.insert(0, '')
nfixedNums.grid(column=1, row=9)

ttk.Label(monty321, width=16, text="最大数量:").grid(column=0, row=10, sticky='W')
nmaxNums = tkinter.Entry(monty321, width=18)
nmaxNums.insert(0, '')
nmaxNums.grid(column=1, row=10)

monty322 = ttk.LabelFrame(monty32, text='混箱模式')
monty322.grid(column=0, row=11, padx=8, pady=4)
monty322.grid(sticky=E + W)

ttk.Label(monty322, width=16, text="混箱程度:").grid(column=0, row=12, sticky='W')
ymixLevel = tkinter.Entry(monty322, width=18)
ymixLevel.insert(0, '1,2,4')
ymixLevel.grid(column=1, row=12)

ttk.Label(monty322, width=16, text="最大数量:").grid(column=0, row=13, sticky='W')
ymaixNums = tkinter.Entry(monty322, width=18)
ymaixNums.insert(0, '100')
ymaixNums.grid(column=1, row=13)

monty323 = ttk.LabelFrame(tab4, text='库存镜像')
monty323.grid(column=0, row=14, padx=8, pady=4)
monty323.grid(sticky=E + W)

ttk.Label(monty323, width=17, text="镜像源终点货位:").grid(column=0,
                                                    row=15,
                                                    sticky='W')
jxtext = tkinter.Entry(monty323, width=18)
jxtext.insert(0, '100')
jxtext.grid(column=1, row=15)

ttk.Label(monty323, width=17, text="镜像起点货位:").grid(column=0,
                                                   row=16,
                                                   sticky='W')
jxTtext = tkinter.Entry(monty323, width=18)
jxTtext.insert(0, '101')
jxTtext.grid(column=1, row=16)


def clickMe34():
    orderPath = file1_
    skuCodeMap = file4_
    locationsPath = file2_
    try:
        stockPath = file3_
    except NameError:
        stockPath = ''
    tarPath = path_
    floatWide = floatWideNum.get()
    fixedNums = nfixedNums.get()
    maxNums = nmaxNums.get()
    mixLevel = ymixLevel.get()
    maixNums = ymaixNums.get()

    isTFlag = stockCreate(orderPath, skuCodeMap, locationsPath, stockPath,
                          tarPath, floatWide, fixedNums, maxNums, mixLevel,
                          maixNums)

    if isTFlag == True:
        mBox.showinfo('消息框', '库存生成已完成，存放地址：{}'.format(tarPath))
    else:
        mBox.showinfo('消息框', '库存生成输入参数有错误，请检查！')


action = tkinter.Button(monty322, text="生成库存", command=clickMe34)
action.grid(column=2, row=13)


def clickMe35():
    tarPath = path_
    mirrorSource = jxtext.get()
    mirrorTar = jxTtext.get()

    isTFlag = mirStockCreate(tarPath, mirrorSource, mirrorTar)

    if isTFlag == True:
        mBox.showinfo('消息框', '库存生成已完成，存放地址：{}'.format(tarPath))
    else:
        mBox.showinfo('消息框', '库存生成输入参数有错误，请检查！')


action = tkinter.Button(monty323, text="库存镜像", command=clickMe35)
action.grid(column=2, row=16)

style = ttk.Style()
# ---------------Tab3控件--库存生成------------------#

# ---------------tab2控件--地图生成------------------#
monty4 = ttk.LabelFrame(tab2, text='基础参数')
monty4.grid(column=0, row=0, padx=8, pady=4)
monty4.grid(sticky=E + W)


def selectFile():
    global file_
    file_ = askopenfilename()
    path1.set(file_)


ttk.Label(monty4, width=18, text="源文件地址:").grid(column=0, row=1, sticky='W')
infoText1 = tkinter.Entry(monty4, textvariable=path1, width=18).grid(column=1,
                                                                     row=1)
tkinter.Button(monty4, text="文件选择", command=selectFile).grid(column=2, row=1)


def selectPath():
    global path_
    path_ = askdirectory()
    path2.set(path_)


ttk.Label(monty4, width=18, text="转换存放地址:").grid(column=0, row=2, sticky='W')
infoText2 = tkinter.Entry(monty4, textvariable=path2, width=18).grid(column=1,
                                                                     row=2)
tkinter.Button(monty4, text="路径选择", command=selectPath).grid(column=2, row=2)

ttk.Label(monty4, width=18, text="巷道方式（x/y):").grid(column=0,
                                                    row=3,
                                                    sticky='W')
infoText43 = tkinter.Entry(monty4, width=18)
infoText43.insert(0, 'x')
infoText43.grid(column=1, row=3)

ttk.Label(monty4, width=18, text="坐标点间距:").grid(column=0, row=4, sticky='W')
infoText44 = tkinter.Entry(monty4, width=18)
infoText44.insert(0, '3')
infoText44.grid(column=1, row=4)

monty42 = ttk.LabelFrame(tab2, text='Config参数')
monty42.grid(column=0, row=10, padx=8, pady=4)
monty42.grid(sticky=E + W)

ttk.Label(monty42, width=18, text="rows:").grid(column=0, row=11, sticky='W')
skutext49 = tkinter.Entry(monty42, width=18)
skutext49.insert(0, '80')
skutext49.grid(column=1, row=11)

ttk.Label(monty42, width=18, text="cols:").grid(column=0, row=12, sticky='W')
skutext410 = tkinter.Entry(monty42, width=18)
skutext410.insert(0, '60')
skutext410.grid(column=1, row=12)

monty43 = ttk.LabelFrame(tab2, text='充电参数')
monty43.grid(column=0, row=13, padx=8, pady=4)
monty43.grid(sticky=E + W)

ttk.Label(monty43, width=18, text="Most of the thetas:").grid(column=0,
                                                              row=14,
                                                              sticky='W')
skutext411 = tkinter.Entry(monty43, width=18)
skutext411.insert(0, '1.57')
skutext411.grid(column=1, row=14)

monty44 = ttk.LabelFrame(tab2, text='货位参数')
monty44.grid(column=0, row=15, padx=8, pady=4)
monty44.grid(sticky=E + W)

ttk.Label(monty44, width=18, text="首层高度:").grid(column=0, row=16, sticky='W')
skutext412 = tkinter.Entry(monty44, width=18)
skutext412.insert(0, '400')
skutext412.grid(column=1, row=16)

ttk.Label(monty44, width=18, text="层高:").grid(column=0, row=17, sticky='W')
skutext413 = tkinter.Entry(monty44, width=18)
skutext413.insert(0, '400')
skutext413.grid(column=1, row=17)

ttk.Label(monty44, width=18, text="层数:").grid(column=0, row=18, sticky='W')
skutext414 = tkinter.Entry(monty44, width=18)
skutext414.insert(0, '10')
skutext414.grid(column=1, row=18)

ttk.Label(monty44, width=18, text="深浅货位:").grid(column=0, row=19, sticky='W')
skutext415 = tkinter.Entry(monty44, width=18)
skutext415.insert(0, 'shallow')
skutext415.grid(column=1, row=19)


def fileConvert2():
    sourceFile = file_
    targetFile = path_
    channelType = infoText43.get()
    pointLength = infoText44.get()
    configRows = skutext49.get()
    configCols = skutext410.get()
    mostTheta = skutext411.get()
    firstHeight = skutext412.get()
    comHeight = skutext413.get()
    flowNums = skutext414.get()
    locations = skutext415.get()

    yNoHorizontal = []
    xNoVertical = []
    ypNoHorizontal = []
    xpNoVertical = []

    basicMap = [
        sourceFile, channelType, targetFile, pointLength, yNoHorizontal,
        xNoVertical, ypNoHorizontal, xpNoVertical
    ]
    othersList = [
        configRows, configCols, mostTheta, firstHeight, comHeight, flowNums,
        locations
    ]
    pointInfo = pointToLine(basicMap, othersList)

    mBox.showinfo(
        '消息框', '方案地图坐标点源文件地址:{},\n'
        '转换后的文件存放地址:{},\n'
        '巷道排列方式为:{} 方向平行,\n'
        '地图坐标点间最大距离为:{},\n'
        '水平方向不连线的坐标点Y坐标集合为:{},\n'
        '垂直方向不连线的坐标点X坐标集合为:{},\n'
        '水平方向相邻两点不连线的坐标点集合为:{},\n'
        '垂直方向相邻两点不连线的坐标点集合为:{}, \n'
        '根据方案源文件一共生成巷道：{} 条 \n'
        '方案源文件共有坐标点：{} 个，转换成功：{} 个，重复坐标点：{} 个 \n'
        '方案源文件转 adjacency_list 和 channelEE 文件成功，文件存放于:{}'.format(
            sourceFile, targetFile, channelType, pointLength, yNoHorizontal,
            xNoVertical, ypNoHorizontal, xpNoVertical, pointInfo[4],
            pointInfo[1], pointInfo[2], pointInfo[3], pointInfo[0]))


action = tkinter.Button(monty44, text="文件生成", command=fileConvert2)
action.grid(column=2, row=19)

style = ttk.Style()
# ---------------tab2控件--地图生成------------------#

# ---------------Tab5控件--参数配置------------------#
monty5 = ttk.LabelFrame(tab5, text='基础参数')
monty5.grid(column=0, row=0, padx=8, pady=4)
monty5.grid(sticky=E + W)


def selectPath():
    global path_
    path_ = askdirectory()
    path.set(path_)


ttk.Label(monty5, width=18, text="基础文件地址:").grid(column=0, row=1, sticky='W')
infoText1 = tkinter.Entry(monty5, textvariable=path, width=18).grid(column=1,
                                                                    row=1)
tkinter.Button(monty5, text="文件选择", command=selectPath).grid(column=2, row=1)

ttk.Label(monty5, width=18, text="项目配置名称:").grid(column=0, row=2, sticky='W')
skutext22 = tkinter.Entry(monty5, width=18)
skutext22.insert(0, 'JD1212-20200908.yaml')
skutext22.grid(column=1, row=2)


def selectTarPath():
    global path2_
    path2_ = askdirectory()
    path2.set(path2_)


ttk.Label(monty5, width=18, text="转换存放地址:").grid(column=0, row=3, sticky='W')
infoText2 = tkinter.Entry(monty5, textvariable=path2, width=18).grid(column=1,
                                                                     row=3)
tkinter.Button(monty5, text="路径选择", command=selectTarPath).grid(column=2,
                                                                row=3)

monty52 = ttk.LabelFrame(tab5, text='机器人参数')
monty52.grid(column=0, row=4, padx=8, pady=4)
monty52.grid(sticky=E + W)

ttk.Label(monty52, width=18, text="数量:").grid(column=0, row=5, sticky='W')
skutext8 = tkinter.Entry(monty52, width=18)
skutext8.insert(0, '60')
skutext8.grid(column=1, row=5)

ttk.Label(monty52, width=18, text="背篓数:").grid(column=0, row=6, sticky='W')
skutext9 = tkinter.Entry(monty52, width=18)
skutext9.insert(0, '8')
skutext9.grid(column=1, row=6)

ttk.Label(monty52, width=10, text="浮动范围:").grid(column=0, row=7, sticky='W')
skutext10 = tkinter.Entry(monty52, width=18)
skutext10.insert(0, '5')
skutext10.grid(column=1, row=7)

ttk.Label(monty52, width=10, text="初始朝向:").grid(column=0, row=8, sticky='W')
skutext21 = tkinter.Entry(monty52, width=18)
skutext21.insert(0, '0')
skutext21.grid(column=1, row=8)

monty53 = ttk.LabelFrame(tab5, text='操作台参数')
monty53.grid(column=0, row=9, padx=8, pady=4)
monty53.grid(sticky=E + W)

ttk.Label(monty53, width=10, text="数量:").grid(column=0, row=10, sticky='W')
skutext11 = tkinter.Entry(monty53, width=18)
skutext11.insert(0, '5')
skutext11.grid(column=1, row=10)

ttk.Label(monty53, width=18, text="分播槽位数量:").grid(column=0, row=11, sticky='W')
skutext19 = tkinter.Entry(monty53, width=18)
skutext19.insert(0, '30')
skutext19.grid(column=1, row=11)

ttk.Label(monty53, width=18, text="单品订单限位:").grid(column=0, row=12, sticky='W')
skutext20 = tkinter.Entry(monty53, width=18)
skutext20.insert(0, '0')
skutext20.grid(column=1, row=12)

ttk.Label(monty53, width=18, text="操作台模式:").grid(column=0, row=13, sticky='W')
skutext12 = tkinter.Entry(monty53, width=18)
skutext12.insert(0, 'Normal')
skutext12.grid(column=1, row=13)

monty54 = ttk.LabelFrame(tab5, text='模型参数')
monty54.grid(column=0, row=14, padx=8, pady=4)

monty541 = ttk.LabelFrame(monty54, text='固定模式')
monty541.grid(column=0, row=15, padx=8, pady=4)
monty541.grid(sticky=E + W)

ttk.Label(monty541, width=18, text="固定每料箱处理耗时:").grid(column=0,
                                                      row=16,
                                                      sticky='W')
skutext13 = tkinter.Entry(monty541, width=18)
skutext13.insert(0, '22.8')
skutext13.grid(column=1, row=16)

monty542 = ttk.LabelFrame(monty54, text='模型公式')
monty542.grid(column=0, row=17, padx=8, pady=4)
monty542.grid(sticky=E + W)

ttk.Label(monty542, width=18, text="固定拣选1个SKU耗时:").grid(column=0,
                                                        row=18,
                                                        sticky='W')
skutext14 = tkinter.Entry(monty542, width=18)
skutext14.insert(0, '0.0')
skutext14.grid(column=1, row=18)

ttk.Label(monty542, width=18, text="固定扫描1个SKU耗时:").grid(column=0,
                                                        row=19,
                                                        sticky='W')
skutext15 = tkinter.Entry(monty542, width=18)
skutext15.insert(0, '2.3')
skutext15.grid(column=1, row=19)

ttk.Label(monty542, width=18, text="配单1行耗时:").grid(column=0,
                                                   row=20,
                                                   sticky='W')
skutext16 = tkinter.Entry(monty542, width=18)
skutext16.insert(0, '3.5')
skutext16.grid(column=1, row=20)

ttk.Label(monty542, width=18, text="拣选1件耗时:").grid(column=0,
                                                   row=21,
                                                   sticky='W')
skutext17 = tkinter.Entry(monty542, width=18)
skutext17.insert(0, '4.0')
skutext17.grid(column=1, row=21)

ttk.Label(monty542, width=18, text="移除1个空箱耗时:").grid(column=0,
                                                     row=22,
                                                     sticky='W')
skutext18 = tkinter.Entry(monty542, width=18)
skutext18.insert(0, '1.0')
skutext18.grid(column=1, row=22)

ttk.Label(monty52, width=18, text="是否正常充放电:").grid(column=0,
                                                   row=23,
                                                   sticky='W')
skutext26 = tkinter.Entry(monty52, width=18)
skutext26.insert(0, 'yes')
skutext26.grid(column=1, row=23)


ttk.Label(monty52, width=18, text="浮动范围的步长:").grid(column=0,
                                                   row=24,
                                                   sticky='W')
skutext23 = tkinter.Entry(monty52, width=18)
skutext23.insert(0, '1')
skutext23.grid(column=1, row=24)

ttk.Label(monty53, width=18, text="操作台休息开始时间点").grid(column=0,
                                                     row=14,
                                                     sticky='W')
skutext24 = tkinter.Entry(monty53, width=18)
skutext24.insert(0, '0, 12, 18')
skutext24.grid(column=1, row=14)

ttk.Label(monty53, width=18, text="操作台休息结束时间点").grid(column=0,
                                                     row=15,
                                                     sticky='W')
skutext25 = tkinter.Entry(monty53, width=18)
skutext25.insert(0, '7,13.5,19')
skutext25.grid(column=1, row=15)


ttk.Label(monty53, width=18, text="输送线缓存位数量:").grid(column=0,
                                                    row=25,
                                                    sticky='W')
skutext27 = tkinter.Entry(monty53, width=18)
skutext27.insert(0, 10)
skutext27.grid(column=1, row=25)

ttk.Label(monty53, width=18, text="人的拣选位:").grid(column=0,
                                                 row=26,
                                                 sticky='W')
skutext28 = tkinter.Entry(monty53, width=18)
skutext28.insert(0, 5)
skutext28.grid(column=1, row=26)


ttk.Label(monty53, width=18, text="使用卸料机的操作台:").grid(column=0,
                                                     row=27,
                                                     sticky='W')
skutext29 = tkinter.Entry(monty53, width=18)
skutext29.insert(0, "1,2,3")
skutext29.grid(column=1, row=27)


def clickMe4():
    curPath = path_
    configName = skutext22.get()
    tarPath = path2_
    kubotNums = int(skutext8.get())
    trayNums = int(skutext9.get())
    fluctuateNums = int(skutext10.get())
    fluctuateNumsStep = int(skutext23.get())
    robotTheta = skutext21.get()
    stationNums = int(skutext11.get())
    modelType = skutext12.get()
    stationBreakBegin = skutext24.get()
    stationBreakEnd = skutext25.get()
    fixedTime = float(skutext13.get())
    fixedPick = float(skutext14.get())
    fixedScann = float(skutext15.get())
    minPick = float(skutext16.get())
    payOrder = float(skutext17.get())
    pickItem = float(skutext18.get())
    slotNum = int(skutext19.get())
    slotLimit = int(skutext20.get())
    kubotIfCharge = str(skutext26.get())
    conveyerBinCacheNum = skutext27.get()
    staffPickLocation = skutext28.get()
    useHaiportStation = skutext29.get()
    stationConfig = [stationNums, slotNum, slotLimit]
    stationList = [
        stationNums, modelType, fixedTime, fixedPick, fixedScann,
        minPick, payOrder, pickItem, stationConfig, stationBreakBegin, stationBreakEnd,
    ]  # 工作站参数

    yamlUpdate(curPath, configName, tarPath, kubotNums, trayNums,
               fluctuateNums, fluctuateNumsStep, robotTheta, stationList,
               kubotIfCharge, conveyerBinCacheNum, staffPickLocation, useHaiportStation)


action = tkinter.Button(monty542, text="生成参数", command=clickMe4)
action.grid(column=2, row=22)

style = ttk.Style()

# ---------------Tab5控件------------------#


# ----------------菜单栏-------------------#
def _quit():
    win.quit()
    win.destroy()
    exit()


menuBar = Menu(win)
win.config(menu=menuBar)

fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="新建")
fileMenu.add_separator()
fileMenu.add_command(label="退出", command=_quit)
menuBar.add_cascade(label="文件", menu=fileMenu)


def _msgBox1():
    mBox.showwarning('Warning Box', '提示：运行前请先阅读帮助信息')


msgMenu = Menu(menuBar, tearoff=0)
msgMenu.add_command(label="提示", command=_msgBox1)
menuBar.add_cascade(label="帮助", menu=msgMenu)
# ----------------菜单栏-------------------#

# start
win.mainloop()
