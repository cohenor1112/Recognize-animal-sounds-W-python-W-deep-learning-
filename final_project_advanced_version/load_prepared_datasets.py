import numpy as np
import ast

import os

#from tkinter import messagebox

PREPARED_DATASETS_PATH = "Prepared_Datasets"
ESC50_DATASET_NAME = "Environmental_Sound_Classification_50"
RECORDED_AUDIOS_DATASET_NAME = "Recorded_audios"

def load_prepared_datasets(Environmental_Sound_Classification_50, Recorded_dataset, prepared_dataset_path=PREPARED_DATASETS_PATH):
    '''
    Load from every dataset (that marked at True) : np_arr_all_data, np_arr_all_labels from .npy files and animals from .txt file.

    Returns *total* np_arr_all_data , np_arr_all_labels , np_arr_all_numeric_lebels , animals.

    The first is a numpy array contains numpy arrays of each audio's numerical features - extract_features()
    The second numpy array contains *STRING* labeles.
    The third numpy array contains *numerical* labeles.
    The arrays indexes align up between the three arrays. np.array(all_data)[idx] is classified as np.array(all_labels)[idx] and np_arr_numeric_labels[idx] )
    animals is a list of animals classes as strings, his role is to match a between animal type to its numerical number. every animal type has the number that represent it .eventually animal type = animals[arg.max(y_predict)]
    '''
    
    print("Load prepared dataset.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    all_data1 = []
    np_arr_all_data1 = np.array(all_data1)
    np.reshape(np_arr_all_data1,(0,187))
    all_labels1 = []
    np_arr_all_labels1 = np.array(all_labels1)
    np.reshape(np_arr_all_labels1,(0,187))
    animals1 = []
    
    all_data2 = []
    np_arr_all_data2 = np.array(all_data2)
    np.reshape(np_arr_all_data2,(0,187))
    all_labels2 = []
    np_arr_all_labels2 = np.array(all_labels2)
    np.reshape(np_arr_all_labels2,(0,187))
    animals2 = []
    
    if Environmental_Sound_Classification_50 == True and Recorded_dataset == False :

        np_arr_all_data1, np_arr_all_labels1, animals1 = load_prepared_dataset(ESC50_DATASET_NAME)
        np_arr_all_numeric_labels1 = np.array([animals1.index(label) for label in np_arr_all_labels1]) # labels by index
        print("Done load prepared dataset.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!
        return np_arr_all_data1, np_arr_all_labels1, np_arr_all_numeric_labels1, animals1
    
    if Environmental_Sound_Classification_50 == False and Recorded_dataset == True:

        np_arr_all_data2, np_arr_all_labels2, animals2 = load_prepared_dataset(RECORDED_AUDIOS_DATASET_NAME)
        np_arr_all_numeric_labels2 = np.array([animals2.index(label) for label in np_arr_all_labels2]) # labels by index
        # if len(animals2)==0:
        #     message1 = messagebox.showinfo(title="Error", message="Please Prepare raw / Load prepared dataset that are not empty!")
        print("Done load prepared dataset.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!
        return np_arr_all_data2, np_arr_all_labels2, np_arr_all_numeric_labels2, animals2

    if Environmental_Sound_Classification_50 == True and Recorded_dataset == True:
        
        np_arr_all_data1, np_arr_all_labels1, animals1 = load_prepared_dataset(ESC50_DATASET_NAME)
        np_arr_all_data2, np_arr_all_labels2, animals2 = load_prepared_dataset(RECORDED_AUDIOS_DATASET_NAME)

        if len(animals2) != 0 :

            np_arr_all_data = np.append(np_arr_all_data1, np_arr_all_data2, 0) # np_arr_all_data = np_arr_all_data1 + np_arr_all_data2 (appends rows)
            np_arr_all_labels = np.append(np_arr_all_labels1, np_arr_all_labels2, 0) # np_arr_all_labels = np_arr_all_labels1 + np_arr_all_labels2 (appends rows)
            animals = animals1 + animals2
            animals = list(set(animals))
            np_arr_all_numeric_labels = np.array([animals.index(label) for label in np_arr_all_labels]) # labels by index
            print("Done load prepared dataset.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!
            return np_arr_all_data, np_arr_all_labels, np_arr_all_numeric_labels, animals
        else:
            np_arr_all_numeric_labels1 = np.array([animals1.index(label) for label in np_arr_all_labels1]) # labels by index
            print("Done load prepared dataset.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!
            return np_arr_all_data1, np_arr_all_labels1, np_arr_all_numeric_labels1, animals1


def load_prepared_dataset(dataset_name, prepared_datasets_path=PREPARED_DATASETS_PATH):
    '''
    Load all_data, all_labels from .npy files and animals from .txt file.

    Returns all_data, all_labels, animals.

    The first is a numpy array contains numpy arrays of each audio's numerical features - extract_features()
    The second numpy array contains *STRING* labeles.
    The arrays indexes align up between the three arrays. np.array(all_data)[idx] is classified as np.array(all_labels)[idx])
    animals is a list of animals classes as strings, his role is to match a between animal type to its numerical number. every animal type has the number that represent it .eventually animal type = animals[arg.max(y_predict)]
    '''
    
    print("Load prepared {} dataset.".format(dataset_name)) #NOTE:PRINT FOR DEBUGGING , DELETE!

    full_path = os.path.join(os.getcwd(), prepared_datasets_path)
    if not os.path.isdir(full_path) :
        os.mkdir(full_path)

    full_path = os.path.join(full_path, dataset_name)
    if not os.path.isdir(full_path) :
        os.mkdir(full_path)

    if not os.listdir (full_path) :
        print("{} prepared dataset is empty.\n".format(dataset_name))
        empty_list = []
        np_arr_empty_list = np.array(empty_list)
        return np_arr_empty_list, np_arr_empty_list, empty_list

    #loads all_data
    all_data_file = full_path+"/all_data_"+dataset_name+".npy"
    np_arr_all_data = np.load(all_data_file)

    #loads all_labels
    all_labels_file = full_path+"/all_labels_"+dataset_name+".npy"
    np_arr_all_labels = np.load(all_labels_file)

    #loads animals
    with open (full_path+"/animals_"+dataset_name+".txt", 'r') as filehandle:
        #filehandle.readline() returns the entire line from the file. its read it as a string.
        animals_as_str = filehandle.readline()
        #ast.literal_eval converts string of list to list
        animals = ast.literal_eval(animals_as_str) 

    print("Done load prepared {} dataset.".format(dataset_name)) #NOTE:PRINT FOR DEBUGGING , DELETE!

    return np_arr_all_data, np_arr_all_labels, animals

if __name__ == "__main__":

    all_data, all_labels, all_numeric_lebels, animals = load_prepared_datasets(Environmental_Sound_Classification_50=True, Recorded_dataset=True)
    print (animals)