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
        mfcc_feat = mfcc(ele[1:], samplerate).reshape(-1,)
        #print("mfcc_feat:", mfcc_feat)
        #print("mfcc-feat".center(30, "*"))
        #print("mfcc_feat.shape:", mfcc_feat.shape)
        mfcc_result_list.append([ele[0], mfcc_feat])
    mfcc_result_list = np.array(mfcc_result_list)
    #print("mfcc_result:", mfcc_result_list)
    return mfcc_result_list
    

def getsvm(mfcc_data, index, sample):
    clf = svm.SVC(kernel='linear', C = 1.0)
    clf.fit(mfcc_data, index)
    result = clf.predict(sample)
    return result

def handle_MFCC_data(path_array):
    mfcc_feat_first = get_MFCC_each_seconds(path_array[0])[0][1]
    mfcc_feat_first = np.array([mfcc_feat_first])
    path_array = path_array[1:]
    for i in range (len(path_array)):
        mfcc_feat_n = get_MFCC_each_seconds(path_array[i])[0][1]
        mfcc_feat_n = np.array([mfcc_feat_n])
        mfcc_feat_first = np.vstack((mfcc_feat_first, mfcc_feat_n))
    #print("mfcc_feat_first", mfcc_feat_first)
    return mfcc_feat_first


def test_sample_sound(path_array, sample_path):
    #处理训练声音特征数据
    mfcc_result = handle_MFCC_data(path_array)
    #print(mfcc_result)
    #print(mfcc_result.shape)

    #处理待匹配声音特征数据
    match_result_array = []
    owner_result_array = []
    sample_mfcc_feat_array = get_MFCC_each_seconds(sample_path)

    for i in range(len(sample_mfcc_feat_array)):
        item = sample_mfcc_feat_array[i]
        sample = np.array([item[1]])

        index = []
        for j in range(len(path_array)):
            index.append(j+1)
        #对样品声音进行匹配
        match_result = getsvm(mfcc_result, index, sample)[0]
        match_result_array.append(match_result)
        owner_result_array.append([item[0][0], item[0][1], match_result])

        '''
        if match_result == 1:
            owner_first.append([item[0][0], item[0][1], match_result])
        if match_result == 2:
            owner_second.append([item[0][0], item[0][1], match_result])
        if match_result == 3:
            owner_third.append([item[0][0], item[0][1], match_result])
        '''
    owner_result_array = np.array(owner_result_array)
    print("match_result_array:", match_result_array)
    print("owner_result_array:", owner_result_array)
    '''
    first_ndarray = np.array(owner_first)
    second_ndarray = np.array(owner_second)
    third_ndarray = np.array(owner_third)
    result_tuple = (first_ndarray, second_ndarray, third_ndarray)
    print("result_tuple:", result_tuple)
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

def main():
    while True:
        print("chose the sound format file:")
        path_array = get_sound_file_paths()
        print("Now chose the sample sound file:")
        sample_path_array = get_sound_file_paths()
        if len(path_array)!=0 or len(sample_path_array)!=0:
            break

    for element in sample_path_array:
        test_sample_sound(path_array, element)

if __name__ == "__main__":
    main()