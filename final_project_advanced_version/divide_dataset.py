import numpy as np
import sklearn as sk
from sklearn.model_selection import train_test_split

#TODO : use also validation in our model: maybe - VALIDATION_SIZE = 0.2

TEST_SIZE = 0.2

def divide_dataset(np_arr_all_data,np_arr_all_numeric_lebels,test_size=TEST_SIZE):
    '''
    Divide dataset for train and test , by TEST_SIZE .
    
    Returns x_train, x_test, y_train, y_test
    '''

    print("Divide dataset for train and test.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    x_train, x_test, y_train, y_test = sk.model_selection.train_test_split(np_arr_all_data, np_arr_all_numeric_lebels, test_size=test_size, shuffle=True)
    
    print("Done divide dataset for train and test.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

    return x_train, x_test, y_train, y_test
