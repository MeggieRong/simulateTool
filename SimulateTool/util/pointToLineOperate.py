# coding:utf-8

import codecs
import csv
import json
import os
import xlrd
import yaml


def locatPointSort(sourceFile, isRC):
    pointdict = {}

    allPList = searchAllPoint(sourceFile)
    for point in allPList:
        x = floatRound(point[0])
        y = floatRound(point[1])
        if isRC == 'row':
            # 坐标点分成行
            if y not in pointdict.keys():
                pointlist = []
                pointlist.append(x)
                pointdict[y] = pointlist
            else:
                pointlist = pointdict[y]
                pointlist.append(x)
        if isRC == 'col':
            # 坐标点分成列
            if x not in pointdict.keys():
                pointlist = []
                pointlist.append(y)
                pointdict[x] = pointlist
            else:
                pointlist = pointdict[x]
                pointlist.append(y)

    # 行坐标排序
    # 先排key值
    locationlist = list(pointdict.keys())
    locationlist = sorted(list(set(locationlist)))
    keylist = locationsort(locationlist)
    hangsort = {}

    # 再排values
    for k in keylist:
        valuelist = pointdict[float(k)]
        valuesortlist = locationsort(valuelist)
        valuesortlist = sorted(list(set(valuesortlist)))
        hangsort[k] = valuesortlist

    return hangsort

# 四舍五入，精确到两位


def floatRound(strNum):
    sourceNum = str(strNum)
    first = sourceNum.split('.')[0]
    last = sourceNum.split('.')[1]
    if len(last) >= 3:
        flast = last[1]
        llast = last[2]
        if int(llast) >= 5:
            flast = int(flast) + 1
            sssttt = first + '.' + last[0] + str(flast)
        else:
            sssttt = first + '.' + last[0:2]

        fRNum = float(sssttt)
    else:
        fRNum = float(sourceNum)

    return fRNum

# 坐标排序


def locationsort(locationlist):
    hanglist = []
    for i in range(0, len(locationlist)):
        key = float(locationlist[i])
        hanglist.append(key)

    return sorted(hanglist)


def strDevert(sdr):
    strconvert = ''
    sdrlist = list(sdr)
    if sdrlist[-1] == '0':
        sdrlist = sdrlist[:-2]
        strDevert(sdrlist)

    if sdrlist[-1] == '.':
        sdrlist = sdrlist[:-1]

    for k in sdrlist:
        strconvert += k

    return strconvert


def createChanelList(sourceFile, channelType):
    pointdict = {}
    hangsort = {}

    # 遍历所有坐标点
    allPList = searchAllPoint(sourceFile)
    for point in allPList:
        x = point[0]
        y = point[1]
        isChannel = point[2]
        # 找到取放货点分巷道
        if isChannel == '1':
            if channelType == 'x':
                if y not in pointdict.keys():
                    pointlist = []
                    pointlist.append(x)
                    pointdict[y] = pointlist
                else:
                    pointlist = pointdict[y]
                    pointlist.append(x)
            elif channelType == 'y':
                if x not in pointdict.keys():
                    pointlist = []
                    pointlist.append(y)
                    pointdict[x] = pointlist
                else:
                    pointlist = pointdict[x]
                    pointlist.append(y)

    # 巷道行坐标排序
    # 先排key值
    locationlist = list(pointdict.keys())
    keylist = locationsort(locationlist)

    # 再排values
    for k in keylist:
        valuelist = pointdict[float(k)]
        valuesortlist = locationsort(valuelist)
        hangsort[k] = valuesortlist

    return hangsort


