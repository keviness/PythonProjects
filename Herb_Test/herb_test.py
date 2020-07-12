import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt 
from matplotlib import dates as mpl_dates
from sympy import S, symbols, printing
from scipy.optimize import curve_fit
import tkinter
from tkinter import filedialog, messagebox

#pfn = 'C:/Users/02ehr/Documents/量表.xlsx'
#----- Reading Multiple Excel Sheets (Begin)
# start and end for the x arange of the data getting 
# from a Column Xlsx
def showExcelFileData(filePath):
    start=1; end=15 
    sheetName = 'Sheet1'
    with pd.ExcelFile(filePath) as xlsBook:

    # from xlsBook, read sht1 to sht1_da
    #get array from specific Column of sht1_da

        sht1_da = pd.read_excel(xlsBook, sheetName) 
        herbName = sht1_da[start:end]['中药名称'] #中药名称
        herbXing = sht1_da[start:end]['性'] #性
        herbQXX = sht1_da[start:end]['趋向性'] #趋向性
        herbQXing = np.vstack((herbQXX, herbQXing))
        herbFZL = sht1_da[start:end]['分子量'] #分子量
        herbRD = sht1_da[start:end]['熔点（℃）'] #熔点（℃）
        herbFD = sht1_da[start:end]['沸点（℃ at 760 mmHg）'] #沸点（℃ at 760 mmHg）
        herbSD = sht1_da[start:end]['闪点（℃）'] #闪点（℃）

    print("\n**** Result from parts of sht1_da ****")
    print ('\nherbName=\n', herbName, '\nherbXing=\n', herbXing, '\nherbQXX=\n', herbQXX,
       '\nherbFZL=\n', herbFZL, '\nherbRD=\n', herbRD, '\nherbFD=\n', herbFD, '\nherbSD=\n', herbSD)

def getExcelFilePath():
    while True:
        answer = input("Do you want to search the excel file:(y/n)")[0]
        if answer == "y":
            win = tkinter.Tk()
            win.withdraw()
            filename = filedialog.askopenfilename().replace("/", "\\")
            if filename[-5:] == ".xlsx":
                filePath = filename
                print("Input successfully!")
            else:
                print("The file you input is not the true file, try again!")
                continue
        elif answer == "n":
            print("Exit successfully!")
            break
        else:
            print("The command you input error, try again!")
            continue
    print("Already get files information:")
    print(filePath)
    return filePath

def main():
    filePath = getExcelFilePath();
    showExcelFileData(filePath)

if __name__ == "__main__":
    main()
