# coding:utf-8

import codecs
import csv
import datetime
import math
import os
import time
from xlrd import xldate_as_tuple
import pandas as pd


# 非京东项目订单转换
def otherOrderSku(targetFile, sheet, nrows, ncols, intervalTime, interval):
    # 计算下发时间间隔
    interTimeDict = wIntervalTime(sheet, nrows, ncols, interval)

    orderDict = {}
    orderNoDict = {}
    orderTime = {}
    skuCodeList = []
    for i in range(1, nrows):
        skuList = []
        orderNoID = -1
        skuCodeID = -1
        qtyID = -1
        oTimeID = -1
        for j in range(0, ncols):
            colName = sheet.cell(0, j).value
            if colName == '订单号':
                orderNoID = j
            if colName == '商品编码':
                skuCodeID = j
            if colName == '实际拣货量':
                qtyID = j
            if colName == '允许可下发时间':
                oTimeID = j
        orderNo = sheet.cell(i, orderNoID).value
        skuCode = sheet.cell(i, skuCodeID).value
        qty = sheet.cell(i, qtyID).value
        oTime = sheet.cell(i, oTimeID)
        if oTime.ctype == 3:
            date = xldate_as_tuple(oTime.value, 0)
            interTime = datetime.datetime(*date)

        skuDict = {'skuCode': skuCode, 'qty': qty}
        skuCodeList.append(skuCode)

        if orderNo not in orderDict.keys():
            skuList.append(skuDict)
            orderDict[orderNo] = skuList
            orderNoDict[orderNo] = i
            orderTime[orderNo] = interTime
        else:
            skuList = orderDict[orderNo]
            skuList.append(skuDict)
            orderDict[orderNo] = skuList

    # 写订单文件
    tarFile = os.path.join(targetFile, "./order.csv")
    orderFile = codecs.open(tarFile, 'w', 'gbk')
    writer = csv.writer(orderFile)
    skuCodeList = set(skuCodeList)
    skuCodeList = list(skuCodeList)
    for k, v in orderDict.items():
        orderId = orderNoDict[k]
        cOrderId = k
        skuNums = len(v)
        skuRowList = []

        # 前4列赋值
        workOrderId = -1
        priority = 0
        deadlineTime = 0
        if intervalTime == 0:
            dispatchId = 0
        else:
            strInterTime = orderTime[k]
            dispatchId = interTimeDict[str(strInterTime)]

        for m in v:
            # 通过skuCodeList的下标序号表示SKU名称
            skuCodeId = m['skuCode']
            skuQty = m['qty']
            skuName = skuCodeList.index(skuCodeId) + 1
            # locationRowsList = [workOrderId, dispatchId, priority, deadlineTime, orderId, str(cOrderId)[:-2] + '\t',
            #                     skuNums]
            locationRowsList = [workOrderId, dispatchId, priority, deadlineTime, orderId, str(cOrderId) + '\t',
                                skuNums]
            skuRowList.append(skuName)
            skuRowList.append(str(skuQty))
        locationRows = locationRowsList + skuRowList
        writer.writerow(locationRows)

    # 写SKU映射表
    skuTarFile = os.path.join(targetFile, "./skuCode.csv")
    skuFile = codecs.open(skuTarFile, 'w', 'gbk')
    writerSku = csv.writer(skuFile)
    for q in skuCodeList:
        skuCsvList = []
        skuCsvList.append(skuCodeList.index(q) + 1)
        # skuCsvList.append(str(q)[:-2] + '\t')
        skuCsvList.append(str(q) + '\t')
        writerSku.writerow(skuCsvList)

    orderFile.close()


