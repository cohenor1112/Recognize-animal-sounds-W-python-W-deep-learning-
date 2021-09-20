import pyaudio
import wave

import os

# SAVE_RECORDS_TMP_PATH = "tmp_recorded_audio/"
# RECORD_TMP_NAME = "tmp_recorded_audio"

SAVE_RECORDS_TMP_PATH = "tmp_recorded_audio"
RECORD_TMP_NAME = "tmp_recorded_audio"

#some DEFINES:
RATE = 44100  #sr                               #SR_OF_DATASET = 44100(MAIN)/16000
FORMAT = pyaudio.paInt16                        #TODO : UNDERSTAND BETTER WHY.
GET_SAMPLE_SIZE_FORMAT = 2                      #NOTE : this value refer to FORMAT = pyaudio.paInt16 .
CHANNELS = 1

# Reading input sound signal using Python - https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python
def audio_from_mic_5_sec(save_record_path,recorded_audio_name):
    '''
    Reading 5 sec input sound signal . 
    
    return nothing , but save a .wav file of the sound in folder = save_record_path in name = recorded_audio_name.
    '''

    print("Reading 5 sec input sound signal.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    #some DEFINES:
    CHUNK = 1024  #(CHUNK_IN_SEC = CHUNK/RATE)

    RECORD_SECONDS = 5

    #creating object p = pyaudio object.
    p = pyaudio.PyAudio()

    #start recording
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    #audio buffer in frames
    frames = []

    #reading and loading to audio_buffer (frames) the data of every chunk (concatenated)
    total_num_of_chunks = int(RATE / CHUNK * RECORD_SECONDS) #TODO: UNDERSTAND WHY NOT: total_num_of_chunks = RECORD_SECONDS*SR/CHUNK
    for i in range(0, total_num_of_chunks):
        data = stream.read(CHUNK)
        frames.append(data)
    #now recording is stopped

    print("* done recording")

    #print("p.get_sample_size(FORMAT) = {}".format(p.get_sample_size(FORMAT)))

    save_recorded_audio(frames,save_record_path,recorded_audio_name)

    #stop and close streaming audio signal from mic , and terminate object p
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Done reading 5 sec input sound signal.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

    #return frames    


def save_recorded_audio(audio_buffer_frames,save_records_path,recorded_audio_name):
    '''
    Save audio_buffer_frames as .wav file with name = recorded_audio_name , in folder = save_records_path
    '''

    print("Save audio_buffer_frames as .wav file.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    #make sure save_records_path folder is exist
    save_records_full_path = os.path.join(os.getcwd() ,save_records_path)
    if not os.path.isdir(save_records_full_path):
        os.mkdir(save_records_full_path)

    FILE_FULL_NAME=os.path.join(save_records_full_path,recorded_audio_name)+'.wav'
    
    wf = wave.open(FILE_FULL_NAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(GET_SAMPLE_SIZE_FORMAT)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_buffer_frames))
    wf.close()

    print("Done save audio_buffer_frames as .wav file.") #NOTE:PRINT FOR DEBUGGING , DELETE!


# if __name__=="__main__":

#     import extract_features

#     AUDIO_FILE_NAME = "audio_from_mic_5_sec"

#     EXTRACT_FROM_WAV_FILE = False
#     EXTRACT_FROM_MIC = True

#     audio_buffer_frames = audio_from_mic_5_sec()
#     features = extract_features.extract_features(audio_buffer_frames,EXTRACT_FROM_WAV_FILE,EXTRACT_FROM_MIC)
    
#     save_recorded_audio(audio_buffer_frames,AUDIO_FILE_NAME)