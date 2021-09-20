#working on dataset :
import load_prepared_datasets
import prepare_datasets
import divide_dataset
#-------------------------------
#working on the model :
import build_and_compile_model
import fit_save_or_load_fitted_model
#-------------------------------
#analyzing model :
import model_evaluation
import analyze_model
#-------------------------------
#get audio :
import audio_from_mic
#-------------------------------
#play sound : 
from playsound import playsound
#-------------------------------
#extract features from audio and predict (and get other information) from features:
import extract_features
import predict
#-------------------------------
#get animal information :
import animal_info
#-------------------------------
#save audio sound from mic :
import os
import shutil
#-------------------------------
#import os


if __name__=="__main__":

#------------------------------------------------------
    #working on dataset:

    #getting np_arr_all_data ,np_arr_all_labels ,np_arr_all_numeric_labels, animals.
    #some DEFINES:
    LOAD_PREPARED_DATASETS_F = True
    PREPARE_RAW_DATASETS_F = False

    PREPARED_DATASET_PATH = "Prepared_Datasets"
    ENVIRONMENTAL_SOUND_CLASSIFICATION_50 = True
    RECORDED_AUDIO = True
    SAVE_PREPARED_DATASET = True

    if LOAD_PREPARED_DATASETS_F == True:
        np_arr_all_data ,np_arr_all_labels ,np_arr_all_numeric_labels, animals = load_prepared_datasets.load_prepared_datasets(ENVIRONMENTAL_SOUND_CLASSIFICATION_50,
                                                                                                                               RECORDED_AUDIO,
                                                                                                                               PREPARED_DATASET_PATH)
    if PREPARE_RAW_DATASETS_F == True:
        np_arr_all_data ,np_arr_all_labels ,np_arr_all_numeric_labels, animals = prepare_datasets.prepare_datasets(ENVIRONMENTAL_SOUND_CLASSIFICATION_50,
                                                                                                                   RECORDED_AUDIO,
                                                                                                                   SAVE_PREPARED_DATASET)
    
    #divide dataset to x_train ,x_test ,y_train ,y_test:
    #some DEFINES:
    TEST_SIZE = 0.2

    x_train, x_test, y_train, y_test = divide_dataset.divide_dataset(np_arr_all_data,np_arr_all_numeric_labels,test_size=TEST_SIZE)

#------------------------------------------------------------------------
    #working on the model :
    
    #build and compile model
    #some DEFINES:
    INPUT_DIM = x_train.shape[1]
    N_CLASSES = len(animals)

    model = build_and_compile_model.build_and_compile_model(INPUT_DIM,N_CLASSES)

    #fit / fit and save / load fitted model
    #some DEFINES:
    # LOADֹֹ_MODEL = True
    # TRAIN_MODEL = True

    LOAD_MODEL_FILE_NAME = False # False / "Animal_classifier_model"
    SAVE_MODEL_FILE_IN_NAME = "Animal_classifier_model" # False / "Animal_classifier_model"

    model ,history = fit_save_or_load_fitted_model.fit_save_or_load_fitted_model(model,LOAD_MODEL_FILE_NAME,SAVE_MODEL_FILE_IN_NAME,x_train, y_train,x_test, y_test)
    
    print('Model summary:')
    model.summary()
    print('\n')

#-----------------------------------------------------------------------------
    #analyzing model :
    
    #model_evaluation on test set:
    model_evaluation.model_evaluation (model, x_test, y_test)
    
    #testing (analyzing) model :
    analyze_model.model_analysys(model ,x_test ,y_test, history, animals)

#------------------------------------------------------------------------------
    #get audio from .wav file or directly from mic

    #some DEFINES:
    GET_AUDIO_FROM_WAV_FILE = True
    GET_AUDIO_FROM_MIC = False

    #get audio from .wav file:
    if GET_AUDIO_FROM_WAV_FILE == True:
        #some DEFINES:
        ANIMALS_SOUNDS_FOLDER_PATH = "animals_sounds/"
        ANIMAL_SOUND_FILE_NAME = 'dog.wav'
        ANIMAL_SOUND = ANIMALS_SOUNDS_FOLDER_PATH + ANIMAL_SOUND_FILE_NAME

        fname = ANIMAL_SOUND
    
    #get audio directly from mic:
    elif GET_AUDIO_FROM_MIC == True:
        #some DEFINES:
        SAVE_RECORDS_TMP_PATH = "tmp_recorded_audio/"
        RECORD_TMP_NAME = "tmp_recorded_audio"

        audio_from_mic.audio_from_mic_5_sec(SAVE_RECORDS_TMP_PATH,RECORD_TMP_NAME)

        fname = SAVE_RECORDS_TMP_PATH + RECORD_TMP_NAME + '.wav'

#------------------------------------------------------------------------------
    #play sound

    #some DEFINE:
    PLAY_SOUND = True

    if PLAY_SOUND == True:
        playsound(fname)

#------------------------------------------------------------------------------
    #extract features from audio and predict (and get other information) from features:

    #some DEFINES:
    PREDICT = True

    if PREDICT==True:
        features = extract_features.extract_features_from_1wav_file(fname)
        predicted_index , predicted_animal , probability_array_percentages = predict.predict_input_features(model , features , animals)
        predict.show_probabilities_hist(animals , probability_array_percentages)

#------------------------------------------------------------------------------
    #TODO : how to decide which animal it is?
    #decide which animal it is and get predicted_animal information:
    #some DEFINES:
    PROBABILITY_TRESHOLD = 80

    if probability_array_percentages[predicted_index] >= PROBABILITY_TRESHOLD:
        print ("The model is {}% sure that the sound heard is from a {}\n".format(probability_array_percentages[predicted_index],predicted_animal))
        #get predicted_animal information:
        #animal_info = animal_info.get_animal_info(predicted_animal)
        print (animal_info)
    else :
        print ("The model is not sure which animal it is")

#------------------------------------------------------------------------------
    #save audio sound from mic :

    # #some DEFINES:
    # SAVE_AUDIO_F = False

    # SAVE_RECORDS_PATH = "Recorded_audio/"
    # RECORD_NAME = predicted_animal

    # SRC_FILE = fname
    # DST_FILE = SAVE_RECORDS_PATH + RECORD_NAME +'.wav'

    # if SAVE_AUDIO_F == True :
    #     shutil.move(SRC_FILE,DST_FILE)
    # else:
    #     os.remove(SRC_FILE)