def deadTime(sheet, nrows, ncols, deadline):
    # 取出时间数据
    dateTimeList = []
    deadTimeList = []
    for i in range(1, nrows):
        deadTimeID = -1
        for j in range(0, ncols):
            colName = sheet.cell(0, j).value
            if colName == '生产结束时间':
                deadTimeID = j

        deadTime = sheet.cell(i, deadTimeID)
        if deadTime.ctype == 3:
            date = xldate_as_tuple(deadTime.value, 0)
            dTime = datetime.datetime(*date)
            date = str(dTime)[:10]
            dateTime = datetime.datetime.strptime(date, '%Y-%m-%d')
            dateTimeList.append(dateTime)
            deadTimeList.append(dTime)

    # 时间字段转时间戳
    # 日期时间戳
    dtimestampList = []
    for j in dateTimeList:
        middTime = time.mktime(j.timetuple())
        dtimestampList.append(int(str(middTime)[:-2]))

    # 日期+时分时间戳
    timestampList = []
    for i in deadTimeList:
        midTime = time.mktime(i.timetuple())
        timestampList.append(int(str(midTime)[:-2]))

    # 找到最早时间戳
    # 日期时间戳
    dtimestampList = set(dtimestampList)
    dtimestampList = list(dtimestampList)
    minDTime = dtimestampList[0]
    for i in dtimestampList:
        if i - minDTime < 0:
            minDTime = i

    # 日期+时分时间戳
    timestampList = set(timestampList)
    timestampList = list(timestampList)
    minTime = timestampList[0]
    for j in timestampList:
        if j - minTime < 0:
            minTime = j

    # 计算截单时间
    deadTimeDict = {}
    for p in timestampList:
        if p == minTime:
            deadDateTime = minTime - minDTime - deadline * 60
            if deadDateTime <= 0:
                minDTime = minDTime - 86400
                deadDateTime = minTime - minDTime - deadline * 60
            timeArray = time.localtime(minTime)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            deadTimeDict[otherStyleTime] = deadDateTime
        else:
            deadDateTime = p - minDTime - deadline * 60
            timeArray = time.localtime(p)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            deadTimeDict[otherStyleTime] = deadDateTime

    return deadTimeDict


