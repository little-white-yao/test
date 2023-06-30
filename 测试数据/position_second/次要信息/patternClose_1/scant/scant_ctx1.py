import xlwt
import os
from os import path
import random

text_condition = ("C2",)
bin_kind = ("0",)
framed_count = {"arco_valentino_dense_vox20": 1,
                "egyptian_mask_vox20": 1,
                "facade_00009_vox20": 1,
                "facade_00015_vox20": 1,
                "facade_00064_vox20": 1,
                "frog_00067_vox20": 1,
                "head_00039_vox20": 1,
                "house_without_roof_00057_vox20": 1,
                "landscape_00014_vox20": 1,
                "palazzo_carignano_dense_vox20": 1,
                "shiva_00035_vox20": 1,
                "stanford_area_2_vox20": 1,
                "stanford_area_4_vox20": 1,
                "staue_klimt_vox20": 1,
                "ulb_unicorn_hires_vox20": 1,
                "ulb_unicorn_vox20": 1}
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
    attribute = [0 for n in range(15 + len(newDataName))]
    recyle_time = True
    PSNR_time = 0
    singlePlyCount = framed_count[plyname]

    driftQCount = 0
    planeCount = 0

    for all_line in lines:
        line = all_line.split()
        if len(line) >= 2:
            if line[0] == "Total" and line[1] == "frame":
                attribute[0] += int(line[3])*8
            if len(line) > 6 and line[0] == "positions" and line[1] == "bitstream" and line[6] == "bpp)":
                attribute[1] += int(line[3])*8
            if line[0] == "colors" and line[1] == "bitstream" and len(line) > 6 and line[6] == "bpp)":
                attribute[2] += int(line[3])*8
            if line[0] == "Processing" and line[1] == "time" and line[2] == "(user):":
                if recyle_time == True:
                    attribute[13] += float(line[3])
                    # recyle_time=False
                # else:
                    # attribute[14]+=float(line[3])
                    recyle_time = True

                    for nameIdx in range(len(newDataName)):
                        if (newDataSliceCount[nameIdx]):
                            attribute[15 +
                                      nameIdx] /= newDataSliceCount[nameIdx]
                    newDataSliceCount = [0 for n in range(len(newDataName))]

                    value_list.append(attribute)
                    attribute = [0 for n in range(15 + len(newDataName))]
            if line[0] == "Job" and line[1] == "done!":
                value_list.append(attribute)
                attribute = [0 for n in range(15 + len(newDataName))]
            elif line[0] == "mseF,PSNR" and line[1] == "(p2point):":
                attribute[3] += float(line[2])
            elif line[0] == "mseF,PSNR" and line[1] == "(p2plane):":
                attribute[8] += float(line[2])
            elif line[0] == "h.r,PSNR" and line[1] == "(p2point):" and line[2] == "F":
                attribute[9] += float(line[3])
            elif line[0] == "c[0],PSNRF":
                attribute[4] += float(line[2])
            elif line[0] == "c[1],PSNRF":
                attribute[5] += float(line[2])
            elif line[0] == "c[2],PSNRF":
                attribute[6] += float(line[2])
            elif line[0] == "h.c[0],PSNRF":
                attribute[9] += float(line[2])
            elif line[0] == "h.c[1],PSNRF":
                attribute[10] += float(line[2])
            elif line[0] == "h.c[2],PSNRF":
                attribute[11] += float(line[2])
            elif line[0] == "r,PSNR" and line[1] == "F":
                attribute[7] += float(line[3])
            elif line[0] == "h.r,PSNR" and line[1] == "F":
                attribute[12] += float(line[3])
            for nameIdx in range(len(newDataName)):
                if (line[0] == newDataName[nameIdx]):
                    inputIdx = 15 + nameIdx
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
        tile_infor = ["Total", "geometry", "attributes", "D1_PSNR",
                      "Y_PSNR", "U_PSNR", "V_PSNR", "R_PSNR", "D1_Haus",
                                "Y_Haus", "U_Haus", "V_Haus", "R_Haus",
                                "encoder_time", "decoder_time"]

        for newData in newDataName:
            tile_infor.append(newData)

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
                    for list_data in value_list:
                        column = 1
                        for data in list_data:
                            sheet.write(row, column, data)
                            column += 1
                        row += 1

    xls.save(workpath+"\\"+output_name+".xls")


read_txt(text_condition, "scant_patternClose_1")
