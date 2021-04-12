#coding:utf-8

import xlrd
import csv

# xls转csv
def fileConvertFunction(sourceFile, targetFile):
    # 读取源文件
    mapdataList = readFile(sourceFile)

    # 将货位点和非货位点写入CSV文件
    csvPath = targetFile + '\mapData.csv'
    csvFile = open(csvPath, 'w', newline='')
    try:
        # 创建并打开mapData.csv文件
        writer = csv.writer(csvFile)
        writer.writerows(mapdataList)
    finally:
        csvFile.close()

    # print('xls转csv文件成功')

def readFile(sourceFile):
    fileType = sourceFile[-3:]
    mapDataList = []

    if fileType == 'xls' or fileType == 'lsx':
        mapdatalist = xlrd.open_workbook(sourceFile)
        sheet = mapdatalist.sheet_by_index(0)
        nrow = sheet.nrows

        # 找到颜色列
        for i in range(sheet.ncols):
            if sheet.cell(0, i).value in ('颜色', 'Color', 'color'):
                ncol = i
                break

        # 将货位点和非货位点写入CSV文件
        count = 0
        for j in range(nrow):
            count += 1
            if count == 1:
                continue

            # 遍历xls文件取出货位点和非货位点，颜色为洋红：货架取放货点
            if sheet.cell(j, ncol).value != '':
                if sheet.cell(j, ncol).value in ('洋红', 'Magenta', 'magenta'):
                    x = sheet.cell(j, ncol + 1).value
                    y = sheet.cell(j, ncol + 2).value
                    isMagenta = 1
                else:
                    x = sheet.cell(j, ncol + 1).value
                    y = sheet.cell(j, ncol + 2).value
                    isMagenta = 0

                maplist = [x, y, isMagenta]
                mapDataList.append(maplist)
    elif fileType == 'csv':
        with open(sourceFile, 'r') as f:
            reader = csv.reader(f)

            count = 0
            for row in reader:
                for k in range(0, len(row)):
                    if row[k] in ('颜色', 'Color', 'color'):
                        ncol = k
                        break

                count += 1
                if count == 1:
                    continue

                if row[ncol] != '':
                    x = row[ncol + 1]
                    y = row[ncol + 2]
                    if row[ncol] in ('洋红', 'Magenta', 'magenta'):
                        isMagenta = 1
                    else:
                        isMagenta = 0
                    maplist = [x, y, isMagenta]
                    mapDataList.append(maplist)

    return mapDataList

if __name__ == '__main__':
    sourceFile = 'D:\DingDing\DingDingTalk\优衣库点位(模拟版）.xls'
    # sourceFile = 'E:\业务测试\项目需求\武汉新宁\地图坐标\SMT区域V6.1 for SIMU.csv'
    targetFile = 'E:\地图数据\python地图工具'

    fileConvertFunction(sourceFile, targetFile)