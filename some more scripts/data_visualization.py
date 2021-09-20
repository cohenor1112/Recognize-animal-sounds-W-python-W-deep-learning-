import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
import librosa.display
import numpy as np


def data_visualization(audio_file_path):

    audio , sr = librosa.load(audio_file_path)
    #print(type(x), type(sr))

    #ipd.Audio(audio_path)

    #display waveform
    display_waveform(audio,sr)

    #mel spectogram
    display_mel_spec(audio,sr)

    #Spectral Contrast
    desplay_spectral_contrast(audio,sr)


    #chroma
    audio_stft = np.abs(librosa.stft(audio))
    desplay_chromagram(audio_stft,sr)

    #mfcc
    display_mfcc(audio,sr)


#------------------------------------------------------

    #display waveform
def display_waveform(audio,sr):
    #%matplotlib inline
    plt.figure(figsize=(10, 4))
    librosa.display.waveplot(audio, sr=sr)

    #mel spectogram
def display_mel_spec(audio,sr):
    S = librosa.feature.melspectrogram(y=audio, sr=sr)
    plt.figure(figsize=(10, 4))
    S_dB = librosa.power_to_db(S, ref=np.max)
    print(S_dB.shape)
    librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    plt.show()

    #Spectral Contrast
def desplay_spectral_contrast(audio,sr):    
    S = np.abs(librosa.stft(audio))
    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
    print(contrast.shape)

    plt.figure(figsize=(10,4))
    librosa.display.specshow(contrast, x_axis='time')
    plt.colorbar()
    plt.ylabel('Frequency bands')
    plt.title('Spectral contrast')
    plt.tight_layout()
    plt.show()

    #chroma
def desplay_chromagram(audio_stft,sr):
    chroma = librosa.feature.chroma_stft(S=audio_stft, sr=sr)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(chroma, y_axis='chroma', x_axis='time')
    plt.colorbar()
    plt.title('Chromagram')
    plt.tight_layout()
    plt.show()

    #mfcc
def display_mfcc(audio,sr,n_mfcc=40):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfcc, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()