def writeJDOrderSku(targetFile, sheet, nrows, ncols, intervalTime, interval, deadline, ifRecombine):
    # 计算下发时间间隔
    interTimeDict = wIntervalTime(sheet, nrows, ncols, interval)
    # 计算截单时间
    deadTimeDict = deadTime(sheet, nrows, ncols, deadline)

    orderDict = {}
    orderNoDict = {}
    orderTime = {}
    orderIfMerge = {}
    orderDeadTime = {}
    skuCodeList = []
    for i in range(1, nrows):
        """
        遍历原始订单文件每一行
        """
        skuList = []
        orderNoID = -1
        ifMergeS = -1
        skuCodeID = -1
        qtyID = -1
        oTimeID = -1
        deadTimeID = -1
        for j in range(0, ncols):
            """
            遍历每一行的每一列
            """
            colName = sheet.cell(0, j).value
            """
            sheet.cell(x,y)表示第x行第y列的单元格
            因为上一层遍历是每一行，所以这里每次遍历只有一行，x = 0 
            """
            if colName == '订单号':
                orderNoID = j
            if colName == '商品编码':
                skuCodeID = j
            if colName == '实际拣货量':
                qtyID = j
            if colName == '允许可下发时间':
                oTimeID = j
            if colName == '生产结束时间':
                deadTimeID = j
            if colName == '是否合流':
                ifMerge = j
        orderNo = sheet.cell(i, orderNoID).value
        skuCode = sheet.cell(i, skuCodeID).value
        qty = sheet.cell(i, qtyID).value
        oTime = sheet.cell(i, oTimeID)
        ifMergeS = sheet.cell(i, ifMerge).value

        if oTime.ctype == 3:
            """
            python读取excel中单元格的内容返回的有5种类型。
            ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error。
            即date的ctype=3，这时需要使用xlrd的xldate_as_tuple来处理为date格式
            先判断表格的ctype=3时xldate才能开始操作
            """
            date = xldate_as_tuple(oTime.value, 0)
            interTime = datetime.datetime(*date)

        dTime = sheet.cell(i, deadTimeID)

        if dTime.ctype == 3:
            ddate = xldate_as_tuple(dTime.value, 0)
            deTime = datetime.datetime(*ddate)

        skuDict = {'skuCode': skuCode, 'qty': qty}
        skuCodeList.append(skuCode)

        if orderNo not in orderDict.keys():
            """
            如果orderNo不在orderDict里，说明是新添加的order
            那么sku列表添加这一行的 sku字典，包括sku名称及件数
            """
            skuList.append(skuDict)
            orderDict[orderNo] = skuList
            orderNoDict[orderNo] = i
            orderIfMerge[orderNo] = ifMergeS
            orderTime[orderNo] = interTime
            orderDeadTime[orderNo] = deTime
        else:
            """
            如果订单已经存在于字典中，则只需要将新sku及其件数添加即可
            """
            skuList = orderDict[orderNo]
            skuList.append(skuDict)
            orderDict[orderNo] = skuList

    # 写订单文件
    tarFile = os.path.join(targetFile, "./order.csv")
    orderFile = codecs.open(tarFile, 'w', 'gbk')
    writer = csv.writer(orderFile)
    skuCodeList = set(skuCodeList)
    skuCodeList = list(skuCodeList)
    print(orderDict)
    for k, v in orderDict.items():
        orderId = orderNoDict[k]
        cOrderId = k
        skuNums = len(v)
        OrderQtt = sum(d['qty'] for d in v)
        IfMergeKey = orderIfMerge[k]
        skuRowList = []

        # 京东前4列赋值
        # 工单号三种情况
        if ifRecombine == 0:
            """
            不组单，工单号全为-1
            """
            workOrderId = -1
        elif ifRecombine == 1:
            """
            根据订单的单多件属性，及是否合流标识工单号
            单件 ：1 ； 多件 ：2 ； 合流 ： -1
            """
            if IfMergeKey == '合流':
                workOrderId = -1
            elif OrderQtt == 1:
                workOrderId = 1
            else:
                workOrderId = 2
        else:
            workOrderId = 1

        priority = 0

        # 下发间隔
        if intervalTime == 0:
            dispatchId = 0
        else:
            strInterTime = orderTime[k]
            dispatchId = interTimeDict[str(strInterTime)] - 1

        # 截单时间
        dlTime = orderDeadTime[k]
        deadlineTime = deadTimeDict[str(dlTime)]

        for m in v:
            # 通过skuCodeList的下标序号表示SKU名称
            skuCodeId = m['skuCode']
            skuQty = m['qty']
            skuName = skuCodeList.index(skuCodeId) + 1
            # locationRowsList = [workOrderId, dispatchId, priority, deadlineTime, orderId, str(cOrderId)[:-2] + '\t',
            #                     skuNums]
            locationRowsList = [workOrderId, dispatchId, priority, deadlineTime, orderId, str(cOrderId) + '\t',
                                skuNums]
            skuRowList.append(skuName)
            skuRowList.append(str(skuQty))
        locationRows = locationRowsList + skuRowList
        writer.writerow(locationRows)

    # 写SKU映射表
    skuTarFile = os.path.join(targetFile, "./skuCode.csv")
    skuFile = codecs.open(skuTarFile, 'w', 'gbk')
    writerSku = csv.writer(skuFile)
    for q in skuCodeList:
        skuCsvList = []
        skuCsvList.append(skuCodeList.index(q) + 1)
        # skuCsvList.append(str(q)[:-2] + '\t')
        skuCsvList.append(str(q) + '\t')
        writerSku.writerow(skuCsvList)

    orderFile.close()


# 京东项目订单转换
def wIntervalTime(sheet, nrows, ncols, interval):
    # 取出时间数据
    intervalTimeList = []
    for i in range(1, nrows):
        oTimeID = -1
        for j in range(0, ncols):
            colName = sheet.cell(0, j).value
            if colName == '允许可下发时间':
                oTimeID = j

        oTime = sheet.cell(i, oTimeID)
        if oTime.ctype == 3:
            date = xldate_as_tuple(oTime.value, 0)
            value = datetime.datetime(*date)
            intervalTimeList.append(value)

    # 时间字段转时间戳
    timestampList = []
    for i in intervalTimeList:
        midTime = time.mktime(i.timetuple())
        timestampList.append(int(str(midTime)[:-2]))

    # 找到最早时间戳
    timestampList = set(timestampList)
    timestampList = list(timestampList)
    minTime = timestampList[0]
    for j in timestampList:
        if j - minTime < 0:
            minTime = j

    # 计算间隔时段
    interTimeDict = {}
    for p in timestampList:
        if p == minTime:
            timeArray = time.localtime(minTime)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            interTimeDict[otherStyleTime] = 1
        else:
            curTime = (p - minTime) / 60
            interTime = math.ceil(float(curTime) / interval)

            timeArray = time.localtime(p)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            interTimeDict[otherStyleTime] = interTime

    return interTimeDict
