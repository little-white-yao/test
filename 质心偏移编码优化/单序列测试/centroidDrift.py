import xlwt
import os
from os import path
import random

text_condition = ("C2",)
bin_kind = ("0",)
framed_count = {"enc-r01": 1}
workpath = path.dirname(__file__)
Text_paths = []
for i in range(1):

    Text_paths.append(workpath+"\\"+"Text")


def readTxt_list(lines, plyname):
    global newDataSliceCount
    value_list = []

    attribute_1 = [0 for n in range(91)]
    attribute_2 = [0 for n in range(91)]
    attribute_3 = [0 for n in range(91)]
    recyle_time = True

    sliceCount = 0
    for all_line in lines:
        line = all_line.split()
        if len(line) >= 2:
            if line[0] == "Processing" and line[1] == "time" and line[2] == "(user):":
                for ctx in range(91):
                    if (sliceCount):
                        attribute_1[ctx] /= sliceCount
                        attribute_2[ctx] /= sliceCount
                sliceCount = 0
                value_list.append(attribute_1)
                attribute_1 = [0 for n in range(91)]
                value_list.append(attribute_2)
                attribute_2 = [0 for n in range(91)]
                value_list.append(attribute_3)
            for ctx in range(91):
                ctx = str(ctx)
                name_1 = ctx+"result1"
                name_2 = ctx+"result2"

                name_3 = ctx+"numAll"
                ctx = int(ctx)
                if line[0] == name_1:
                    attribute_1[ctx] += float(line[2])
                if line[0] == name_2:
                    attribute_2[ctx] += float(line[2])
                if line[0] == name_3:
                    attribute_3[ctx] += float(line[2])
            if line[0] == "Loop" and line[1] == "on":
                sliceCount += 1
    return value_list


def read_txt(text_condition, output_name):
    xls = xlwt.Workbook(encoding="ANSI")
    for condition in text_condition:
        sheet = xls.add_sheet(condition)
        tile_infor = ["result1", "result2", "num"]

        ls = 1
        for head in tile_infor:
            sheet.write(0, ls, head)
            ls += 1
        row = 1
        for name in framed_count:
            for B in bin_kind:
                #_dir = workpath+"\\"+condition+"\\"+"Text"+"\\"
                _dir = workpath+"\\"+"Text"
                if os.path.exists(_dir+"\\"+name+"_"+B+".txt"):
                    file_txt = open(_dir+"\\"+name+"_"+B+".txt", 'r')
                    value_list = []
                    lines = file_txt.readlines()
                    value_list = readTxt_list(lines, name)
                    sheet.write(row, 0, name+"_"+B)
                    column = 1
                    for list_data in value_list:
                        row = 1
                        for data in list_data:
                            sheet.write(row, column, data)
                            row += 1
                        column += 1

    xls.save(workpath+"\\"+output_name+".xls")


read_txt(text_condition, "centroid_map")
