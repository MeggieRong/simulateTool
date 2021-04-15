# encoding: utf-8

import csv
import json
import operator
import os
import shutil
import pandas as pd
import numpy as np

def kubotFile(dataPath, kubotNums, robotTheta):
    # 机器人初始位置集
    kubotList = []
    kubotID = 0    # 机器人ID

    # 读取巷道文件
    chfilePath = os.path.join(dataPath, "channelEE.txt")
    rf = open(chfilePath, 'r', encoding='utf-8')
    lines = rf.readlines()

    # 生成机器人初始位
    for line in lines:
        robotStates = line.split(':')[1]
        xyList = robotStates.split(',')
        kubotList.append([xyList[0], xyList[1]])
        y2 = xyList[3].replace('\n', '')
        kubotList.append([xyList[2], y2])

    # 写kubot文件
    kubotFilePath = os.path.join(dataPath, "kubot.txt")
    wf = open(kubotFilePath, 'w+', encoding='utf-8')
    for node in kubotList:
        kubotID += 1
        kubotNode = str(kubotID) + ',' + \
            str(node[0]) + ',' + str(node[1]) + ',' + str(robotTheta)
        wf.write(kubotNode)

        if kubotID == kubotNums:
            print('Kubot file update completed.')
            break
        else:
            wf.write('\n')


def judgeIfTentaclesType():
    xListAllmap = []
    yListAllmap = []
    def getOriginStationInfo():
        global xListAllmap, yListAllmap, mapFile, stationDf
        mapFile = pd.read_excel(
            'C:\\Users\\admin\\Desktop\\test\\PD坐标点属性.xlsx', '普通点', header=None, names=['no', 'color', 'x', 'y', 'function'])
        del mapFile['no']
        del mapFile['color']

        unloadList = mapFile[mapFile.function == '输送线放货点'][['x', 'y']]
        loadList = mapFile[mapFile.function == '输送线取货点'][['x', 'y']]
        unloadList.reset_index(inplace=True, drop=True)
        loadList.reset_index(inplace=True, drop=True)
        stationList = list(range(1, len(loadList)+1))
        stationDf = pd.DataFrame()
        stationDf['stationNo'] = stationList
        stationDf['xUnload'] = unloadList.x
        stationDf['yUnload'] = unloadList.y
        stationDf['xLoad'] = loadList.x
        stationDf['yLoad'] = loadList.y

        # 获取全地图的x和y,去重并且各自做升序
        xListAllmap = sorted(
            set(mapFile.x[1:].apply(lambda x: float(x)).to_list()), reverse=False)
        yListAllmap = sorted(
            set(mapFile.y[1:].apply(lambda y: float(y)).to_list()), reverse=False)

        return stationDf

    # 触角型haiport操作台

    def haiportStationTheta():
        global stationDf
        stationDf['theta'] = np.nan
        for i in range(0, len(stationDf)):
            if stationDf.at[i, 'xLoad'] in xListAllmap[:2]:
                stationDf.at[i, 'theta'] = 0
            elif stationDf.at[i, 'xLoad'] in xListAllmap[-2:]:
                stationDf.at[i, 'theta'] = -3.14
            elif stationDf.at[i, 'yLoad'] in yListAllmap[:2]:
                stationDf.at[i, 'theta'] = 1.57
            else:
                stationDf.at[i, 'theta'] = -1.57
        return stationDf

    # 非触角型操作台

    def conveyorStationTheta():
        if stationDf.xLoad == stationDf.xUnload:
            if stationDf.yLoad > stationDf.yUnload:
                stationDf['theta'] = 1.57
            else:
                stationDf['theta'] = -1.57
        elif stationDf.xLoad > stationDf.xUnload:
            stationDf['theta'] = -3.14
        else:
            stationDf['theta'] = 0
        return stationDf

    stationDf = getOriginStationInfo()
    specialStation = stationDf[:1]

    if specialStation.xUnload[0] == specialStation.xLoad[0]:
        specialYMapFile = mapFile[mapFile.x == specialStation.xUnload[0]]
        yList = sorted(list(set(specialYMapFile.y.to_list())), reverse=False)

        if abs(yList.index(specialStation.yUnload) - yList.index(specialStation.yLoad)) == 1:
            print('map have outside station')
            # 同x坐标，y轴索引相邻，说明没有中间点，属于触角型操作台
            stationDf = haiportStationTheta()
        else:
            print('map have inside station')
            stationDf = conveyorStationTheta()
    else:
        specialxMapFile = mapFile[mapFile.y == specialStation.yUnload[0]]
        xList = sorted(list(set(specialxMapFile.x.to_list())), reverse=False)
        if abs(xList.index(specialStation.xUnload[0]) - xList.index(specialStation.xLoad[0])) == 1:
            print('map have outside station')
            # 同y坐标，x轴索引相邻，说明没有中间点，属于触角型操作台
            stationDf = haiportStationTheta()
        else:
            print('map have inside station')
            stationDf = conveyorStationTheta()
    data_list = []
    for i in range(0, len(stationDf)):
        data_list.append(stationDf.iloc[i].to_list())
    return data_list

