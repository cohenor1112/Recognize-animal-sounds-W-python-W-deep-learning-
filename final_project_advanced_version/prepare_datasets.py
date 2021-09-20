import os
import pandas as pd
import numpy as np

import extract_features

DATASETS_PATH = "Datasets"
PREPARED_DATASETS_PATH = "Prepared_Datasets"
ESC50_DATASET_NAME = "Environmental_Sound_Classification_50"
RECORDED_AUDIOS_DATASET_NAME = "Recorded_audios"

def prepare_datasets(Environmental_Sound_Classification_50,
                     Recorded_dataset,
                     save_prepared_datasets_f=True): 
    '''
    Works on raw datasets: Environmental_Sound_Classification_50 or/and Recorded_dataset.
    extracts features from every .wav file *that contain animal sound*,
    and makes prepared dataset for machine learning model.  

    Returns np.array_all_data, np.array_all_labels, np_arr_numeric_labels, animals of the whole datasets.

    The first is a numpy array contains numpy arrays of each audio's numerical features - extract_features()
    The second numpy array contains *STRING* labeles.
    The third numpy array contains *numerical* labeles.
    The arrays indexes align up between the three arrays. np.array_all_data[idx] is classified as np.array_all_labels[idx] and np_arr_numeric_labels[idx] )
    animals is a list of animals classes as strings , his role is to match a between animal type to its numerical number. every animal type has the number that represent it .eventually animal type = animals[arg.max(y_predict)]
    
    if save_prepared_datasets_f = True so the 4 parameters will be saved in prepared_dataset folder , and np.array_all_data, np.array_all_labels, animals of each dataset in its folder.
    '''

    print("Prepare datasets.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    all_data1 = []
    all_labels1 = []
    animals1 = []

    all_data2 = []
    all_labels2 = []
    animals2 = []

    if Environmental_Sound_Classification_50:

        #extracts features from every .wav file *that contain animal sound* , and fills all_data , all_labels.  
        animals1=["dog","chirping_birds","crow","sheep","frog","cow","insects","hen","pig","rooster","cat","crickets"]
        print("Loading Environmental_Sound_Classification_50 dataset.")
        DATASETS_FULL_PATH = os.path.join(os.getcwd(),DATASETS_PATH)
        ESC50_DATASET_FULL_PATH = os.path.join(DATASETS_FULL_PATH,ESC50_DATASET_NAME)
        esc50_csv = os.path.join(ESC50_DATASET_FULL_PATH,"esc50.csv")
        metadata = pd.read_csv(esc50_csv)
        for root, dirs, files in os.walk(ESC50_DATASET_FULL_PATH):
            for file in files:
                if file.endswith('.wav'):
                    fname = os.path.join(root, file)
                    label = metadata[metadata.filename == file]["category"].tolist()[0]
                    if label in animals1:
                        #for debugging :
                        if(len(all_data1) % 100 == 0 and len(all_data1)!=0):
                            print("{} animals wav file extracted.".format(str(len(all_data1))))
                        features = extract_features.extract_features_from_1wav_file(fname)
                        all_data1.append(features)
                        all_labels1.append(label)

        np_arr_all_data1 = np.array(all_data1)
        np_arr_all_labels1 = np.array(all_labels1)
        
        print("Environmental_Sound_Classification_50 dataset extraction completed.")
        print("{} animals wav file extracted.".format(str(len(all_data1))))

        #saves the 3 first parameters in prepared_dataset folder
        if save_prepared_datasets_f:
            save_prepared_dataset_1 (PREPARED_DATASETS_PATH, ESC50_DATASET_NAME, np_arr_all_data1, np_arr_all_labels1, animals1)

    if Recorded_dataset:

        print("Loading Recorded_audios dataset.")
        DATASETS_FULL_PATH = os.path.join(os.getcwd(), DATASETS_PATH)
        RECORDED_AUDIOS_DATASET_FULL_PATH = os.path.join(DATASETS_FULL_PATH, RECORDED_AUDIOS_DATASET_NAME)
        if not os.path.isdir(RECORDED_AUDIOS_DATASET_FULL_PATH) :
            os.mkdir(RECORDED_AUDIOS_DATASET_FULL_PATH)
        # if not os.listdir (RECORDED_AUDIOS_DATASET_FULL_PATH) :
        #     print("Recorded_audios dataset is empty.\n")
        #     empty_list = []
        #     np_arr_empty_list = np.array(empty_list)
        #     return np_arr_empty_list, np_arr_empty_list, np_arr_empty_list, empty_list
        for root, dirs, files in os.walk(RECORDED_AUDIOS_DATASET_FULL_PATH):
            for file in files:
                if file.endswith('.wav'):
                    fname = os.path.join(root, file)
                    #for debugging :
                    if(len(all_data2) % 100 == 0 and len(all_data2)!=0):
                        print("{} animals wav file extracted.".format(str(len(all_data2))))
                    features = extract_features.extract_features_from_1wav_file(fname)
                    all_data2.append(features)
                    splitted_name = file.split('-')
                    splitted_name.pop(-1)
                    label = '.'.join(splitted_name)
                    all_labels2.append(label)
        
        np_arr_all_data2 = np.array(all_data2)
        np_arr_all_labels2 = np.array(all_labels2)
        animals2 = list(set(all_labels2))

        print("Recorded_audio dataset extraction completed.")
        print("{} animals wav file extracted.".format(str(len(all_data2))))

        #saves the 3 parameters in prepared_dataset folder
        if save_prepared_datasets_f:
            save_prepared_dataset_1 (PREPARED_DATASETS_PATH, RECORDED_AUDIOS_DATASET_NAME, np_arr_all_data2, np_arr_all_labels2, animals2)

    all_data = all_data1 + all_data2
    all_labels = all_labels1 + all_labels2
    animals = animals1+animals2
    animals = list(set(animals))
    all_numeric_labels = [animals.index(label) for label in all_labels] # labels by index

    np_arr_all_data = np.array(all_data)
    np_arr_all_labels = np.array(all_labels)
    np_arr_all_numeric_labels = np.array(all_numeric_labels)
        
    print("Done prepare datasets.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

    return np_arr_all_data, np_arr_all_labels, np_arr_all_numeric_labels, animals


#saves the 3 parameters in prepared_dataset folder
#its saves animals as a string of list in .txt file
def save_prepared_dataset_1(prepared_dataset_path, dataset_name, np_arr_all_data, np_arr_all_lables, animals):
    
    print("Save prepared dataset.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    PREPARED_DATASETS_FULL_PATH = os.path.join(os.getcwd(), prepared_dataset_path)
    is_path = os.path.isdir(PREPARED_DATASETS_FULL_PATH)
    if not is_path:
        os.mkdir(PREPARED_DATASETS_FULL_PATH)
        
    PREPARED_DATASET_FULL_PATH = os.path.join(PREPARED_DATASETS_FULL_PATH, dataset_name)
    is_path = os.path.isdir(PREPARED_DATASET_FULL_PATH)
    if not is_path:
        os.mkdir(PREPARED_DATASET_FULL_PATH)
    
    np.save(PREPARED_DATASET_FULL_PATH+"/all_data_"+dataset_name, np_arr_all_data)
    np.save(PREPARED_DATASET_FULL_PATH+"/all_labels_"+dataset_name, np_arr_all_lables)
    with open(PREPARED_DATASET_FULL_PATH+"/animals_"+dataset_name+".txt", "w") as output:
        output.write(str(animals))
    print("{} was prepared and saved in {}".format(dataset_name,prepared_dataset_path))

    print("Done save prepared dataset.") #NOTE:PRINT FOR DEBUGGING , DELETE!  

if __name__ == "__main__":
    all_data, all_labels,np_arr_numeric_labels, animals = prepare_datasets(Environmental_Sound_Classification_50 = True,
                                                                           Recorded_dataset = True,
                                                                           save_prepared_datasets_f = True)
    print (animals)
    # print (animals[0])