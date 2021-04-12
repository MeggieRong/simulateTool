#coding:utf-8

import math
import random
import xlrd
import re


def getSkuCode(skuCodeFile):
    skuCodeMap = {}

    # 获取skuCode映射
    f = open(skuCodeFile)
    lines = f.readlines()
    for i in lines:
        skuList = i.split(',')
        skuMpa = skuList[0]
        skuCode1 = skuList[1].strip()
        skuCode2 = skuCode1.strip('"')
        skuCode = re.sub(r"\s", "", skuCode2)
        try:
            skuCode = str(int(float(skuCode)))
            print('1', skuCode, type(skuCode))
        except:
            print('2', skuCode, type(skuCode))
            pass
        skuCodeMap[skuCode] = skuMpa

    return skuCodeMap


# 读取订单文件获取sku
def getSkuNums(orderPath, skuCodeFile):
    skuCodeDict = {}
    skuNums = {}

    # 获取skuCode映射
    skuCodeMapDt = getSkuCode(skuCodeFile)

    # 计算订单sku数量
    readbook = xlrd.open_workbook(orderPath)
    sheet = readbook.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    for i in range(1, nrows):
        skuCodeId = -1
        qtyId = -1
        for j in range(0, ncols):
            colName = sheet.cell(0, j).value
            if colName == '商品编码':
                skuCodeId = j
            if colName == '实际拣货量':
                qtyId = j

        try:
            skuCode = str(int(sheet.cell(i, skuCodeId).value))
        except:
            skuCode = str(sheet.cell(i, skuCodeId).value)
        qty = int(sheet.cell(i, qtyId).value)

        # 商品编码和数量存入字典
        if skuCode not in skuNums.keys():
            skuNums[skuCode] = qty
        else:
            midQty = skuNums[skuCode] + qty
            skuNums[skuCode] = midQty

    # skucode映射转换
    for k, v in skuNums.items():
        skuKye = skuCodeMapDt[k]
        skuCodeDict[skuKye] = v
    return skuCodeDict


# 统计箱型SKU数量
def countSkuBinType(skuCodeFile, stockPath):
    skuBinTypeDict = {}
    skuCodeMDict = getSkuCode(skuCodeFile)

    readbook = xlrd.open_workbook(stockPath)
    sheet = readbook.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    for i in range(1, nrows):
        skuNumList = []
        skuCodeId = -1
        qtyId = -1
        binRequireId = -1
        for j in range(0, ncols):
            colName = sheet.cell(0, j).value
            if colName == 'sku编码':
                skuCodeId = j
            if colName == '装箱件数':
                qtyId = j
            if colName == '料箱需求':
                binRequireId = j
        print(1, sheet.cell)
        print(2, skuCodeId)
        print(3, sheet.cell(i, skuCodeId))
        print(4, sheet.cell(i, skuCodeId).value)
        skuCode = str(sheet.cell(i, skuCodeId).value)[:-2]
        print(5, skuCode)

        skuCode = skuCodeMDict[skuCode]
        qty = int(sheet.cell(i, qtyId).value)
        binRequire = int(sheet.cell(i, binRequireId).value)

        print(6, binRequire)
        print(7, skuBinTypeDict.keys())
        if binRequire not in skuBinTypeDict.keys():
            print(8, skuCode)
            skuNumList.append([skuCode, qty])
            print(9, skuNumList)
            skuBinTypeDict[binRequire] = skuNumList
            print(10, skuBinTypeDict)
        else:
            skuNumList = skuBinTypeDict[binRequire]
            skuNumList.append([skuCode, qty])
            skuBinTypeDict[binRequire] = skuNumList

    binTypeList = list(skuBinTypeDict.keys())
    binTypeList.sort()
    skuBType = {}
    for j in binTypeList:
        skuBType[j] = skuBinTypeDict[j]

    return skuBType


