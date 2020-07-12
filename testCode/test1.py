import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from python_speech_features import logfbank
from sklearn import svm
import tkinter
from tkinter import filedialog, messagebox


def get_MFCC_each_seconds(path):
    (samplerate, sig) = wavfile.read(path)
    print("samplerate:", samplerate)
    #print("time:", sig.shape[0]//samplerate)
    #print("sig:", sig)
    print("sig shape:", sig.shape)

    time = sig.shape[0]//samplerate
    print("split-time:", time)
    endIndex = time * samplerate
    #print("sig[0:endIndex]:", sig[0:endIndex])
    sig_split_array = np.vsplit(sig[0:endIndex], time)
    #print("sig_split_array1:", sig_split_array)

    for i in range(len(sig_split_array)):
        #print("sig-split-shape".center(30, "*"))
        #print(sig_split_array[i].shape)
        sig_split_array[i] = np.insert(sig_split_array[i], 0, [i, i+1], axis=0)
    #print("sig_split_array2:", sig_split_array)

    mfcc_result_list = []
    for ele in sig_split_array:
        mfcc_feat = mfcc(ele[1:], samplerate)
        #print("mfcc_feat:", mfcc_feat)
        #print("mfcc-feat".center(30, "*"))
        #print("mfcc_feat.shape:", mfcc_feat.shape)
        mfcc_result_list.append([ele[0], mfcc_feat])
    mfcc_result_list = np.array(mfcc_result_list)
    print("mfcc_result:", mfcc_result_list)
    print("mfcc_result shape:", mfcc_result_list.shape)

    '''
    lst1 = []
    lst2 = []
    for i in range(sig.shape[0]):
        lst1.append(sig[i])
        if (((i+1)%samplerate) == 0):
            time_index = int((i+1)/samplerate)
            print("run-time:",time_index)
            #print("i:",i)
            #print("select_item:", sig[i])
            lst1.insert(0, [time_index-1, time_index])
            lst2.append(lst1)
            lst1 = []
            
    for ele in lst2:
        ele = np.array(ele)
        print("ele:", ele)
        print("ele shape:", ele.shape)

    mfcc_feat = mfcc(sig[0:3], samplerate)
    fbank_feat = logfbank(sig, samplerate)
    print("mfcc_feat:", mfcc_feat)
    print("mfcc_feat shape:", mfcc_feat.shape)
    left = []
    right = []
    for item in sig:
        left.append(item[0])
        right.append(item[1])
    #print(samplerate)
    print("left:".center(30, "*"))
    print(left)
    print("right:".center(30, "*"))
    print(right)
    print("sig:".center(30, "*"))
    print(sig)

    mfcc_feat = np.asarray(mfcc_feat, dtype="int64", order="C").reshape(-1, )
    rows_max = mfcc_feat.size//2
    mfcc_feat_array = mfcc_feat[0: rows_max*2]
    mfcc_feat_array = mfcc_feat_array.reshape(rows_max, 2)
    
    print("mfcc_feat_array:".center(30, "*"))
    print(mfcc_feat_array)
    wavfile.write("mccf_feat.wav", samplerate, mfcc_feat_array)

    wavfile.write('left.wav', samplerate, np.array(left))
    wavfile.write('right.wav', samplerate, np.array(right))
    wavfile.write("sound.wav", samplerate, sig)
    '''

def get_sound_file_paths():
    path_array = []
    while True:
        answer = input("Do you want to search the sound file:(y/n)")[0]
        if answer == "y":
            win = tkinter.Tk()
            win.withdraw()
            filename = filedialog.askopenfilename().replace("/", "\\")
            if filename[-4:] == ".wav":
                path_array.append(filename)
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
    for i in range(len(path_array)):
        print("get the {0} sound file: {1}".format(i+1, path_array[i]))
    
    return path_array

path_array = get_sound_file_paths()
for ele in path_array:
    get_MFCC_each_seconds(ele)