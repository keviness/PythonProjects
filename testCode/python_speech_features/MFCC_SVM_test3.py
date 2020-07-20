import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from python_speech_features import logfbank
from sklearn import svm
import tkinter
from tkinter import filedialog, messagebox

#-----------音频源数据处理-------------------
def get_MFCC_each_seconds(path):
    (samplerate, sig) = wavfile.read(path)
    #声音文件采样频率：
    print("samplerate:", samplerate)
    time = sig.shape[0]//samplerate
    #声音时长（取整数时间）：
    print("time:", time)
    endIndex = time * samplerate
    #对声音源数据进行按秒分离，生成一个二维数组
    sig_split_array = np.vsplit(sig[0:endIndex], time)
    #遍历源数据，向子数组首行加入一个数组[起始点，终止点]
    for i in range(len(sig_split_array)): 
        sig_split_array[i] = np.insert(sig_split_array[i], 0, [i, i+1], axis=0)
    
    #遍历源数据的二维数组，抽取每一秒的声音源数据，获取MFCC特征数据
    mfcc_result_list = []
    for ele in sig_split_array:
        #获取特征值后，平展为一维数组
        mfcc_feat = mfcc(ele[1:], samplerate).reshape(-1,)
        #将首行的起始点和终止点放入一个数组中
        mfcc_result_list.append([ele[0], mfcc_feat])
    mfcc_result_list = np.array(mfcc_result_list)
    #返回数组：
    #[[起始点，终止点，特征数组],
    #.......
    #[起始点，终止点，特征数组]]
    return mfcc_result_list
    
#---------------匹配函数--------------------
def getsvm(mfcc_data, index, sample):
    clf = svm.SVC(kernel='linear', C = 1.0)
    clf.fit(mfcc_data, index)
    result = clf.predict(sample)
    return result

#---------------处理甲、乙、丙音频数据函数------------
def handle_MFCC_data(path_array):
    #获取甲、乙、丙音频特征数据，每一个音频数据选取其中一秒
    mfcc_feat_first = get_MFCC_each_seconds(path_array[0])[0][1]
    #将音频特征数据转为二维数组
    mfcc_feat_first = np.array([mfcc_feat_first])
    path_array = path_array[1:]
    for i in range (len(path_array)):
        mfcc_feat_n = get_MFCC_each_seconds(path_array[i])[0][1]
        mfcc_feat_n = np.array([mfcc_feat_n])
        #获取音频特征数据，将甲、乙、丙选取的一秒特征数据数组进行堆叠
        mfcc_feat_first = np.vstack((mfcc_feat_first, mfcc_feat_n))
    return mfcc_feat_first

#--------------------匹配函数------------------
def test_sample_sound(path_array, sample_path):
    #处理训练声音特征数据
    mfcc_result = handle_MFCC_data(path_array)

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
#-----------------获取音频文件路径--------------------
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

#----------------主函数----------------
def main():
    #导入音频文件
    while True:
        #导入甲、乙、丙音频文件路径
        print("chose the format sound file(甲、乙、丙):")
        path_array = get_sound_file_paths()
        #导入待测音频文件路径
        print("Now chose the sample sound file（测速音频文件）:")
        sample_path_array = get_sound_file_paths()
        if len(path_array)!=0 or len(sample_path_array)!=0:
            break
    #若有多个样品，遍历样品音频路径进行测试
    for element in sample_path_array:
        test_sample_sound(path_array, element)

if __name__ == "__main__":
    main()