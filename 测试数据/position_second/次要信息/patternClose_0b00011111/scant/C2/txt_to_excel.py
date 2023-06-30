import xlwt  # excel写入函数库
import os
from os import path
import random  # 随机数函数

text_condition = ("C2",)  # trisoup里只有C2一种
bin_kind = ("0",)
r = ["r01", "r02", "r03", "r04", "r05", "r06"]
global slice
#framed_count = {"basketball_player_vox11_00000200": 1, }
framed_count={"arco_valentino_dense_vox20":1,
              "egyptian_mask_vox20":1,
              "facade_00009_vox20":1,
              "facade_00015_vox20":1,
              "facade_00064_vox20":1,
              "frog_00067_vox20":1,
              "head_00039_vox20":1,
              "house_without_roof_00057_vox20":1,
              "landscape_00014_vox20":1,
              "palazzo_carignano_dense_vox20":1,
              "shiva_00035_vox20":1,
              "stanford_area_2_vox20":1,
              "stanford_area_4_vox20":1,
              "staue_klimt_vox20":1,
              "ulb_unicorn_hires_vox20":1,
              "ulb_unicorn_vox20":1}
workpath = path.dirname(__file__)  # workpath是E:根目录地址
Text_paths = []  # 存储Text地址
for i in range(1):  # 只有一个循环i=0
    Text_paths.append(workpath+"\\"+"Text")  # 加一个workpath\Text地址


def readTxt_list(lines, plyname):
    t1 = False
    t2 = False
    t3 = False
    t4 = False
    value_list = []
    attribute = [0 for n in range(4)]  # 重置
    global slice
    PSNR_time = 0
    singlePlyCount = framed_count[plyname]
    for all_line in lines:
        line = all_line.split()  # 以空格为分隔符号，包含\n,返回分割后的字符串列表
        if len(line) >= 2:
            if line[0] == "ctx1SegCtx" and line[1] == "is" and line[3] == "0":
                attribute[0] += float(line[6])
                t1 = True
            if line[0] == "ctx1SegCtx" and line[1] == "is" and line[3] == "1":
                attribute[1] += float(line[6])
                t2 = True
            if len(line) > 8 and line[0] == "the" and line[1] == "ctx1SegCtx" and line[7] == "rate":
                attribute[2] += float(line[9])
                t3 = True
                # 取得某一个slice里面某一个上下文值情况下结果
            if line[0] == "entropy" and line[1] == "is":
                attribute[3] += float(line[2])
                t4 = True
            if line[0] == "Slice" and line[1] == "number:":
                slice = float(line[2])
            # if line[0] == "Processing" and line[1] == "time":
                # 某一码率点结束了，计算该码率点下的熵

        if t1 == True and t2 == True and t3 == True and t4 == True:
            value_list.append(attribute)
            attribute = [0 for n in range(4)]
            t1 = False
            t2 = False
            t3 = False
            t4 = False
        # 循环此结构，存储所有slice中该上下文所有情况下结果

    return value_list


def text_to_excel(sheet, attribute_list, tile_infor, excel_name, row, ply_name, xls, output_name):
    sheet.write(row, 0, ply_name)
    for list_data in attribute_list:
        column = 1
        for data in list_data:
            sheet.write(row, column, data)
            column += 1
        row += 1


def read_txt(text_condition, output_name):
    xls = xlwt.Workbook(encoding="ANSI")  # excel的编码格式为ANSI
    global slice
    write = 1
    for condition in text_condition:
        sheet = xls.add_sheet(condition)  # 新建立一个名为C2的sheet
        tile_infor = ["ctx1!=4", "ctx1=4"]  # 该上下文变量取值
        ls = 2
        for head in tile_infor:
            sheet.write(0, ls, head)
            ls += 1
        sheet.write(0, 0, "segind")
        sheet.write(2, 0, 1)
        sheet.write(3, 0, "rate")
        sheet.write(4, 0, "entropy")
        column = 2
        row = 1
        n = 1
        temprow = 1
        for name in framed_count:
            k = 0
            s = 1
            for B in bin_kind:
                # _dir=workpath+"\\"+condition+"\\"+"Text"+"\\"
                _dir = workpath+"\\"+"Text"
                if os.path.exists(_dir+"\\"+name+"_"+B+".txt"):
                    file_txt = open(_dir+"\\"+name+"_"+B +
                                    ".txt", 'r')  # 打开该地址下的txt文件
                    value_list = []
                    lines = file_txt.readlines()  # 每一行作为一个list存储
                    value_list = readTxt_list(lines, name)

                    sheet.write(row, 0, name+"_"+B)  # 注明序列名称

                    for list_data in value_list:
                        if (s == 1 or ((s-1) % slice) == 0) and write == 1:
                            sheet.write(row, 1, r[k])
                            k += 1
                            write = 0
                        for data in list_data:
                            sheet.write(row, column, data)
                            row += 1
                        column += 1
                        row = temprow
                        if column == 4:  # 根据上下文值的可取数量变化
                            column = 2
                            n += 1
                            s += 1
                            row = 4*(n-1) + 1
                            temprow = row
                            write = 1

    xls.save(workpath+"\\"+output_name+".xls")  # 保存excel文件


read_txt(text_condition, "ctx1")
