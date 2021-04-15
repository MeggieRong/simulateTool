# coding:utf-8

import xlrd
from util.orderOperate import writeJDOrderSku, otherOrderSku


def orderConvert(sourceFile, targetFile, intervalTime, interval, deadline, ifRecombine):
    # 读入源订单文件，判断是否京东项目
    readbook = xlrd.open_workbook(sourceFile)
    sheet = readbook.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    # 写订单（订单编号、SKU、下发间隔
    if ifRecombine == 1 or ifRecombine == 2:
        writeJDOrderSku(targetFile, sheet, nrows, ncols,
                        intervalTime, interval, deadline, ifRecombine)
    else:
        otherOrderSku(targetFile, sheet, nrows, ncols, intervalTime, interval)

    return True


if __name__ == '__main__':
    # sourceFile = 'E:\业务测试\项目需求\Youyiku地图\828地图数据\优衣库点位(模拟版）(1).xls'
    # sourceFile = 'E:\业务测试\项目需求\武汉新宁\地图坐标\SMT区域V6.1 for SIMU.csv'
    sourceFile = r'E:\Matrix小组\算法模拟参数工具\订单库存\test_order(1).xlsx'
    targetFile = r'E:\Matrix小组\算法模拟参数工具\订单库存\新建文件夹'
    intervalTime = 1
    interval = 5
    deadline = 25

    orderConvert(sourceFile, targetFile, intervalTime, interval, deadline)