data_list = ''
def stationFile(dataPath, stationConfig):
    stationList = []
    stationNums = stationConfig[0]
    for i in range(1, int(stationNums) + 1):
        stationDict = {}
        stationID = i
        stationType = 'Conveyer_JD'
        location = {'x': 0, 'y': 0}
        slotNum = stationConfig[1]
        slotLimit = stationConfig[2]
        orderOnly = False
        # ustateID = 0
        # lstateID = 0
        conveyorHeight = 0.6
        # conveyorTheta = 0

        # 读取配置文件
        try:
            filePath = os.path.join(dataPath, "station.csv")
            # 如果dataPath没有,说明是标准的操作台，需要动态去识别
            rf = open(filePath, 'r', encoding='utf-8')
            data_list = [i for i in csv.reader(rf)]
        except:
            data_list = judgeIfTentaclesType()

            x = data_list[i - 1][1]
            y = data_list[i - 1][2]
            location['x'] = float(x)
            location['y'] = float(y)
            conveyorTheta = float(data_list[i - 1][5])
            ustateID = searchPointID(dataPath, conveyorTheta, location)
            lx = data_list[i - 1][3]
            ly = data_list[i - 1][4]
            statPointDict = {'x': float(lx), 'y': float(ly)}

            lstateID = searchPointID(dataPath, conveyorTheta, statPointDict)
            stationDict['station id'] = stationID
            stationDict['type'] = stationType
            stationDict['location'] = location
            stationDict['order slot number'] = slotNum
            stationDict['single-item order slot limit'] = slotLimit
            stationDict['single-item order only'] = orderOnly
            stationDict['unload state id'] = ustateID
            stationDict['load state id'] = lstateID
            stationDict['conveyor height'] = conveyorHeight
            stationDict['conveyor theta'] = conveyorTheta

            stationList.append(stationDict)

    # 写工作站配置文件
    configPath = os.path.join(dataPath, "station_config.json")
    with open(configPath, "w") as wf:
        json.dump(stationList, wf)
        print('Station file update completed.')

# 文件夹下文件复制到另一目录


def copy_dirs(src_path, target_path):
    file_count = 0
    source_path = os.path.abspath(src_path)
    target_path = os.path.abspath(target_path)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target_path)
                file_count += 1
    return int(file_count)

# 删除文件夹


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
    os.rmdir(path)


def searchPointID(dataPath, conveyorTheta, pointDict):
    id = 0
    filePath = os.path.join(dataPath, "state_points.json")
    rf = open(filePath, 'r', encoding='utf-8')
    pointList = json.load(rf)
    for i in pointList:
        statePoint = dict(i)
        stateId = statePoint['state id']
        statePosition = dict(statePoint['state position'])
        theta = statePosition['theta']
        positionDict = {'x': statePosition['x'], 'y': statePosition['y']}

        if operator.eq(positionDict, pointDict):
            if abs(float(theta) - float(conveyorTheta)) < float(0.3):
                id = stateId

    return id
