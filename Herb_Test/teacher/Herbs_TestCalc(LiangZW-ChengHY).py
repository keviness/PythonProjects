import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt 

#from matplotlib import style
#style.use("ggplot")
from sklearn import svm

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
pfn = '量表-6.28.xlsx' #pfn = 'C:/Users/02ehr/Documents/量表-6.28.xlsx'
sht1 = 'Sheet1'
#----- Reading Multiple Excel Sheets (Begin)
with pd.ExcelFile(pfn) as xlsBook:
    sht1_da = pd.read_excel(xlsBook, sht1) # from xlsBook, read sht1 to sht1_da
    print('\nsht1_da=\n',sht1_da)
#----- Reading Multiple Excel Sheets (End)
#===== Read Xlsx file and its' Sheets (End)

#===== Data Machine Learning (ML) on Herbs with SVM Pattern Recognition (PR) (Begin)
#----- 处理Train Set训练集X_Train (Begin) ----- 

#1.界定总的数据集Gdaset_0全部行列(全集)，并从Xlsx的数据类型取数后转为numpy的array类型
Gdaset_0 = np.array(sht1_da[:][:]); print('\nGdaset_0=\n',Gdaset_0)
#重整理Gdaset: 指定纳入的行及其列(变量)并重排序
Rows_1 = Gdaset_0[0:10, :]
Rows_2 = Gdaset_0[11:26, :]

Gdaset_1 = np.vstack((Rows_1, Rows_2))
print('\nGdaset_1=\n',Gdaset_1)

Cols_1 = Gdaset_1[:, 0:6]
Cols_2 = Gdaset_1[:, 7:8]
Cols_3 = Gdaset_1[:, 9:13]
Gdaset = np.hstack((Cols_1, Cols_2, Cols_3))
print('\nGdaset=\n',Gdaset)

#2.界定训练集的行和列的起止范围(含非运算元素，如'中药名称')
SttTrainR=0; EndTrainR=18 #注意：以python规则，指定范围内不含尾数[SttTrainR-->EndTrainR)
SttTrainC=2; EndTrainC=13 #注意：以python规则，指定范围内不含尾数[SttTrainC-->EndTrainC)
print('\nSttTrainC=',SttTrainC,' EndTrainC=',EndTrainC)
#仅获取1列(第零列)的多行，以获取'中药名称'供打印显示。预期结果，如上述名称
TrainSet = Gdaset[SttTrainR:EndTrainR,0]
print('\nTrainSet=\n',TrainSet) #此处仅获取1列('中药名称')的多行。行序号为：[0,1,2,3,4,5]
#获取不含'中药名称'列的多行，只获取数据的行(StartTrain:EndTrain)列(SttTrainC:EndTrainC)，供作为训练集
X_Train = Gdaset[SttTrainR:EndTrainR,SttTrainC:EndTrainC]; print('\nX_Train=\n',X_Train) #X获赋值以后，行序号为：[0,1,2,3,4,5,6]
#----- 处理Train Set训练集X_Train (End) ----- 

#----- 处理Template Set模板集y_Tmpl (Begin) ----- 
#$1.Unsupervised Mode: 以自身作模板,则可：从Gdaset的'中文名称'(第0)列取多行(StartTrain:EndTrain)的值(亦即训练集的各个总集合)，形成1维数组，用作模板
y_Tmpl = Gdaset[SttTrainR:EndTrainR,0]; print('\ny_Tmpl=\n',y_Tmpl) #1维数组：['桂枝','紫苏叶',......] #[0,1,2,3,4,5,6] 

#$2a.Supervised Mode: 以人工判断的先验定论作模板：构建1维数组(其元素总个数等于训练集总个数)，用作模板
#y_Tmpl = np.array(['升','升','升','升','升','降','降']); print('\ny_Tmpl=\n',y_Tmpl) 
#$2b.Supervised Mode: 以人工判断的先验定论(降/平/升,第2列的列序号为1)作模板：构建1维数组(其元素总个数等于训练集总个数)，用作模板
#y_Tmpl = np.array(Gdaset[SttTrainR:EndTrainR,1],dtype='str'); print('\ny_Tmpl=\n',y_Tmpl)

#$3.Supervised Mode: 以人工判断的先验定论(寒凉/平/温热,第3列的列序号为2)作模板：构建1维数组(其元素总个数等于训练集总个数)，用作模板
#y_Tmpl = np.array(Gdaset[SttTrainR:EndTrainR,2],dtype='str'); print('\ny_Tmpl=\n',y_Tmpl)
#----- 处理Template Set训练集y_Tmpl (End) ----- 

#----- 处理模式/样本/测试/试验/效验集(Begin) ----- 
#指定一个需要计算/判别的中药,作为测试集（或在此也作为）效验集的样本（Sample，或模式Pattern）,(并酌情是否需要预先作'*.T'运算)
# 注意范围：[Start-->End),右边界为开区间
rng1=np.array(range(18,24));rng2=np.array(range(0,1));rng3=np.array(range(7,8));
p_ExamName = np.vstack((Gdaset[rng1,0:1],Gdaset[rng2,0:1],Gdaset[rng3,0:1]))
p_Exam = np.vstack((Gdaset[rng1,SttTrainC:EndTrainC],Gdaset[rng2,SttTrainC:EndTrainC],Gdaset[rng3,SttTrainC:EndTrainC]))
print('\n rng1=',rng1, '\n rng2=',rng2, '\n rng3=',rng3); print('\n p_ExamName=\n',p_ExamName); print('\np_Exam=\n',p_Exam)
#----- 处理模式/样本/试验/效验集(End) ----- 

#----- 采用机器学习的进行PR模式识别处理 (Begin) ----- 
#调用SVM支持向量机，一种模式识别方法/函数,对输入变量(训练集,模板集,模式集)进行处理并返回结果
svmResultPR=getsvm(X_Train,y_Tmpl,p_Exam)
print('\nsvmResultPR=\n',svmResultPR)
#----- 采用机器学习的进行模式识别处理 (End) ----- 
#===== Data Machine Learning (ML) on Herbs with SVM Pattern Recognition (PR) (End)