def searchAllPoint(sourceFile):
    allPointList = []

    # 遍历所有坐标点，
    with open(sourceFile, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # 找出所有巷道点
            x = floatRound(float(row[0]))
            y = floatRound(float(row[1]))
            isChannel = row[2]
            allPointList.append([x, y, isChannel])

    return allPointList


def creatChannel(sourceFile, channelType, pointLength):
    channelDict = {}
    hangsort = createChanelList(sourceFile, channelType)

    # 巷道拆分
    countChanel = 1
    for k, v in hangsort.items():
        subSetChannel = []
        flag = False
        for i in range(0, len(v)-1):
            if flag:
                break
            for j in range(0, len(v)-i-1):
                if v[j+1] - v[j] <= float(pointLength):
                    subSetChannel.append(v[j])
                    if v[j+1] == v[-1]:
                        subSetChannel.append(v[j+1])
                        if channelType == 'x':
                            channelStart = [subSetChannel[0], k]
                            channelEnd = [subSetChannel[-1], k]
                        elif channelType == 'y':
                            channelStart = [k, subSetChannel[0]]
                            channelEnd = [k, subSetChannel[-1]]
                        channelDict[countChanel] = [channelStart, channelEnd]
                        subSetChannel = []
                        countChanel += 1
                        flag = True
                else:
                    subSetChannel.append(v[j])
                    if channelType == 'x':
                        channelStart = [subSetChannel[0], k]
                        channelEnd = [subSetChannel[-1], k]
                    elif channelType == 'y':
                        channelStart = [k, subSetChannel[0]]
                        channelEnd = [k, subSetChannel[-1]]
                    channelDict[countChanel] = [channelStart, channelEnd]
                    subSetChannel = []
                    countChanel += 1

    return channelDict


def strDevert(str):
    strconvert = ''
    sdrlist = list(str)
    if sdrlist[-1] == '0':
        sdrlist = sdrlist[:-2]
        strDevert(sdrlist)

    if sdrlist[-1] == '.':
        sdrlist = sdrlist[:-1]

    for k in sdrlist:
        strconvert += k

    return strconvert


def creatAdjacencyList(sourceFile, channelType, pointLength, yNoHorizontal, xNoVertical, ypNoHorizontal, xpNoVertical):
    # 所有坐标点分行、分列
    pointLength = float(pointLength)
    isRC1 = 'row'
    hangdict = locatPointSort(sourceFile, isRC1)
    isRC2 = 'col'
    liedict = locatPointSort(sourceFile, isRC2)

    # 获取巷道
    channelDict = creatChannel(sourceFile, channelType, pointLength)

    # 遍历所有坐标点，
    allPList = searchAllPoint(sourceFile)
    pointAdjcList = {}
    count = 0
    for point in allPList:
        count += 1
        x = point[0]
        y = point[1]
        isChannel = point[2]
        upPoint = []
        leftPoint = []
        downPoint = []
        rightPoint = []
        linePointList = []

        # 获取取货点巷道ID
        if isChannel == '1':
            point = [float(x), float(y)]
            channelID = searchChannelId(point, channelDict)
        else:
            channelID = -1

        # 检查坐标点是否重复
        pointKey = [x, y, channelID]
        pADList = []
        for k in pointAdjcList.keys():
            pADList.append(list(k))

        if pointKey not in pADList:
            if channelType == 'x':
                hanglist = hangdict[float(y)]
                x = float(x)
                # 坐标点左右连线
                if y in yNoHorizontal:
                    leftPoint = []
                    rightPoint = []
                elif len(hanglist) > 1:
                    if x == hanglist[0]:
                        if abs(hanglist[hanglist.index(x) + 1] - x) <= pointLength:
                            if len(ypNoHorizontal) != 0:
                                for q in ypNoHorizontal:
                                    if str(x) == q[0][0] and str(y) == q[0][1] and str(hanglist[hanglist.index(x) + 1]) == q[1][0] and str(y) == q[1][1]:
                                        rightPoint = []
                                    else:
                                        rightPoint = [
                                            hanglist[hanglist.index(x) + 1], y]
                            else:
                                rightPoint = [
                                    hanglist[hanglist.index(x) + 1], y]
                    elif x == hanglist[-1]:
                        if abs(hanglist[hanglist.index(x) - 1] - x) <= pointLength:
                            if len(ypNoHorizontal) != 0:
                                for q in ypNoHorizontal:
                                    if str(x) == q[1][0] and str(y) == q[1][1] and str(hanglist[hanglist.index(x) - 1]) == q[0][0] and str(y) == q[0][1]:
                                        leftPoint = []
                                    else:
                                        leftPoint = [
                                            hanglist[hanglist.index(x) - 1], y]
                            else:
                                leftPoint = [
                                    hanglist[hanglist.index(x) - 1], y]
                    else:
                        if abs(x - hanglist[hanglist.index(x) - 1]) <= pointLength:
                            if len(ypNoHorizontal) != 0:
                                for q in ypNoHorizontal:
                                    if str(x) == q[0][0] and str(y) == q[0][1] and str(hanglist[hanglist.index(x) + 1]) == q[1][0] and str(y) == q[1][1]:
                                        rightPoint = []
                                        leftPoint = [
                                            hanglist[hanglist.index(x) - 1], y]
                                    elif str(x) == q[1][0] and str(y) == q[1][1] and str(hanglist[hanglist.index(x) - 1]) == q[0][0] and str(y) == q[0][1]:
                                        if abs(hanglist[hanglist.index(x) + 1] - x) <= pointLength:
                                            rightPoint = [
                                                hanglist[hanglist.index(x) + 1], y]
                                        else:
                                            rightPoint = []
                                        leftPoint = []
                                    else:
                                        if abs(hanglist[hanglist.index(x) + 1] - x) <= pointLength:
                                            rightPoint = [
                                                hanglist[hanglist.index(x) + 1], y]
                                        else:
                                            rightPoint = []
                                        leftPoint = [
                                            hanglist[hanglist.index(x) - 1], y]
                            else:
                                if abs(hanglist[hanglist.index(x) + 1] - x) <= pointLength:
                                    rightPoint = [
                                        hanglist[hanglist.index(x) + 1], y]
                                else:
                                    rightPoint = []
                                leftPoint = [
                                    hanglist[hanglist.index(x) - 1], y]
                        elif abs(x - hanglist[hanglist.index(x) + 1]) <= pointLength:
                            if len(ypNoHorizontal) != 0:
                                for q in ypNoHorizontal:
                                    if str(x) == q[0][0] and str(y) == q[0][1] and str(hanglist[hanglist.index(x) + 1]) == q[1][0] and str(y) == q[1][1]:
                                        rightPoint = []
                                        if abs(hanglist[hanglist.index(x) - 1] - x) <= pointLength:
                                            leftPoint = [
                                                hanglist[hanglist.index(x) - 1], y]
                                        else:
                                            leftPoint = []
                                    elif str(x) == q[1][0] and str(y) == q[1][1] and str(hanglist[hanglist.index(x) - 1]) == q[0][0] and str(y) == q[0][1]:
                                        rightPoint = [
                                            hanglist[hanglist.index(x) + 1], y]
                                        if abs(hanglist[hanglist.index(x) - 1] - x) <= pointLength:
                                            leftPoint = [
                                                hanglist[hanglist.index(x) - 1], y]
                                        else:
                                            leftPoint = []
                                    else:
                                        rightPoint = [
                                            hanglist[hanglist.index(x) + 1], y]
                                        if abs(hanglist[hanglist.index(x) - 1] - x) <= pointLength:
                                            leftPoint = [
                                                hanglist[hanglist.index(x) - 1], y]
                                        else:
                                            leftPoint = []
                            else:
                                rightPoint = [
                                    hanglist[hanglist.index(x) + 1], y]
                                if abs(hanglist[hanglist.index(x) - 1] - x) <= pointLength:
                                    leftPoint = [
                                        hanglist[hanglist.index(x) - 1], y]
                                else:
                                    leftPoint = []

                # 非取货点上下连线
                lielist = liedict[float(x)]
                if isChannel == '0':
                    y = float(y)
                    if x in xNoVertical:
                        upPoint = []
                        downPoint = []
                    elif len(lielist) > 1:
                        if y == lielist[0]:
                            if abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                                if len(xpNoVertical) != 0:
                                    for p in xpNoVertical:
                                        if str(x) == p[0][0] and str(y) == p[0][1] and str(x) == p[1][0] and str(lielist[lielist.index(y) + 1]) == p[1][1]:
                                            upPoint = []
                                        else:
                                            upPoint = [
                                                x, lielist[lielist.index(y) + 1]]
                                else:
                                    upPoint = [
                                        x, lielist[lielist.index(y) + 1]]
                        elif y == lielist[-1]:
                            if abs(lielist[lielist.index(y) - 1] - y) <= pointLength:
                                if len(xpNoVertical) != 0:
                                    for p in xpNoVertical:
                                        if str(x) == p[1][0] and str(y) == p[1][1] and str(x) == p[0][0] and str(lielist[lielist.index(y) - 1]) == p[0][1]:
                                            downPoint = []
                                        else:
                                            downPoint = [
                                                x, lielist[lielist.index(y) - 1]]
                                else:
                                    downPoint = [
                                        x, lielist[lielist.index(y) - 1]]
                        else:
                            if abs(y - lielist[lielist.index(y) - 1]) <= pointLength:
                                if len(xpNoVertical) != 0:
                                    for p in xpNoVertical:
                                        if str(x) == p[0][0] and str(y) == p[0][1] and str(x) == p[1][0] and str(lielist[lielist.index(y) + 1]) == p[1][1]:
                                            upPoint = []
                                            downPoint = [
                                                x, lielist[lielist.index(y) - 1]]
                                        elif str(x) == p[1][0] and str(y) == p[1][1] and str(x) == p[0][0] and str(lielist[lielist.index(y) - 1]) == p[0][1]:
                                            if abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                                                upPoint = [
                                                    x, lielist[lielist.index(y) + 1]]
                                            else:
                                                upPoint = []
                                            downPoint = []
                                        else:
                                            if abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                                                upPoint = [
                                                    x, lielist[lielist.index(y) + 1]]
                                            else:
                                                upPoint = []
                                            downPoint = [
                                                x, lielist[lielist.index(y) - 1]]
                                else:
                                    if abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                                        upPoint = [
                                            x, lielist[lielist.index(y) + 1]]
                                    else:
                                        upPoint = []
                                    downPoint = [
                                        x, lielist[lielist.index(y) - 1]]
                            elif abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                                if len(xpNoVertical) != 0:
                                    for p in xpNoVertical:
                                        if str(x) == p[0][0] and str(y) == p[0][1] and str(x) == p[1][0] and str(lielist[lielist.index(y) + 1]) == p[1][1]:
                                            upPoint = []
                                            if abs(lielist[lielist.index(y) - 1] - y) <= pointLength:
                                                downPoint = [
                                                    x, lielist[lielist.index(y) - 1]]
                                            else:
                                                downPoint = []
                                        elif str(x) == p[1][0] and str(y) == p[1][1] and str(x) == p[0][0] and str(lielist[lielist.index(y) - 1]) == p[0][1]:
                                            upPoint = [
                                                x, lielist[lielist.index(y) + 1]]
                                            downPoint = []
                                        else:
                                            upPoint = [
                                                x, lielist[lielist.index(y) + 1]]
                                            if abs(lielist[lielist.index(y) - 1] - y) <= pointLength:
                                                downPoint = [
                                                    x, lielist[lielist.index(y) - 1]]
                                            else:
                                                downPoint = []
                                else:
                                    upPoint = [
                                        x, lielist[lielist.index(y) + 1]]
                                    if abs(lielist[lielist.index(y) - 1] - y) <= pointLength:
                                        downPoint = [
                                            x, lielist[lielist.index(y) - 1]]
                                    else:
                                        downPoint = []

                # 连线点写入行坐标
                if len(upPoint) != 0:
                    linePointList.append(upPoint)
                if len(leftPoint) != 0:
                    linePointList.append(leftPoint)
                if len(downPoint) != 0:
                    linePointList.append(downPoint)
                if len(rightPoint) != 0:
                    linePointList.append(rightPoint)

            elif channelType == 'y':
                lielist = liedict[float(x)]
                y = float(y)
                # 坐标点上下连线
                if x in xNoVertical:
                    upPoint = []
                    downPoint = []
                elif len(lielist) > 1:
                    if y == lielist[0]:
                        if abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                            if len(xpNoVertical) != 0:
                                for p in xpNoVertical:
                                    if str(x) == p[0][0] and str(y) == p[0][1] and str(x) == p[1][0] and str(lielist[lielist.index(y) + 1]) == p[1][1]:
                                        upPoint = []
                                    else:
                                        upPoint = [
                                            x, lielist[lielist.index(y) + 1]]
                            else:
                                upPoint = [x, lielist[lielist.index(y) + 1]]
                    elif y == lielist[-1]:
                        if abs(lielist[lielist.index(y) - 1] - y) <= pointLength:
                            if len(xpNoVertical) != 0:
                                for p in xpNoVertical:
                                    if str(x) == p[1][0] and str(y) == p[1][1] and str(x) == p[0][0] and str(lielist[lielist.index(y) - 1]) == p[0][1]:
                                        downPoint = []
                                    else:
                                        downPoint = [
                                            x, lielist[lielist.index(y) - 1]]
                            else:
                                downPoint = [x, lielist[lielist.index(y) - 1]]
                    else:
                        if abs(y - lielist[lielist.index(y) - 1]) <= pointLength:
                            if len(xpNoVertical) != 0:
                                for p in xpNoVertical:
                                    if str(x) == p[0][0] and str(y) == p[0][1] and str(x) == p[1][0] and str(lielist[lielist.index(y) + 1]) == p[1][1]:
                                        upPoint = []
                                        downPoint = [
                                            x, lielist[lielist.index(y) - 1]]
                                    elif str(x) == p[1][0] and str(y) == p[1][1] and str(x) == p[0][0] and str(lielist[lielist.index(y) - 1]) == p[0][1]:
                                        if abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                                            upPoint = [
                                                x, lielist[lielist.index(y) + 1]]
                                        else:
                                            upPoint = []
                                        downPoint = []
                                    else:
                                        if abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                                            upPoint = [
                                                x, lielist[lielist.index(y) + 1]]
                                        else:
                                            upPoint = []
                                        downPoint = [
                                            x, lielist[lielist.index(y) - 1]]
                            else:
                                if abs(lielist[lielist.index(y) + 1] - y) <= pointLength:
                                    upPoint = [
                                        x, lielist[lielist.index(y) + 1]]
                                else:
                                    upPoint = []
                                downPoint = [x, lielist[lielist.index(y) - 1]]

                # 非取货点左右连线
                hanglist = hangdict[float(y)]
                if isChannel == '0':
                    x = float(x)
                    if y in yNoHorizontal:
                        rightPoint = []
                        leftPoint = []
                    elif len(hanglist) > 1:
                        if x == hanglist[0]:
                            if abs(hanglist[hanglist.index(x) + 1] - x) <= pointLength:
                                if len(ypNoHorizontal) != 0:
                                    for p in ypNoHorizontal:
                                        if str(x) == p[0][0] and str(y) == p[0][1] and str(hanglist[hanglist.index(x) + 1]) == p[1][0] and str(y) == p[1][1]:
                                            rightPoint = []
                                        else:
                                            rightPoint = [
                                                hanglist[hanglist.index(x) + 1], y]
                                else:
                                    rightPoint = [
                                        hanglist[hanglist.index(x) + 1], y]
                        elif x == hanglist[-1]:
                            if abs(hanglist[hanglist.index(x) - 1] - x) <= pointLength:
                                if len(ypNoHorizontal) != 0:
                                    for p in ypNoHorizontal:
                                        if str(x) == p[1][0] and str(y) == p[1][1] and str(hanglist[hanglist.index(x) - 1]) == p[0][0] and str(y) == p[0][1]:
                                            leftPoint = []
                                        else:
                                            leftPoint = [
                                                hanglist[hanglist.index(x) - 1], y]
                                else:
                                    leftPoint = [
                                        hanglist[hanglist.index(x) - 1], y]
                        else:
                            if abs(x - hanglist[hanglist.index(x) - 1]) <= pointLength:
                                if len(ypNoHorizontal) != 0:
                                    for p in ypNoHorizontal:
                                        if str(x) == p[0][0] and str(y) == p[0][1] and str(hanglist[hanglist.index(x) + 1]) == p[1][0] and str(y) == p[1][1]:
                                            rightPoint = []
                                            leftPoint = [
                                                hanglist[hanglist.index(x) - 1], y]
                                        elif str(x) == p[1][0] and str(y) == p[1][1] and str(hanglist[hanglist.index(x) - 1]) == p[0][0] and str(y) == p[0][1]:
                                            if abs(hanglist[hanglist.index(x) + 1] - x) <= pointLength:
                                                rightPoint = [
                                                    hanglist[hanglist.index(x) + 1], y]
                                            else:
                                                rightPoint = []
                                            leftPoint = []
                                        else:
                                            if abs(hanglist[hanglist.index(x) + 1] - x) <= pointLength:
                                                rightPoint = [
                                                    hanglist[hanglist.index(x) + 1], y]
                                            else:
                                                rightPoint = []
                                            leftPoint = [
                                                hanglist[hanglist.index(x) - 1], y]
                                else:
                                    if abs(hanglist[hanglist.index(x) + 1] - x) <= pointLength:
                                        rightPoint = [
                                            hanglist[hanglist.index(x) + 1], y]
                                    else:
                                        rightPoint = []
                                    leftPoint = [
                                        hanglist[hanglist.index(x) - 1], y]

                # 添加坐标点到行坐标
                if len(upPoint) != 0:
                    linePointList.append(upPoint)
                if len(leftPoint) != 0:
                    linePointList.append(leftPoint)
                if len(downPoint) != 0:
                    linePointList.append(downPoint)
                if len(rightPoint) != 0:
                    linePointList.append(rightPoint)

            pointAdjcList[x, y, channelID] = linePointList
        else:
            print('坐标点：{} 重复'.format([x, y]))
            continue

    coverPoint = len(pointAdjcList)
    pInfo = []
    pInfo.append(count)
    pInfo.append(coverPoint)
    pInfo.append((count-coverPoint))
    # print('方案源文件共有坐标点：{} 个，转换成功：{} 个，重复坐标点：{} 个'.format(count, coverPoint, (count-coverPoint)))
    return pointAdjcList, pInfo


def searchChannelId(point, channelDict):
    channelId = 0
    for k, v in channelDict.items():
        if v[0][0] <= float(point[0]) <= v[1][0] and v[0][1] <= point[1] <= v[1][1]:
            channelId = k

    return channelId


def writerFiles(channelDict, adjacencyList, targetFile):
    adjacencyPath = targetFile + r'\adjacency_list.in'
    adjacencyCsvPath = targetFile + r'\adjacent_list.csv'
    channelEEPath = targetFile + '\channelEE.txt'

    # 生成channelEE文件
    with open(channelEEPath, "w+") as f:
        channelFlag = 1
        for k, v in channelDict.items():
            channelStartx = v[0][0]
            channelStarty = v[0][1]
            channelEndx = v[1][0]
            channelEndy = v[1][1]
            channelLine = str(k) + ',' + str(channelFlag) + ':' + str(channelStartx) + \
                ',' + str(channelStarty) + ',' + \
                str(channelEndx) + ',' + str(channelEndy)

            f.write(channelLine)
            f.write('\n')

            if channelFlag == 1:
                channelFlag = -1
            else:
                channelFlag = 1

    f.close()

    # 生成adjacency_list文件
    with open(adjacencyPath, "w+") as fi:
        for m, n in adjacencyList.items():
            pointx = m[0]
            pointy = m[1]
            channelId = m[2]
            adjacencyLine = str(pointx) + ',' + str(pointy) + \
                ',' + str(channelId) + ':'
            for adValue in n:
                if adValue != n[-1]:
                    adjacencyLine = adjacencyLine + \
                        str(adValue[0]) + ',' + str(adValue[1]) + ';'
                else:
                    adjacencyLine = adjacencyLine + \
                        str(adValue[0]) + ',' + str(adValue[1])

            fi.write(adjacencyLine)
            fi.write('\n')

    fi.close()

    # 生成adjacent_csv文件
    with open(adjacencyCsvPath, "w+") as file:
        for m, n in adjacencyList.items():
            pointx = m[0]
            pointy = m[1]
            channelId = m[2]
            adjacencyCsvLine = str(pointx) + ',' + \
                str(pointy) + ',' + str(channelId) + ':'
            for adValue in n:
                if adValue != n[-1]:
                    adjacencyCsvLine = adjacencyCsvLine + \
                        str(adValue[0]) + ',' + str(adValue[1]) + ';'
                else:
                    adjacencyCsvLine = adjacencyCsvLine + \
                        str(adValue[0]) + ',' + str(adValue[1])

            file.write(adjacencyCsvLine)
            file.write('\n')

    file.close()


def chargeListFile(sourcePath):
    xyDict = []

    # 读取Excel文件,取出充电点
    readbook = xlrd.open_workbook(sourcePath)
    sheet = readbook.sheet_by_index(0)

    # 获取全地图的x和y,去重并且各自做升序
    xList = sorted(set(sheet.col_values(2)[1:]), reverse=False)
    yList = sorted(set(sheet.col_values(3)[1:]), reverse=False)

    def kubotTheta(x, y):
        if x in xList[:2]:
            theta = -3.14
        elif x in xList[-2:]:
            theta = 0
        elif y in yList[:2]:
            theta = 1.57
        else:
            theta = -1.57
        return theta

    nrows = sheet.nrows
    for i in range(1, nrows):
        color = sheet.cell(i, 1).value
        if color == '白' or color == 'White':
            x = sheet.cell(i, 2).value
            y = sheet.cell(i, 3).value
            theta = kubotTheta(x, y)
            xyDict.append({'x': x, 'y': y, 'theta': theta})

    return xyDict


def writeConfig(curpath, rows, cols):
    configDict = {
        'rows': rows,
        'cols': cols
    }

    yamlpath = os.path.join(curpath, "./config.yaml")

    # 写入到yaml文件
    with open(yamlpath, "w", encoding="utf-8") as f:
        yaml.dump(configDict, f, allow_unicode=True,
                  default_flow_style=False, sort_keys=False)


def writeCharge(curpath, xyDict):
    jsontext = {
        'rest-stations': [],
        'charge-stations': []
    }
    # 为他赋值，任何你要存的值，我这里是遍历了一下我的dataframe
    for i in xyDict:
        x = i['x']
        y = i['y']
        theta = i['theta']
        positionDict = {
            'x': x,
            'y': y,
            'theta': theta
        }

        chargeDict = {
            'position': positionDict,
            'kubotId': -1
        }

        jsontext['charge-stations'].append(chargeDict)

    # 写入rest_stations.json文件
    # 后面的参数是调整生成的json的格式，不加也行，就是丑点
    jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '))
    chargePath = os.path.join(curpath, "./rest_stations.json")
    f = open(chargePath, 'w')
    f.write(jsondata)
    f.close()


def writeLocations(locDir, locationInfo, sourcePath, curpath):
    getXYDict = []
    if locDir == 'y':
        dirList = [1, 3]
    elif locDir == 'x':
        dirList = [0, 2]

    # 货架参数
    firstHeightNum = locationInfo[0]
    folowHeight = locationInfo[1]
    folowNums = locationInfo[2]
    isShallow = locationInfo[3]

    # 获取所有货位点
    readbook = xlrd.open_workbook(sourcePath)
    sheet = readbook.sheet_by_index(0)
    nrows = sheet.nrows
    for i in range(1, nrows):
        color = sheet.cell(i, 1).value
        if color == '洋红' or color == 'Magenta':
            x = sheet.cell(i, 2).value
            y = sheet.cell(i, 3).value

            getXYDict.append({'x': x, 'y': y})

    # 写 locations.csv 文件
    tarFile = os.path.join(curpath, "./locations.csv")
    f = codecs.open(tarFile, 'w', 'gbk')
    writer = csv.writer(f)
    numFlag = 1
    for i in getXYDict:
        x = i['x']
        y = i['y']
        for k in dirList:
            for j in range(0, int(folowNums)):
                heightNum = int(firstHeightNum) + j * int(folowHeight)
                locationRows = [numFlag, x, y,
                                heightNum, k, numFlag, 1, isShallow]
                writer.writerow(locationRows)
                numFlag += 1
    f.close()


def writeQrCode(qrFilePath, curpath):
    qrCodeList = []
    f = csv.reader(open(qrFilePath, 'r'))
    for i in f:
        qrCodeList.append([i[0], i[1]])

    tarFile = os.path.join(curpath, "./qr_code.csv")
    f = codecs.open(tarFile, 'w', 'gbk')
    writer = csv.writer(f)
    for j in qrCodeList:
        writer.writerow(j)

    f.close()


def writeStatePoints(spPath, curpath):
    f = open(spPath, 'r')
    lines = f.readlines()

    # 找齐方向
    spPoint = {}
    isXDir = 0
    isYDir = 0
    idFlag = 0
    jsontext = []
    for i in lines:
        pointList = i.split(':')

        # 目标坐标点
        sxy = pointList[0].split(',')
        x = float(sxy[0])
        y = float(sxy[1])

        # 方向坐标点
        txyPoint = pointList[1].strip('\n').split(';')
        for j in txyPoint:
            txy = j.split(',')
            tx = float(txy[0])
            ty = float(txy[1])
            if x - tx == 0:
                isXDir = 1
                continue

            if y - ty == 0:
                isYDir = 1
                continue

        # 后面的参数是调整生成的json的格式，不加也行，就是丑点
        # 组参
        if isXDir == 1:
            statePosition = {}
            statePosition['state id'] = idFlag
            statePosition['state position'] = {'theta': 0.0, 'x': x, 'y': y}
            jsontext.append(statePosition)
            idFlag += 1

            statePosition = {}
            statePosition['state id'] = idFlag
            statePosition['state position'] = {'theta': -3.14, 'x': x, 'y': y}
            jsontext.append(statePosition)
            idFlag += 1

        if isYDir == 1:
            statePosition = {}
            statePosition['state id'] = idFlag
            statePosition['state position'] = {'theta': 1.57, 'x': x, 'y': y}
            jsontext.append(statePosition)
            idFlag += 1

            statePosition = {}
            statePosition['state id'] = idFlag
            statePosition['state position'] = {'theta': -1.57, 'x': x, 'y': y}
            jsontext.append(statePosition)
            idFlag += 1

    # 写入rest_stations.json文件
    jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '))
    chargePath = os.path.join(curpath, "./state_points.json")
    f = open(chargePath, 'w')
    f.write(jsondata)
    f.close()


def writeOthers(curpath):
    kubotFile = os.path.join(curpath, "./kubot.csv")
    kubotF = codecs.open(kubotFile, 'w', 'gbk')

    obstacleFile = os.path.join(curpath, "./obstacle.csv")
    obstacleF = codecs.open(obstacleFile, 'w', 'gbk')

    shelfFile = os.path.join(curpath, "./shelf.csv")
    shelfF = codecs.open(shelfFile, 'w', 'gbk')

    kubotF.close()
    obstacleF.close()
    shelfF.close()
