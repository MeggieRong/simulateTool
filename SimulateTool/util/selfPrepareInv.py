#-*- coding: utf-8 -*-
from numpy.core.numeric import False_
import pandas as pd
import numpy as np
import sys
import math
import itertools
from sklearn.utils import shuffle
from tqdm import tqdm
import random
import warnings
warnings.filterwarnings("ignore")


def createInv(orderPath, locationsPath, stockPath, tarPath, skuCodeFile):
    global invFile
    orderFile = pd.read_excel(orderPath, usecols=['订单号', '商品编码', '实际拣货量'])

    orderFile.rename(columns={
        '订单号': 'orderNo',
        '商品编码': 'sku',
        '实际拣货量': 'orderQty'
    },
                     inplace=True)

    locationFile = pd.read_csv(locationsPath,
                               names=[
                                   'locationId', 'nothingOne', 'nothingTwo',
                                   'x', 'y', 'z', 'nothingThree', 'nothingFour'
                               ],
                               header=None)
    locationFile = pd.DataFrame(locationFile['locationId'])

    invFile = pd.read_excel(stockPath)
    invFile.rename(columns={
        '装箱件数': 'maxQtyEachBin',
        '料箱需求': 'slotType',
        '库存': 'invQty'
    },
                   inplace=True)

    skuCodeFile = pd.read_csv(skuCodeFile, names=['mapSku', 'sku'])

    invFile.sku = invFile.sku.apply(lambda x: str(x))
    orderFile.sku = orderFile.sku.apply(lambda x: str(x))
    skuCodeFile.sku = skuCodeFile.sku.apply(lambda x: str(x))

    slotTypeList = []
    skuNeedQty = pd.DataFrame()

    def firstFilterInv():
        global firstFilter
        """
        订单需要的sku都可以在库存找到
        """
        try:
            invFile.sku = invFile.sku.apply(lambda x: x.split(' ')[0])
            orderFile.sku = orderFile.sku.apply(lambda x: x.split(' ')[0])
            skuCodeFile.sku = skuCodeFile.sku.apply(lambda x: x.split('\t')[0])
        except:
            pass
        invSku = set(invFile.sku.to_list())
        orderSku = set(orderFile.sku.to_list())
        filterSkuContain = orderSku.issubset(invSku)

        if filterSkuContain == True:
            firstFilter = True
            print('we can find all needed sku in inv file,good job!')
            # print('订单需要的sku都在库存找到')
        else:
            print(
                'Thers is some sku we cannot find in inv file, please double check'
            )
            # print('订单所需sku在库存不存在，请检查')
            sys.exit()
        return firstFilter

    def caseTwoQrtCheck():
        global skuNeedQty, invFile
        """
        现有库存件数是否满足订单所需
        """
        skuNeedQty = orderFile.groupby('sku').orderQty.sum().reset_index()
        invFile = pd.merge(invFile, skuNeedQty, how='left', on='sku')
        invFile.reset_index(inplace=True, drop=True)
        invFile.orderQty.fillna(1, inplace=True)
        invFile.orderQty = invFile.orderQty.astype('int')
        ifSatisfy = (invFile.invQty.values < invFile.orderQty.values).any()
        if ifSatisfy == True:
            print(
                'now qrt in inv is not enough for order,we have used order qrt to fix it'
            )
            # print('现有库存件数不满足订单所需,已用订单总件数补齐库存件数')
            for i in range(0, len(invFile)):
                if invFile.at[i, 'invQty'] < invFile.at[i, 'orderQty']:
                    invFile.at[i, 'invQty'] = invFile.at[i, 'orderQty']
            del invFile['orderQty']
        else:
            del invFile['orderQty']
            print('now qrt in inv is enough for order')
            # print('现有库存件数满足订单所需')
        return invFile

    def secondFilterInv():
        needbinNum = []
        global skuNeedQty
        """
        库位是否足够
        """
        skuNeedQty = orderFile.groupby('sku').orderQty.sum().reset_index()
        for i in range(0, len(skuNeedQty)):
            skuMaxQtyEachBin = invFile[invFile.sku == skuNeedQty.at[
                i, 'sku']].iloc[0].maxQtyEachBin
            needMinBinNum = math.ceil(skuNeedQty.at[i, 'orderQty'] /
                                      int(skuMaxQtyEachBin))
            needbinNum.append(needMinBinNum)
        if sum(needbinNum) < len(locationFile):
            secondFilter = 'Y'
        else:
            print('location num is not enough.Plaese double check')
            # print('库位数不够，请检查箱规或者减少订单')
            sys.exit()
        return secondFilter

    def simpleClean(column):
        global useInvFile, invFile, skuNeedQty
        # 保留库存中订单需要的sku
        invFile = invFile[invFile.sku.isin(set(orderFile.sku.to_list()))]

        # 合并库存表和订单sku透视表
        invFile = pd.merge(invFile, skuNeedQty, how='left', on='sku')

        # 根据订单sku所需件数，除以库存表箱规，得到每个sku最少需要箱子数
        invFile['minNeedBinNum'] = invFile[column] / \
            invFile.maxQtyEachBin.astype('int')

        # 最少需要的箱子数向上取整
        invFile.minNeedBinNum = invFile.minNeedBinNum.apply(
            lambda x: math.ceil(x))

        # 判断如果最少需要箱子数低于3个箱子，则给与3个箱子。其他不变
        for i in invFile.sku.to_list():
            if invFile[invFile['sku'] == i].iloc[0]['minNeedBinNum'] < 3:
                invFile[invFile['sku'] == i].iloc[0]['minNeedBinNum'] = 3
            else:
                pass

        # 所示库存表useInvFile 只保留需要的字段
        useInvFile = invFile[[
            'sku', 'minNeedBinNum', 'slotType', 'maxQtyEachBin'
        ]]

        # 因为有分格，所以分格的sku的放到每个箱子的库存件数 = 箱规/分格数
        useInvFile.maxQtyEachBin = useInvFile.maxQtyEachBin.apply(
            lambda x: int(float(x))) / useInvFile.slotType.apply(
                lambda x: int(float(x)))

        # 因为有分格，所以分格的sku的箱子数要 * 分格数
        useInvFile.minNeedBinNum = useInvFile.minNeedBinNum.apply(
            lambda x: int(float(x))) * useInvFile.slotType.apply(
                lambda x: int(float(x)))

        # 向上取整新的箱规
        useInvFile.maxQtyEachBin = useInvFile.maxQtyEachBin.apply(
            lambda x: math.ceil(x))

        # slotType格式有str转int
        useInvFile.slotType = useInvFile.slotType.apply(lambda x: int(x))

        # 返回初步库存表
        return useInvFile

    def getslotype(df):
        global slotTypeList
        slotTypeList = list(set(df.slotType.to_list()))
        slotTypeList = list(map(int, slotTypeList))
        return slotTypeList

    def repeat(df):
        """
        每个sku重复n次，表示要放n个箱子
        """
        newSkuList = []
        for i in tqdm(range(0, len(df))):
            skuRepeatList = list(
                np.repeat(df.at[i, 'sku'], df.at[i, 'minNeedBinNum']))
            newSkuList.append(skuRepeatList)
        return newSkuList

    def convertListIntoDf(ls):
        """
        简单处理嵌套list
        """
        lsTmp = []
        for i in ls:
            lsTmp += i
        return lsTmp

    def getSlotMain(df):
        global slotTypeList, newInv
        """
        赋予分格库位
        """
        n = 1
        newInv = pd.DataFrame()
        for i in slotTypeList:
            tmp = df[df.slotType == i]
            tmpQty = df[df.slotType == i][['sku', 'maxQtyEachBin']]
            tmp.reset_index(inplace=True, drop=True)
            newSkuListTmp = repeat(tmp)
            newSkuDf = pd.DataFrame(convertListIntoDf(newSkuListTmp),
                                    columns=['sku'])
            newSkuDf = shuffle(newSkuDf)
            newSkuDf = pd.merge(newSkuDf, tmpQty, how='left', on=['sku'])

            # 打乱库位
            locationNoNum = int(len(newSkuDf) / i)
            locationNo = pd.DataFrame(list(range(n, locationNoNum + n)),
                                      columns=['binNo'])
            locationNo['repeatTimes'] = i
            locationNoDf = np.repeat(locationNo['binNo'],
                                     locationNo['repeatTimes'])
            n = max(locationNo.binNo) + 1
            locationNoDf = shuffle(locationNoDf)
            locationNoDf.reset_index(inplace=True, drop=True)

            newSkuDf['locationNo'] = locationNoDf
            newInv = newInv.append(newSkuDf)
        newInv.reset_index(inplace=True, drop=True)

        newInv = newInv[['locationNo', 'sku', 'maxQtyEachBin']]
        newInv.rename(columns={'maxQtyEachBin': 'qty'}, inplace=True)
        return newInv

    def addExtraInv():
        global invFinally
        """
        添加额外的垃圾库存
        """
        # 总库位数
        totalLocationNum = len(locationFile.locationId)

        # 订单所需库存占用库位数
        invNeedLocationNum = len(set(newInv.locationNo))

        # 订单所需库位数占据总库存数的百分比
        invPercentage = invNeedLocationNum / totalLocationNum

        # 如果上述百分比大于95%，则说明订单所需库存几乎占满了库位，则跳过
        if invPercentage >= 0.95:
            invFinally = newInv.copy()
        # 如果占比低于95%，则需要额外95%-百分比个库位放置垃圾sku，只留下5%空库位
        else:
            # 需要垃圾sku箱子数
            extraLocationNum = int(totalLocationNum * 0.95 -
                                   invNeedLocationNum)

            # 还可以分配的库位编号
            extralocationNoList = locationFile[~locationFile.locationId.isin(
                list(set(newInv.locationNo)))].locationId.to_list()
            extralocationNoList = list(map(int, set(extralocationNoList)))
            # 生成随机乱序垃圾sku并且在sku插入标识‘extra’
            extraLocationDf = pd.DataFrame(np.arange(extraLocationNum),
                                           columns=['sku'])
            extraLocationDf.sku = extraLocationDf.sku.apply(
                lambda x: str(x) + 'extra')

            # 垃圾sku一箱一件
            extraLocationDf['qty'] = 1

            # 给垃圾sku分配剩余的库位编号
            extraLocationDf['locationNo'] = random.sample(
                extralocationNoList, extraLocationNum)
            columns = ['locationNo', 'sku', 'qty']

            # 合并订单所需库存及垃圾库存
            invFinally = pd.concat([newInv, extraLocationDf], axis=0)
        return invFinally

    def convertInvSkuCode():
        global invFinally
        invFinally = pd.merge(invFinally, skuCodeFile, how='left', on=['sku'])
        invFinally.mapSku.fillna(invFinally.sku, inplace=True)
        del invFinally['sku']
        invFinally.rename(columns={'mapSku': 'sku'}, inplace=True)
        invFinally = invFinally[['locationNo', 'sku', 'qty']]
        return invFinally

    def caseOne():
        """
        有sku，箱规，所属料箱分格，没有库存件数
        """
        firstFilter = pd.DataFrame()
        useInvFile = pd.DataFrame()
        firstFilterInv()
        secondFilterInv()
        invdf = simpleClean('orderQty')
        slotTypeList = getslotype(invdf)
        invResult = getSlotMain(invdf)
        invFinally = addExtraInv()
        invFinally = convertInvSkuCode()
        return invFinally

    def caseTwo():
        """
        有sku，箱规，所属料箱分格，库存件数
        """
        firstFilterInv()
        invFile = caseTwoQrtCheck()
        secondFilterInv()
        invdf = simpleClean('invQty')
        slotTypeList = getslotype(invdf)
        invResult = getSlotMain(invdf)
        invFinally = addExtraInv()
        invFinally = convertInvSkuCode()
        return invFinally

    if invFile.invQty.sum() == 0 or len(invFile.invQty) == 0:
        invCaseOne = caseOne()
        invCaseOne.to_csv(tarPath + '/inv.csv', index=False)
    else:
        invCaseTwo = caseTwo()
        invCaseTwo.to_csv(tarPath + '/inv.csv', index=False)
    return True
