import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from python_speech_features import logfbank
from sklearn import svm
import tkinter
from tkinter import filedialog, messagebox

def getsvm(mfcc_data, index, sample):

    clf = svm.SVC(kernel='linear', C = 1.0)
    clf.fit(mfcc_data, index)
    result = clf.predict(sample)

    return result

a = np.linspace(1,12,12, dtype="int64").reshape(6,2)
print("a:", a)
index = list("123")
print("index:", index)
b = np.array([[1,2],[3,4],[5,6],[7,8]])
print("b:",b)
result = getsvm(a, index, b)
print(result)