import numpy as np
from scipy.io import wavfile
from python_speech_features import *
from sklearn import svm
import tkinter
from tkinter import filedialog

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
    for element in sig_split_array:
        #获取特征值后，平展为一维数组
        #MFCC特征值：
        wav_feat = mfcc(element[1:], samplerate, nfft=1200)
        '''
        wav_feat = mfcc(signal, samplerate, numcep=self.numc, winlen=0.025, winstep=0.01,
                           nfilt=26, nfft=512, lowfreq=0, highfreq=None, preemph=0.97)
        signal - 需要用来计算特征的音频信号，是一个N*1的数组
        samplerate - 信号的采样率
        winlen - 分析窗口的长度，按秒计，默认0.025s(25ms)
        winstep - 连续窗口之间的步长，按秒计，默认0.01s（10ms）
        numcep - 倒频谱返回的数量，默认13
        nfilt - 滤波器组的滤波器数量，默认26
        nfft - FFT的大小，默认512
        lowfreq - 梅尔滤波器的最低边缘，单位赫兹，默认:0
        highfreq - 梅尔滤波器的最高边缘，单位赫兹，默认:采样率/2
        preemph - 应用预加重过滤器和预加重过滤器的系数，0:没有过滤器，默认0.97
        ceplifter - 将升降器应用于最终的倒谱系数。 0:没有升降机。默认值为22。
        appendEnergy - 如果是true，则将第0个倒谱系数替换为总帧能量的对数。 
        '''
        d_mfcc_feat = delta(wav_feat, 1)
        d_mfcc_feat2 = delta(wav_feat, 2)
        mfcc_feat = np.hstack((wav_feat, d_mfcc_feat, d_mfcc_feat2))
        mfcc_feat = mfcc_feat.reshape(-1,)

        #logfbank特征值：
        logfbank_feat = logfbank(element[1:], samplerate, nfft=1200)
        d_logfbank_feat = delta(logfbank_feat, 1)
        d_logfbank_feat2 = delta(logfbank_feat, 2)
        logfbank_feat_arr = np.hstack((logfbank_feat, d_logfbank_feat, d_logfbank_feat2))
        logfbank_feat_arr = logfbank_feat_arr.reshape(-1,)

        sound_feat = np.hstack((mfcc_feat, logfbank_feat_arr))
        #将首行的起始点，终止点，声音源数据和mfcc数据放入一个数组中
        mfcc_result_list.append([element[0], element[1:], sound_feat])
    mfcc_result_list = np.array(mfcc_result_list)
    #返回数组：
    #[起始点，终止点，声音源数据，特征数据],
    #.......
    #[起始点，终止点，声音源数据，特征数据]]
    return mfcc_result_list
    
#---------------匹配函数--------------------
def getsvm(mfcc_data, index, sample):
    clf = svm.SVC(kernel='rbf', C = 0.8)
    clf.fit(mfcc_data, index)
    result = clf.predict(sample)
    return result

#---------------处理甲、乙、丙音频数据函数------------
def handle_MFCC_data(path_array):
    #获取甲、乙、丙音频特征数据，每一个音频数据选取其中一秒
    mfcc_feat_first = get_MFCC_each_seconds(path_array[0])[0][2]
    #将音频特征数据转为二维数组
    mfcc_feat_first = np.array([mfcc_feat_first])
    path_array = path_array[1:]
    for i in range (len(path_array)):
        mfcc_feat_n = get_MFCC_each_seconds(path_array[i])[0][2]
        mfcc_feat_n = np.array([mfcc_feat_n])
        #获取音频特征数据，将甲、乙、丙选取的一秒特征数据数组进行堆叠
        mfcc_feat_first = np.vstack((mfcc_feat_first, mfcc_feat_n))
    return mfcc_feat_first

#--------------------匹配函数------------------
def test_sample_sound(path_array, sample_path):
    #处理训练声音特征数据
    mfcc_result = handle_MFCC_data(path_array)

    #处理待匹配声音特征数据
    owner_first = []
    owner_second = []
    owner_third = []
    match_result_array = []
    #获取待测音频特征数据数组
    sample_mfcc_feat_array = get_MFCC_each_seconds(sample_path)
    #遍历数组，选取每一秒的待测音频声音特征数据进行匹配
    for i in range(len(sample_mfcc_feat_array)):
        item = sample_mfcc_feat_array[i]
        sample = np.array([item[2]])

        index = []
        for j in range(len(path_array)):
            index.append(j+1)
        #对样品声音进行匹配，将匹配结果和声音起始点，终止点放入一个数组中
        match_result = getsvm(mfcc_result, index, sample)[0]
        match_result_array.append([item[0][0], item[0][1], match_result])
        if match_result == 1:
            owner_first.append(item[1])
        if match_result == 2:
            owner_second.append(item[1])
        if match_result == 3:
            owner_third.append(item[1])
    match_result_array = np.array(match_result_array)
    owner_first = np.array(owner_first)
    owner_second = np.array(owner_second)
    owner_third = np.array(owner_third)
    
    owner_first = vstack_ndarray(owner_first)
    owner_second = vstack_ndarray(owner_second)
    owner_third = vstack_ndarray(owner_third)
    #返回结果数组：
    #[[起始点，终止点，分类值]
    #......
    # [起始点，终止点，分类值]]
    #打印，和返回结果
    print("result_array:\n", match_result_array)
    #print("owner_first:", owner_first)
    #print("owner_second:", owner_second)
    #print("owner_third:", owner_third)
    separate_sound(owner_first, owner_second, owner_third)

def vstack_ndarray(ndarray):
    first_array = ndarray[0]
    for i in range(len(ndarray)-1):
        first_array = np.vstack((first_array, ndarray[i+1]))
    return first_array

def separate_sound(owner_first, owner_second, owner_third):
    samplerate = 44100
    
    wavfile.write('owner1.wav', samplerate, owner_first)
    wavfile.write('owner2.wav', samplerate, owner_second)
    wavfile.write('owner3.wav', samplerate, owner_third)

    print("write to new sound file successfully!")

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

#-------------------------主函数----------------------------
def main():
    #导入音频文件
    while True:
        #导入甲、乙、丙音频文件路径
        print("chose the format sound file(甲、乙、丙):")
        path_array = get_sound_file_paths()
        #导入待测音频文件路径
        print("Now chose the sample sound file（待测音频文件）:")
        sample_path_array = get_sound_file_paths()
        if len(path_array)!=0 or len(sample_path_array)!=0:
            break
    #若有多个待测音频数据，遍历待测音频数据进行测试
    for element in sample_path_array:
        test_sample_sound(path_array, element)

if __name__ == "__main__":
    main()