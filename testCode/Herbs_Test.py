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



#TrainSet = 'TrainSet'
#PtnSet = 'PtnSet'
#TmpltSet = 'TmpltSet'

#----- get trainSet, ptnSet and tmpltSet-----
def getSetDatas(path, sheetName ,selectItemName):
    SourceData = pd.read_excel(path, sheet_name=sheetName)
    data = SourceData.set_index("中药名称")
    #print("SourceData:", data)
    popItem = data.drop(index=selectItemName)

    #Train set
    TrainSetArray = np.array(popItem)
    #print("popItem:", popItem)
    #print("TrainSet:", TrainSetArray)

    #TmpltSet
    TmpltSet = popItem.index
    TmpltSetArray = np.array(TmpltSet)
    #print("Ptnset:", PtnSet)
    #print("TmpltSetArray:",TmpltSetArray)

    #PtnSet
    PtnSet = data.loc[selectItemName]
    PtnSetArray = np.array([PtnSet])

    result = (TrainSetArray, TmpltSetArray, PtnSetArray)
    #print(result)
    return result

def main():
    sheetName = 'GdaSet'
    try:
        path = getExcelFilePath()
        SourceData = pd.read_excel(path, sheet_name=sheetName)
        data = SourceData.set_index("中药名称")
    except:
        print("Can\'t get the sourceData")
        return

    while True:
        itemNames = np.array(data.index)
        for index, value in enumerate(itemNames):
            print("{0:<10} {1:>10}".format(index, value))
        choice = input("Do you want to quit?(y/n)")[0]
        if choice in ["y", "Y"]:
            print("The done, bye~")
            break
        elif choice in ["n", "N"]:
            selectItemName = input("Enter the selected item name:")
            setDatas = getSetDatas(path, sheetName, selectItemName)
            matchResult = getsvm(setDatas[0], setDatas[1], setDatas[2])
            print("The match result: \n", matchResult)
        else:
            print("The choice is wrong, try again!")

if __name__ == "__main__":
    main()

'''
df = SourceData["性"]
print(df)
writer = pd.ExcelWriter(path[0])
SourceData.to_excel(writer, sheet_name="sourceData")
df.to_excel(writer, sheet_name="select")
writer.close()
data = pd.read_excel(path[0])
print("data:\n", data)
'''