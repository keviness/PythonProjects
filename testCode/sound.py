import numpy as np
from scipy.io import wavfile


def splitWav( path ):
    samplerate, data = wavfile.read(path)
    left = []
    right = []
    for item in data:
        left.append(item[0])
        right.append(item[1])
    wavfile.write('left.wav', samplerate, np.array(left))
    wavfile.write('right.wav', samplerate, np.array(right))

if __name__ == '__main__':

    splitWav("./f2.wav")
