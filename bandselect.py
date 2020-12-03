'''
@brief:实现GF1/2/6以及HY1C卫星数据的波段提取
@author:zangjinxia
@date:2020/12/3
'''

import gdal
import numpy as np
import platform


# !/usr/bin/env Python
# coding=utf-8

def logInfo(string):
    print(string)


def logError(string):
    print("[ERROR] " + string)


def EncodeUtf8(string):
    sys = platform.system()
    if sys == "Windows":
        strCode = (unicode(string.decode("gbk").encode("utf-8"), 'utf8'))
        return strCode
    else:
        return string


def read_img(filename):
    dataset = gdal.Open(filename)

    width = dataset.RasterXSize
    height = dataset.RasterYSize
    band = dataset.RasterCount
    im_data = dataset.ReadAsArray(0, 0, width, height)

    geotrans = dataset.GetGeoTransform()
    proj = dataset.GetProjection()
    # data = np.zeros([width, height, band])

    return im_data, proj, geotrans, width, height


def write_tiff(filename, proj, geotrans, data):
    # gdal数据类型包括
    # gdal.GDT_Byte,
    # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
    # gdal.GDT_Float32, gdal.GDT_Float64
    # 判断栅格数据的数据类型
    if 'int8' in data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    # 判读数组维数
    if len(data.shape) == 3:
        bands, height, width = data.shape
    else:
        bands = 1
        height, width = data.shape
    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(filename, width, height, bands, datatype)
    ListgeoTransform1 = list(geotrans)
    ListgeoTransform1[5] = -ListgeoTransform1[5]
    newgeoTransform1 = tuple(ListgeoTransform1)
    dataset.SetGeoTransform(newgeoTransform1)
    dataset.SetProjection(proj)

    if bands == 1:
        dataset.GetRasterBand(1).WriteArray(data)
    else:
        for i in range(bands):
            dataset.GetRasterBand(i + 1).WriteArray(data[i])
    del dataset


def bandSelect(raster, outtif, bandlist):
    dataArray3 = []
    data, proj, geotrans, width, height = read_img(raster)

    for i in bandlist:
        dataArray3.append(data[i - 1])
    # dataArray3.append(data[bandlist[1] - 1])
    # dataArray3.append(data[bandlist[2] - 1])
    laydata = np.array(dataArray3)
    write_tiff(outtif, proj, geotrans, laydata)


if __name__ == '__main__':
    print("start")

    # 输入需提取的波段号，存在列表中
    band1 = "1"
    band2 = "2"
    band3 = "3"
    bandlist = [band1]
    bandList = [int(i) for i in bandlist]

    # 输入输出影像
    tif = 'D:/AAdata/GF1_WFV4_E112.6_N21.8_20180721_L1A0003341047/GF1_WFV4_E112.6_N21.8_20180721_L1A0003341047.tiff'
    outtif = 'D:/AAdata/GF1_WFV4_E112.6_N21.8_20180721_L1A0003341047/bandselect2.tiff'

    print("开始波段提取")

    # 波段提取
    bandSelect(tif, outtif, bandList)
    print("波段提取完成")
