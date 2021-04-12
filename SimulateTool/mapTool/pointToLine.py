#coding:utf-8

import os

from util.fileConvertFunction import fileConvertFunction
from util.pointToLineOperate import creatChannel, creatAdjacencyList, writerFiles, writeConfig, chargeListFile, \
    writeCharge, writeLocations, writeQrCode, writeStatePoints, writeOthers


def pointToLine(basicMap, othersList):
    sourcePath = basicMap[0]
    curpath = basicMap[2]
    channelType = basicMap[1]
    pointLength = basicMap[3]
    yNoHorizontal = basicMap[4]
    xNoVertical = basicMap[5]
    ypNoHorizontal = basicMap[6]
    xpNoVertical = basicMap[7]

    # csv转换
    fileConvertFunction(sourcePath, curpath)
    csvPath = curpath + '\mapData.csv'
    pointInfo = []

    # 生成channelEE
    channelDict = creatChannel(csvPath, channelType, pointLength)

    # 生成adjacencylist
    adjacencyList, pInfo = creatAdjacencyList(csvPath, channelType, pointLength, yNoHorizontal, xNoVertical, ypNoHorizontal, xpNoVertical)

    # 写 adjaceney 和 channelEE 文件
    writerFiles(channelDict, adjacencyList, curpath)

    pointInfo.append(curpath)
    for k in pInfo:
        pointInfo.append(k)
    pointInfo.append(len(channelDict))

    # 写config.yaml文件
    rows = othersList[0]
    cols = othersList[1]
    writeConfig(curpath, rows, cols)

    # 写rest_station.json文件
    rtTheta = othersList[2]
    xyDict = chargeListFile(sourcePath)
    writeCharge(curpath, xyDict, rtTheta)

    # 写locations.csv文件
    locDir = basicMap[1]
    locationInfo = othersList[3:]
    writeLocations(locDir, locationInfo, sourcePath, curpath)

    # 写其他空文件kubot.csv/obstacle.csv/qr_code.csv/shelf.csv
    # 写qr_code.csv
    qrFilePath = os.path.join(curpath, "./adjacent_list.csv")
    writeQrCode(qrFilePath, curpath)

    # 写state_points.json文件
    spPath = os.path.join(curpath, "./adjacency_list.in")
    writeStatePoints(spPath, curpath)

    # 写其他空文件
    writeOthers(curpath)

    return pointInfo

if __name__ == '__main__':
    # sourceFile = 'E:\业务测试\项目需求\Youyiku地图\828地图数据\优衣库点位(模拟版）(1).xls'
    # sourceFile = 'E:\业务测试\项目需求\武汉新宁\地图坐标\SMT区域V6.1 for SIMU.csv'
    sourceFile = r'E:\测试相关\业务测试\项目需求\百世bilibili\地图\new地图坐标点.xlsx'
    targetFile = r'E:\测试相关\业务测试\项目需求\百世bilibili\地图\新建文件夹'
    channelType = 'y'
    pointLength = 1.5
    yNoHorizontal = [56.63]
    xNoVertical = [1.58, 2.78, 6.31, 7.22, 9.2, 11.56, 13.93, 16.29, 18.66, 21.02, 23.39, 25.75, 28.12, 32.85]
    # xNoVertical = []
    ypNoHorizontal = []
    xpNoVertical = []
    # yNoHorizontal = [20.6,93.82,97.2]  # 水平方向不连线的点
    # xNoVertical = [73.04]  # 垂直方向不连线的点
    # ypNoHorizontal = [[['57.12', '92.92'], ['58.97', '92.92']]]  # 水平方向相邻两点不连
    # xpNoVertical = [[['40.84', '82.69'], ['40.84', '85.26']]]  # 垂直方向相邻两点不连
    configRows = 80
    configCols = 60
    mostTheta = 1.57
    firstHeight = 0
    comHeight = 400
    flowNums = 10
    locations = 'shallow'

    basicMap = [sourceFile, channelType, targetFile, pointLength, yNoHorizontal, xNoVertical, ypNoHorizontal,
                xpNoVertical]
    othersList = [configRows, configCols, mostTheta, firstHeight, comHeight, flowNums, locations]
    pointToLine(basicMap, othersList)