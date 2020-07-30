import numpy as np 
import pandas as pd
#import sys
#from matplotlib import pyplot as plt 
#from matplotlib import style
#style.use("ggplot")
#from openpyxl import *
from sklearn import svm
import tkinter
from tkinter import filedialog
import openpyxl
#----------------机器学习:用向量机进行匹配---------------
def getsvm(trainSet,tmpltSet,ptnset):
    clf = svm.SVC(kernel='linear', C = 1.0)
    clf.fit(trainSet, tmpltSet)
    result = clf.predict(ptnset)
    return result
#------------------获取excel文件路径---------------
def getExcelFilePath():
    while True:
        question = input("Do you want to get a excel file?(yes(y)/no(n)")[0]
        if question in ["y", "Y"]:
            win = tkinter.Tk()
            win.withdraw()
            path = filedialog.askopenfilename().replace("/", "\\")
            if path[-4:] != "xlsx":
                print("The file is not a excel file, try again:")
                continue
            print("The excel %s input successfully!" %path)
            return path
        elif question in ["n", "N"]:
            print("Exiting......")
            break
        else:
            print("The choice is wrong, try again:")

#----- get trainSet, ptnSet and tmpltSet-----
def getSetDatas(data, selectItemName):
    #SourceData = pd.read_excel(path, sheet_name=sheetName, engine="openpyxl")  
    popItem = data.drop(index=selectItemName)

    #Train set
    TrainSetArray = np.array(popItem)

    #TmpltSet
    TmpltSet = popItem.index
    TmpltSetArray = np.array(TmpltSet)

    #PtnSet
    PtnSet = data.loc[selectItemName]
    PtnSetArray = np.array([PtnSet])

    result = (TrainSetArray, TmpltSetArray, PtnSetArray)

    return result

#----------------write to Excel File--------------------
def writeToExcelFile(path, resultList):
    selectedHerbName = resultList[:, 0]
    attribute_selected = resultList[:, 1]
    matchedHerbName = resultList[:, 2]
    attribute_matched  = resultList[:, 3]
    dataResult = pd.DataFrame({"待测药":selectedHerbName, "待测药趋向性":attribute_selected, "匹配药":matchedHerbName, "匹配药趋向性":attribute_matched})
    wb = openpyxl.load_workbook(path)
    writer = pd.ExcelWriter(path, engine="openpyxl")
    writer.book = wb
    dataResult.to_excel(writer, sheet_name="result", columns=None)
    writer.save()
    writer.close()
    print("Write to the excel file successfully!")

#---------------handle source data--------------
def handleSourceData(path, sheetName):
    with pd.ExcelFile(path) as xlsbook:
        SourceData = pd.read_excel(xlsbook, sheet_name=sheetName)
        SourceData = SourceData.set_index("中药名称").loc[:, "趋向性":]
        SourceData = SourceData.dropna(axis=0) #除去含有缺失值的行
        #SourceData = SourceData.dropna(axis=1) #除去含有缺失值的列
    return SourceData

#---------------main function-------------------
def main():
    sheetName = 'GdaSet'
    path = getExcelFilePath()
    Data = handleSourceData(path, sheetName)
    resultList = []
    itemNames = list(Data.index)
    for item in itemNames:
        attribute_item = int(Data.loc[item, ["趋向性"]].values[0])
        dataSample = Data.loc[:, "C数":]
        setDatas = getSetDatas(dataSample, item)
        matchResult = getsvm(setDatas[0], setDatas[1], setDatas[2])[0]
        attribute_result = int(Data.loc[matchResult, ["趋向性"]].values[0])
        print("The herb:{0:}, attribute_item:{1:}, match result: {2:}, attribute_result:{3:}\n".format(item, attribute_item, matchResult, attribute_result))
        resultList.append([item, attribute_item, matchResult, attribute_result])
    writeToExcelFile(path, np.array(resultList))

if __name__ == "__main__":
    main()
