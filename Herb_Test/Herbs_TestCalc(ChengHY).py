import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt 
from matplotlib import dates as mpl_dates
from sympy import S, symbols, printing
from scipy.optimize import curve_fit


#===== Read Xlsx file and its' Sheets (Begin)
#----- Path and File of Excel as well as Specifying Sheets (Begin)
pfn = 'C:\\Users\\Administrator\\Desktop\\量表.xlsx'
sht1 = 'Sheet1'
#----- Path and File of Excel as well as Specifying Sheets (End)

'''
#----- (Demo:) Reading the specific sheet of the xlsx book (Start)
data = pd.read_excel(pfn, sht1)  #('Path/FileName.xlsx','SheetName')
print('data=', data)
# From the specific sheet of the xlsx book, reading specific columns and rows; use the multi-axes indexing funtion
print (data.loc[[21,23,25],['新增重症病例','新增死亡病例']])
#----- (Demo:) Reading the specific sheet of the xlsx book (End)
'''

#----- Reading Multiple Excel Sheets (Begin)
start=1; end=15 # start and end for the x arange of the data getting from a Column Xlsx
with pd.ExcelFile(pfn) as xlsBook:
    sht1_da = pd.read_excel(xlsBook, sht1) # from xlsBook, read sht1 to sht1_da
    #get array from specific Column of sht1_da
    herbName = sht1_da[start:end]['中药名称'] #中药名称
    herbXing = sht1_da[start:end]['性'] #性
    herbQXX = sht1_da[start:end]['趋向性'] #趋向性
    herbQXing = np.vstack((herbQXX, herbXing))
    print(herbQXing)
    print(herbQXing.T)
    herbFZL = sht1_da[start:end]['分子量'] #分子量
    herbRD = sht1_da[start:end]['熔点（℃）'] #熔点（℃）
    herbFD = sht1_da[start:end]['沸点（℃ at 760 mmHg）'] #沸点（℃ at 760 mmHg）
    herbSD = sht1_da[start:end]['闪点（℃）'] #闪点（℃）

    #get array from specific Column of sht2_da
    #......
    
print("\n**** Result from parts of sht1_da ****")
print ('\nherbName=\n', herbName, '\nherbXing=\n', herbXing, '\nherbQXX=\n', herbQXX,
       '\nherbFZL=\n', herbFZL, '\nherbRD=\n', herbRD, '\nherbFD=\n', herbFD, '\nherbSD=\n', herbSD)


#----- Reading Multiple Excel Sheets (End)
#===== Read Xlsx file and its' Sheets (End)



