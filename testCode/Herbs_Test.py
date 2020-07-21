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

def getsvm(trainSet,tmpltSet,ptnset):
    clf = svm.SVC(kernel='linear', C = 1.0)
    clf.fit(trainSet, tmpltSet)
    result = clf.predict(ptnset)
    return result

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
def getSetDatas(path, sheetName ,selectItemName):
    SourceData = pd.read_excel(path, sheet_name=sheetName)
    data = SourceData.set_index("中药名称")
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

def writeToExcelFile(path, resultDict):
    keyList = []
    valueList = []
    for key in resultDict.keys():
        keyList.append(key)
        valueList.append(resultDict[key])
    dataResult = pd.DataFrame({"待测药":keyList, "匹配药":valueList})
    wb = openpyxl.load_workbook(path)
    writer = pd.ExcelWriter(path, engine="openpyxl")
    writer.book = wb
    dataResult.to_excel(writer, sheet_name="result", columns=None)
    writer.save()
    writer.close()
    print("Write to the excel file successfully!")

def main():
    sheetName = 'GdaSet'
    try:
        path = getExcelFilePath()
        SourceData = pd.read_excel(path, sheet_name=sheetName)
        data = SourceData.set_index("中药名称")
    except:
        print("Can\'t get the sourceData")
        return
    resultDict = {}
    while True:
        itemNames = list(data.index)
        print("The herb items:".center(30, "-"))
        for index, value in enumerate(itemNames):
            print("{0:<10} {1:>10}".format(index, value))
        choice = input("Do you want to quit?(y/n)")[0]
        if choice in ["y", "Y"]:
            print("The done, bye~")
            break
        elif choice in ["n", "N"]:
            selectItemNum = eval(input("Enter the selected herb name:"))
            while selectItemNum not in dict(enumerate(itemNames)).keys():
                print(selectItemNum)
                selectItemNum = eval(input("herb name input error!, Enter the selected herb name again:"))
            setDatas = getSetDatas(path, sheetName, itemNames[selectItemNum])
            matchResult = getsvm(setDatas[0], setDatas[1], setDatas[2])[0]
            print("The match result: \n", matchResult)
            resultDict[itemNames[selectItemNum]] = matchResult
        else:
            print("The choice is wrong, try again!")
    writeToExcelFile(path, resultDict)

if __name__ == "__main__":
    main()

