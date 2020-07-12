import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from matplotlib import style
style.use("ggplot")
from python_speech_features import mfcc
from python_speech_features import logfbank
from sklearn import svm

#----------------------
def getmfcc(pathfile):
    (rate,sig) = wav.read(pathfile)
    print('rate=',rate)
    print('sig=',sig)
    mfcc_feat = mfcc(sig,rate)
    fbank_feat = logfbank(sig,rate)

    #print(sig)
    #print(sig.shape)
    #print(rate)
    #print(mfcc_feat.shape)
    #print(fbank_feat.shape)
    #print(fbank_feat[1:3,:])
    return mfcc_feat



#----------------------
def getsvm(X,y,s):

    clf = svm.SVC(kernel='linear', C = 1.0)
    clf.fit(X,y)
    r=clf.predict(s)

    '''
    #
    w = clf.coef_[0]
    print(w)
    a = -w[0] / w[1]

    xx = np.linspace(0,12)
    yy = a * xx - clf.intercept_[0] / w[1]

    #built figure
    #draw line for predict function
    h0 = plt.plot(xx, yy, 'k-', label="non weighted div")
    #plot for array X
    hX = plt.scatter(X[:, 0], X[:, 1], c = y)
    print(X)
    X=X.T.reshape(6,2)
    print(X)
    hX_ = plt.scatter(X[:, 0], X[:, 1])
    #dwaw lengend
    plt.legend()
    plt.show()
    '''
    return r

#============
#a = [1, 5, 1.5, 8, 7, 9]
#b = [2, 8, 1.8, 8, 0.6, 11]
#X=np.array([a,b]).T             
#y = [0,1,0,1,0,1]

pathfile = "C:\\user2020\\PythonTest\\wav\\Z61.wav"
mfcc_feat = getmfcc(pathfile)
mfcc_feat1 = np.reshape(mfcc_feat, mfcc_feat.size) #mfcc_feat[:,0]

rs=mfcc_feat.shape[0]
cs=mfcc_feat.shape[1]

pathfile = "C:\\user2020\\PythonTest\\wav\\Z62.wav"
mfcc_feat = getmfcc(pathfile)
mfcc_feat_ = mfcc_feat[0:rs,:]
mfcc_feat2 = np.reshape(mfcc_feat_, mfcc_feat_.size)

pathfile = "C:\\user2020\\PythonTest\\wav\\Z63.wav"
mfcc_feat = getmfcc(pathfile)
mfcc_feat_ = mfcc_feat[0:rs,:]
mfcc_feat3 = np.reshape(mfcc_feat_, mfcc_feat_.size)

pathfile = "C:\\user2020\\PythonTest\\wav\\Z64.wav"
mfcc_feat = getmfcc(pathfile)
mfcc_feat_ = mfcc_feat[0:rs,:]
mfcc_feat4 = np.reshape(mfcc_feat_, mfcc_feat_.size)

pathfile = "C:\\user2020\\PythonTest\\wav\\CaoS1.wav" #"Z_11-20.wav" #"Z65.wav"
mfcc_feat = getmfcc(pathfile)
mfcc_feat_ = mfcc_feat[0:rs,:]
mfcc_feat5 = np.reshape(mfcc_feat_, mfcc_feat_.size)

pathfile = "C:\\user2020\\PythonTest\\wav\\CaoS2.wav" #"Z_41-50.wav" #"ca1lzw11025.wav"
mfcc_feat = getmfcc(pathfile)
mfcc_feat_ = mfcc_feat[0:rs+0,:]
mfcc_feat6 = np.reshape(mfcc_feat_, mfcc_feat_.size)


### Sampleing file
pathfile = "C:\\user2020\\PythonTest\\wav\\Z_11-20.wav" #"ca1lzw11025.wav"
mfcc_feat = getmfcc(pathfile)
mfcc_feat_ = mfcc_feat[0:rs+0,:]
mfcc_feat0 = np.reshape(mfcc_feat_, mfcc_feat_.size)

X=np.vstack((mfcc_feat1, mfcc_feat2, mfcc_feat3, mfcc_feat4, mfcc_feat5, mfcc_feat6))
y = [1,2,3,4,5,6]
X.shape
print(X.shape)

s = np.vstack((mfcc_feat0)).T

r=getsvm(X,y,s)
print(r)

