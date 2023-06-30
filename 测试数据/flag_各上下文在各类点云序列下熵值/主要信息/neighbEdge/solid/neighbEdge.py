import xlwt
import os
from os import path
import random

text_condition = ("C2",)
bin_kind = ("0",)
framed_count = {"basketball_player_vox11_00000200": 1,
                "dancer_vox11_00000001": 1,
                "Facade_00064_vox11": 1,
                "longdress_vox10_1300": 1,
                "loot_vox10_1200": 1,
                "queen_0200": 1,
                "redandblack_vox10_1550": 1,
                "soldier_vox10_0690": 1,
                "Thaidancer_viewdep_vox12": 1}
# framed_count={"Egyptian_mask_vox12":1,
# "ULB_Unicorn_vox13":1}
workpath = path.dirname(__file__)
Text_paths = []
for i in range(1):
    # Text_paths.append(workpath+"\\"+text_condition[i]+"\\"+"Text")
    Text_paths.append(workpath+"\\"+"Text")


newDataName = ["entropy"]
newDataSliceCount = [0 for n in range(len(newDataName))]
newDataRateIdx = [2 for n in range(len(newDataName))]


def readTxt_list(lines, plyname):
    global newDataSliceCount
    value_list = []
    attribute = [0 for n in range(len(newDataName))]
    recyle_time = True
    PSNR_time = 0
    singlePlyCount = framed_count[plyname]

    driftQCount = 0
    planeCount = 0

    for all_line in lines:
        line = all_line.split()
        if len(line) >= 2:
            if line[0] == "Processing" and line[1] == "time" and line[2] == "(user):":
                if recyle_time == True:
                    for nameIdx in range(len(newDataName)):
                        if (newDataSliceCount[nameIdx]):
                            attribute[nameIdx] /= newDataSliceCount[nameIdx]
                    newDataSliceCount = [0 for n in range(len(newDataName))]

                    value_list.append(attribute)
                    attribute = [0 for n in range(len(newDataName))]

            for nameIdx in range(len(newDataName)):
                if (line[0] == newDataName[nameIdx]):
                    inputIdx = nameIdx
                    inputRateIdx = newDataRateIdx[nameIdx]
                    inputRate = line[inputRateIdx]
                    attribute[inputIdx] += float(inputRate)

            if line[0] == "Loop" and line[1] == "on":
                newDataSliceCount[nameIdx] += 1

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
    xls = xlwt.Workbook(encoding="ANSI")
    for condition in text_condition:
        sheet = xls.add_sheet(condition)
        sheet.write(0, 0, "name")
        sheet.write(0, 1, "entropy")
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
                    for list_data in value_list:
                        column = 1
                        for data in list_data:
                            sheet.write(row, column, data)
                            column += 1
                        row += 1

    xls.save(workpath+"\\"+output_name+".xls")


read_txt(text_condition, "neighbEdge")
