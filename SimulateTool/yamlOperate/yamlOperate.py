# encoding: utf-8

import os
import yaml

from util.updateFile import copy_dirs, kubotFile, del_file, stationFile

# 简单转格式


def stringListConvertIntoInt(listdemo):
    listdemo = listdemo.split(',')
    listdemo = [float(i) for i in listdemo]
    return listdemo


def yamlUpdate(curPath, configName, tarPath, kubotNums, trayNums, fluctuateNums, fluctuateNumsStep, robotTheta, stationList, kubotIfCharge):
    # 复制配置文件
    cpPath = curPath + '2'
    copy_dirs(curPath, cpPath)

    # 读取配置文件
    filePath = os.path.join(curPath, configName)
    f = open(filePath, 'r', encoding='utf-8')
    cfg = f.read()

    # 转换字典
    d = yaml.load(cfg, Loader=yaml.Loader)

    # 计算机器人最大最小数
    kubotMin = kubotNums - fluctuateNums
    kubotMax = kubotNums + fluctuateNums + 1

    # 操作台数量计算
    stationNs = stationList[0] + 1
    stationNumList = []
    for j in range(1, stationNs):
        stationNumList.append(j)
    stationNumDict = {1: stationNumList}

    # 生成机器人数量遍历文件
    if kubotMin > 0 and kubotMax >= kubotMin:
        for i in range(kubotMin, kubotMax, fluctuateNumsStep):
            # 创建遍历文件夹
            folderName = '/robotNum_' + str(i)
            dataPath = tarPath + folderName
            os.makedirs(dataPath)
            copy_dirs(cpPath, dataPath)

            # 修改配置文件名
            d['kConfiguration'] = folderName[1:]

            # 修改机器人参数
            d['kTestKubots'] = i
            d['Kubot Tray Number'] = trayNums

            # 修改機器人是否正常充放電
            if kubotIfCharge == 'yes':
                pass
            else:
                d['kMaxWorkingSecond'] = 2160099999999

            # 修改操作台参数
            d['Bin Picking Model Type'] = stationList[1]
            d['Bin Picking Fixed Time'] = stationList[2]
            d['Station Picking Model'] = stationNumDict

            # 操作台模型公式
            d['Fixed Picking Time Per SKU'] = stationList[3]
            d['Fixed Scanning Time Per SKU'] = stationList[4]
            d['Min Picking Time Per SKU'] = stationList[5]
            d['Pay Order Coefficient'] = stationList[6]
            d['Pick Item Number Coefficient'] = stationList[7]

            # 操作台休息是時間
            if not d.__contains__('Operator Break Starting Time'):
                d.update({'Operator Break Starting Time': [
                    i * 3600 for i in stringListConvertIntoInt(stationList[9])]})
                d.update({'Operator Break Ending Time': [
                    i * 3600 for i in stringListConvertIntoInt(stationList[10])]})
            else:
                d['Operator Break Starting Time'] = [
                    i * 3600 for i in stringListConvertIntoInt(stationList[9])]
                d['Operator Break Ending Time'] = [
                    i * 3600 for i in stringListConvertIntoInt(stationList[10])]

            # 更新配置文件
            configFileName = folderName[1:] + '.yaml'
            newFilePath = os.path.join(dataPath, configFileName)
            print(newFilePath)
            with open(newFilePath, 'w', encoding='utf-8') as nf:
                yaml.dump(d, nf)
                print('Configuration update completed.')

            # 更新联动机器人文件
            kubotFile(dataPath, i, robotTheta)

            # 更新联动操作台文件
            stationConfig = stationList[8]
            stationFile(dataPath, stationConfig)

    del_file(cpPath)


if __name__ == "__main__":
    # configData
    curPath = os.getcwd() + '\configData'   # 所有配置文件（包括地图、config、data）

    # 机器人参数
    kubotNums = 60  # 机器人数量
    trayNums = 8    # 背篓数量
    fluctuateNums = 3   # 浮动数量
    robotTheta = 0

    # 工作站参数
    stationNums = 5    # 工作站数量
    modelType = 'Normal'    # 工作站模式
    fixedTime = 22.8
    fixedPick = 0.0
    fixedScann = 2.3
    minPick = 3.5
    payOrder = 4.0
    pickItem = 1.0

    slotNum = 30
    slotLimit = 0
    stationConfig = [stationNums, slotNum, slotLimit]
    stationList = [stationNums, modelType, fixedTime, fixedPick,
                   fixedScann, minPick, payOrder, pickItem, stationConfig]
    kubotIfCharge = 'yes'
    configName = ''
    tarPath = ''
    stationBreakBegin = ''
    stationBreakEnd = ''
    fluctuateNumsStep = ''
    # 配置修改带联动
    yamlUpdate(curPath, configName, tarPath, kubotNums, trayNums, stationBreakBegin,
               stationBreakEnd,  fluctuateNums, fluctuateNumsStep, robotTheta, kubotIfCharge)

    # 机器人文件修改
    # kubotFile(curPath, kubotNums)

    # 工作站软件修改
    # dataPath = 'E:\JavaPython\pycharm_workspace\Tools\SimulateTool/robotNum_63'
    # # stationFile(dataPath, stationConfig)