def assembleSkuDict(skuNums, locationList, floatWide, skuBinType):
    stockList = []

    for k, v in skuBinType.items():
        if k == 1:
            # 计算数量
            for i in v:
                skuCode = i[0]
                skuQty = int(i[1])  # 料箱sku规格（sku最大数量）
                skuOrderQty = skuNums[skuCode]  # 订单sku数量

                if floatWide == 0:
                    binSkuNums = math.ceil(skuOrderQty / skuQty)
                    restNums = skuOrderQty
                    for j in range(0, binSkuNums):
                        binId = random.randint(0, len(locationList))
                        binCode = locationList[binId]
                        del locationList[binId]

                        if restNums - skuQty > 0:
                            qty = skuQty
                            restNums = restNums - skuQty
                            stockList.append([binCode, skuCode, qty])
                        else:
                            qty = skuQty
                            stockList.append([binCode, skuCode, qty])
                else:
                    restNums = skuOrderQty
                    qty = random.randint(
                        math.ceil(skuQty - (skuQty * floatWide / 100)),
                        math.ceil(skuQty + (skuQty * floatWide / 100)))

                    while restNums - qty > 0:
                        binId = random.randint(0, len(locationList))
                        binCode = locationList[binId]
                        del locationList[binId]

                        restNums = restNums - qty
                        stockList.append([binCode, skuCode, qty])
                        qty = random.randint(
                            math.ceil(skuQty - (skuQty * floatWide / 100)),
                            math.ceil(skuQty + (skuQty * floatWide / 100)))
                    else:
                        binId = random.randint(0, len(locationList))
                        binCode = locationList[binId]
                        del locationList[binId]

                        qty = skuQty
                        stockList.append([binCode, skuCode, qty])
        else:
            while len(v) != 0:
                if len(v) >= k:
                    newSkuList = random.sample(v, k)
                else:
                    newSkuNewList = []
                    for m in range(0, k - len(v)):
                        newSkuCode = '9999' + str(m)
                        newSkuQty = 5 * k
                        newSkuNewList.append([newSkuCode, newSkuQty])
                        skuNums[newSkuCode] = 10000

                    newSkuList = v + newSkuNewList

                binId = random.randint(0, len(locationList))
                binCode = locationList[binId]
                del locationList[binId]

                for i in newSkuList:
                    skuCode = i[0]
                    binQty = int(i[1])  # 料箱sku规格（sku最大数量）
                    skuOrderQty = skuNums[skuCode]  # 订单sku数量

                    if floatWide == 0:
                        skuQtyNums = math.ceil(binQty / k)
                        if skuOrderQty - skuQtyNums > 0:
                            stockList.append([binCode, skuCode, skuQtyNums])
                            skuNums[skuCode] = skuOrderQty - skuQtyNums
                        else:
                            stockList.append([binCode, skuCode, skuQtyNums])
                            v.remove(i)
                    else:
                        skuQtyNums = random.randint(
                            math.ceil(binQty - (binQty * floatWide / 100)),
                            math.ceil(binQty + (binQty * floatWide / 100)))
                        if skuOrderQty - skuQtyNums > 0:
                            stockList.append([binCode, skuCode, skuQtyNums])
                            skuNums[skuCode] = skuOrderQty - skuQtyNums
                        else:
                            stockList.append([binCode, skuCode, skuQtyNums])
                            v.remove(i)

    return stockList


def writeFileNums(skuNums, locationList, floatWide, skuCodeFile, stockPath):
    print('指定库存模式')
    # 统计库存模型中的混箱数量
    skuBinType = countSkuBinType(skuCodeFile, stockPath)

    # 遍历库存模型的数据，重新组装库存数据
    stockList = assembleSkuDict(skuNums, locationList, floatWide, skuBinType)

    return stockList


def writeFixedNums(skuNums, locationList, fixedNums):
    print('不混固定模式')
    stockList = []

    for k, v in skuNums.items():
        fixedNums = int(fixedNums)

        if v > fixedNums:
            binSkuNums = math.ceil(v / fixedNums)
            restNums = v
            for i in range(0, binSkuNums):
                binId = random.randint(0, len(locationList))
                binCode = locationList[binId]
                del locationList[binId]

                if restNums - fixedNums > 0:
                    qty = fixedNums
                    restNums = restNums - fixedNums
                    stockList.append([binCode, k, qty])
                else:
                    qty = fixedNums
                    stockList.append([binCode, k, qty])
        else:
            binId = random.randint(0, len(locationList) - 1)
            binCode = locationList[binId]
            del locationList[binId]

            stockList.append([binCode, k, fixedNums])

    return stockList


def writeMaxNums(skuNums, locationList, floatWide, maxNums):
    print('不混随机模式')
    stockList = []

    for k, v in skuNums.items():
        maxNums = int(maxNums)
        floatWide = int(floatWide)
        minNums = maxNums - (maxNums * floatWide / 100)

        if v > maxNums:
            binSkuNums = math.ceil(v / minNums)
            restNums = v
            for i in range(0, binSkuNums):
                binId = random.randint(0, len(locationList))
                binCode = locationList[binId]
                del locationList[binId]

                skuRanNums = random.randint(minNums, maxNums)
                if restNums - skuRanNums > 0:
                    qty = skuRanNums
                    restNums = restNums - skuRanNums
                    stockList.append([binCode, k, qty])
                else:
                    qty = restNums
                    stockList.append([binCode, k, qty])
        else:
            binId = random.randint(0, len(locationList))
            binCode = locationList[binId]
            del locationList[binId]

            stockList.append([binCode, k, v])

    return stockList


def writeMixNums(skuNums, locationList, floatWide, mixLevel, maixNums):
    print('混箱模式')
    skuNumsLen = len(skuNums)
    mixtureList = [int(i) for i in mixLevel.split(',')]
    mixtureNums = len(mixtureList)

    # 开始混箱计算
    mixFlag = math.ceil(skuNumsLen / mixtureNums)
    count = 0
    levelFlag = 0
    skuLevelDict = {}
    skuList = []
    isFlag = 0
    for k, v in skuNums.items():
        count += 1
        if mixFlag * isFlag < count <= mixFlag * (isFlag + 1):
            skuList.append([k, int(maixNums)])
            skuLevelDict[mixtureList[levelFlag]] = skuList
        else:
            isFlag += 1
            levelFlag += 1
            skuList = []

    stockList = assembleSkuDict(skuNums, locationList, floatWide, skuLevelDict)

    return stockList