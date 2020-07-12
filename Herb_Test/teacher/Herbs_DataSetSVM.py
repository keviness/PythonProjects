import numpy as np 
import pandas as pd
import sys
from matplotlib import pyplot as plt 

#from matplotlib import style
#style.use("ggplot")
from sklearn import svm

i=0
for arg in sys.argv:
    print('\n arg[', i ,']= ',arg)
    i = i+1

#===== SVM Function (Begin)
#Sumary: Support Vector Machine (SVM) Algorithm
#Parameters:
#    X: Array of Traning Set (datatype:Array [[.,.,.],[.,.,.],......,[.,.,.]])
#    y: Array of Template Set (datatype:Array [.,.,.,  .... ])
#    P: Array of Pattern Set (datatype:Array [[.,.,.],[.,.,.],......,[.,.,.]])
def getsvm(X,y,P):
    #print('\nX=\n',X,'\ny\n=',y,'\nP=\n',P)
    #----- Train:
    clf = svm.SVC(kernel='linear', C = 1.0)
    clf.fit(X,y); #print(\nclf=\n'',clf)
    
    #----- Predict:
    mrP=P.shape[0]; mcP=P.shape[1] #mrP: Max Rows of P; mcP: Max Colomn of P
    for i in range(mrP): 
        #print('\nP[i]=\n',P[i],'\nmrP=\n',mrP,'\nmcP=\n',mcP)
        iP=P[i].reshape(1,mcP) #P[i]: Array of Pattern Set (datatype:Array [.,.,.]) needs to reshape to SVM predict-format of (datatype:Array [[.,.,.]])
        iR=clf.predict(iP) #iP: Array of Pattern Set (datatype:Array [[.,.,.]])

        if i == 0: R=iR
        else: R = np.hstack((R,iR)) # Merge each result (iR) to R (Starat) 
    return R
#===== SVM Function (End)

#===== Read Xlsx file and its' Sheets (Begin)
#----- Path and File of Excel as well as Specifying Sheets (Begin)
pfn = sys.argv[1] #or pfn='filename.xlsx' or pfn = 'C:/Users/02ehr/Documents/******.xlsx'
xGdaSet = 'GdaSet'
xTrainSet = 'TrainSet'
xPtnSet = 'PtnSet'
xTmpltSet = 'TmpltSet'

#----- Reading Multiple Excel Sheets (Begin)
with pd.ExcelFile(pfn) as xlsBook: #with excelreader.ParseExcelXMLFile(pfn) as xmlBook:
    xGdaSet_da = pd.read_excel(xlsBook, xGdaSet) # from xlsBook, read specific sheet
    xTrainSet_da = pd.read_excel(xlsBook, xTrainSet)
    xPtnSet_da = pd.read_excel(xlsBook, xPtnSet)
    xTmpltSet_da = pd.read_excel(xlsBook, xTmpltSet)
    print('\n xGdaSet_da= \n',xGdaSet_da)
#----- Reading Multiple Excel Sheets (End)
#===== Read Xlsx file and its' Sheets (End)

#===== Data Machine Learning (ML) on Herbs with SVM Pattern Recognition (PR) (Begin)
#-- 1.处理Train Set训练集X_Train (Begin) ----
#-- 1.1.界定总的数据集Gdaset_0全部行列(全集)，并从Xlsx的数据类型取数后转为numpy的array类型
Gdaset = np.array(xGdaSet_da[:][:])
print('\n Gdaset= \n',Gdaset)

#-- 1.2.界定训练集的行和列的起止范围(含非运算元素，如'中药名称')
TrainSet = np.array(xTrainSet_da[:][:])
SttTrainR=0; EndTrainR=TrainSet.shape[0]
X_Train = TrainSet[SttTrainR:EndTrainR,3:]
print('\n TrainSet= \n',TrainSet)
print('\n X_Train= \n',X_Train)
#-- 处理Train Set训练集X_Train (End) -- 

#-- 2.处理模式/样本/测试/试验/效验集(Begin) -- 
#指定一个需要计算/判别的中药,作为测试集（或在此也作为）效验集的样本（Sample，或模式Pattern）,(并酌情是否需要预先作'*.T'运算)
# 注意范围：[Start-->End),右边界为开区间
PtnSet = np.array(xPtnSet_da[:][:])
SttPtnR=0; EndPtnR=PtnSet.shape[0]
p_PtnName = PtnSet[SttPtnR:EndPtnR,0:1]
p_Ptn = PtnSet[SttPtnR:EndPtnR,3:]
print('\n PtnSet= \n',PtnSet)
print('\n p_Ptn= \n',p_Ptn)
#-- 处理模式/样本/试验/效验集(End) -- 


#-- 3.处理Template Set模板集y_Tmpl (Begin) -- 
TmpltSet = np.array(xTmpltSet_da[:][:]);
SttTmpltR=0; EndTmpltR=TmpltSet.shape[0]
y_Tmplt = np.array(TmpltSet[SttTmpltR:EndTmpltR,0:1],dtype='str').reshape(-1,)
print('\n TmpltSet= \n',TmpltSet)
print('\n y_Tmplt= \n',y_Tmplt)
#-- 处理Template Set训练集y_Tmpl (End) -- 

#-- 4.采用机器学习进行PR模式识别处理 (Begin) -- 
#调用SVM支持向量机，一种模式识别方法/函数,对输入变量(训练集,模板集,模式集)进行处理并返回结果
svmResultPR=getsvm(X_Train,y_Tmplt,p_Ptn)
print('\nsvmResultPR=\n',svmResultPR)
print('\n Memo(备注): p_PtnName= ',p_PtnName.reshape(-1,))
print('\n PtnSet= \n',PtnSet)
#----- 采用机器学习的进行模式识别处理 (End) ----- 
#===== Data Machine Learning (ML) on Herbs with SVM Pattern Recognition (PR) (End)

