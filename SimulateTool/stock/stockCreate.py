#coding:utf-8

import codecs
import csv
import os

from util.stockOperate import getSkuNums, writeFileNums, writeFixedNums, writeMaxNums, writeMixNums
from util.selfPrepareInv import createInv


def stockCreate(orderPath, skuCodeFile, locationsPath, stockPath, tarPath,
                floatWide, fixedNums, maxNums, mixLevel, maixNums):
    floatWide = int(floatWide)
    stockSkuList = []
    # 读订单文件获取SKU数量
    skuNums = getSkuNums(orderPath, skuCodeFile)

    # 读货位文件获取可用货位
    locationList = []
    locationNums = len(open(locationsPath).readlines())
    for i in range(1, locationNums + 1):
        locationList.append(i)

    # 生成库存数据集合
    if stockPath != '' and fixedNums == '' and maxNums == '':
        #直接调用函数并且生成csv
        createInv(orderPath, locationsPath, stockPath, tarPath, skuCodeFile)
        # # 指定库存模式
        # stockSkuList = writeFileNums(skuNums, locationList, floatWide, skuCodeFile, stockPath)
    elif stockPath == '' and fixedNums != '' and maxNums == '':
        # 不混固定模式
        stockSkuList = writeFixedNums(skuNums, locationList, fixedNums)
    elif stockPath == '' and fixedNums == '' and maxNums != '':
        # 不混随机模式
        stockSkuList = writeMaxNums(skuNums, locationList, floatWide, maxNums)
    elif stockPath == '' and fixedNums == '' and maxNums == '':
        # 混箱模式
        stockSkuList = writeMixNums(skuNums, locationList, floatWide, mixLevel,
                                    maixNums)
    else:
        print('库存生成输入参数错误，请检查！')

    # 写库存文件
    if stockPath != '' and fixedNums == '' and maxNums == '':
        pass
    else:
        tarFile = os.path.join(tarPath, "./inv.csv")
        stockFile = codecs.open(tarFile, 'w', 'gbk')
        writer = csv.writer(stockFile)
        for i in stockSkuList:
            writer.writerow(i)

    return True


def mirStockCreate(tarPath, mirrorSource, mirrorTar):
    print(tarPath, mirrorSource, mirrorTar)

    return True


if __name__ == '__main__':
    orderPath = 'E:/Matrix小组/算法模拟参数工具/订单库存/order.xlsx'
    skuCodeFile = 'E:/Matrix小组/算法模拟参数工具/订单库存/新建文件夹/skuCode.csv'
    locationsPath = 'E:/Matrix小组/算法模拟参数工具/地图/kubot_GUI生成规则及前后的输入输出demo/最后使用的文件/109_LZ_JD_New/locations.csv'

    stockPath = 'E:/Matrix小组/算法模拟参数工具/订单库存/模拟库存.xlsx'
    # stockPath = ''
    # tarPath = 'E:\\2021春节工作资料\Matrix组\算法模拟参数工具\订单库存\新建文件夹'
    tarPath = 'E:/Matrix小组/算法模拟参数工具/订单库存/新建文件夹'
    floatWide = '20'
    fixedNums = ''
    maxNums = ''
    mixLevel = '1,2,3,4,5'
    maixNums = '100'

    stockCreate(orderPath, skuCodeFile, locationsPath, stockPath, tarPath,
                floatWide, fixedNums, maxNums, mixLevel, maixNums)
