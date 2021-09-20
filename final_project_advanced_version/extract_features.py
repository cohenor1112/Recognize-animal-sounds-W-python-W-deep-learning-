import librosa
import numpy as np

#For understand better search librosa documentation (and NumPy documentation).
#For understand better about sr -> https://librosa.org/blog/2019/07/17/resample-on-load/
#TODO: understand why i chose this 4 types of features , the number of the features ,and parameters(or default parmeters) of any feature. 


def extract_features_from_1wav_file(file_name):
    """
    Extracts 4 types of chromatographic features from *1* .wav file . 
    including: MFCC's(40), Chroma_stft(12), Melspectrogram(128), Spectral_contrast(7).
    TOTAL NUMBER OF FEATURES = 187 
    
    Return numpy array of features.
    """

    #print("Extract features from 1 .wav file.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    features = []
    
    #Load an audio file as a floating point time series.
    #Audio will be automatically resampled to the given rate (default sr=22050)
    #audio_data is np.ndarray [shape=(n,) or (2, n)] #TODO:understand better
    #sample_rate is sampling rate of audio_data (default sr=22050)
    audio_data, sample_rate = librosa.load(file_name)
    #stft is a Complex-valued matrix of short-term Fourier transform coefficients.
    #stft is np.ndarray [shape=(1 + n_fft/2, n_frames), dtype=dtype] #TODO:understand better
    #then with np.abs stft turned to the magnitude of stft
    stft = np.abs(librosa.stft(audio_data))
    
    #mfcc is Mel-Frequency Cepstral Coefficients
    #mfcc is np.ndarray [shape=(n_mfcc, t)]
    #mfcc then transposed NOTE: i think because the rows need to be t , then in any row t' in t will be the features
    #mfcc then turned mean along the specify axis 
    mfcc = np.mean(librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40).T,axis=0)
    features.extend(mfcc)
    
    #chroma is a chroma filter bank matrix.This creates a linear transformation matrix to project FFT bins onto chroma bins.
    #chroma is np.ndarray [shape=(n_chroma, 1 + n_fft / 2)] #TODO:understand better
    #chroma then transposed NOTE : i think because need to fit the rows in any feature.
    #chroma then turned mean along the specify axis 
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    features.extend(chroma)
    
    #mel is a Mel filter-bank matrix.This produces a linear transformation matrix to project FFT bins onto Mel-frequency bins
    #mel is np.ndarray [shape=(n_mels, 1 + n_fft/2)] #TODO:understand better
    #mel then transposed NOTE: i think because need to fit the rows in any features.
    #mel then turned mean along the specify axis 
    mel = np.mean(librosa.feature.melspectrogram(audio_data, sr=sample_rate).T,axis=0)
    features.extend(mel)
    
    #contrast is spectral contrast
    #contrast is np.ndarray [shape=(n_bands + 1, t)] #TODO:understand better
    #contrast then transposed NOTE: i think because the rows need to be t , then in any row t' in t will be the features
    #contrast then turned mean along the specify axis 
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    features.extend(contrast)

    #print("Done extract features from 1 .wav file.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

    #return a numpy array of features.
    return np.array(features)