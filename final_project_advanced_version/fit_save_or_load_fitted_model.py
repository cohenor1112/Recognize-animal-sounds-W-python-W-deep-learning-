import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint

#TODO : maybe save in another way , without ModelCheckpoint. if use ModelCheckpoint so learn what is it

EPOCHS     = 60
BATCH_SIZE = 50
#TODO : understand why epochs and batch_size like that.

def fit_save_or_load_fitted_model(model, load_model_file_name , save_model_file_in_name ,x_train, y_train,x_test, y_test):
    '''
    Fit / Fit and save / Load fitted model.
    Return fitted model.
    '''

    print("Fit / Fit and save / Load fitted model.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    history = None

    #load fitted model 
    if load_model_file_name:

        print("Load fitted model.")#NOTE:PRINT FOR DEBUGGING , DELETE!

        models_folder_path = os.path.join(os.getcwd(),"models")
        is_path = os.path.isdir(models_folder_path)
        if not is_path:
            os.mkdir(models_folder_path)

        model_full_path = os.path.join(models_folder_path, load_model_file_name + ".hdf5")
        model.load_weights(model_full_path)
        print("Done Load fitted model.")#NOTE:PRINT FOR DEBUGGING , DELETE!

    #fit and save model
    elif save_model_file_in_name:

        print("Fit and save model.")#NOTE:PRINT FOR DEBUGGING , DELETE!

        models_folder_path = os.path.join(os.getcwd(),"models")
        is_path = os.path.isdir(models_folder_path)
        if not is_path:
            os.mkdir(models_folder_path)

        model_full_path_no_hdf5 = os.path.join(models_folder_path,save_model_file_in_name)
        if os.path.exists(model_full_path_no_hdf5+'.hdf5'):
            i=1
            while os.path.exists(model_full_path_no_hdf5+'({})'.format(i)+'.hdf5'):
                i+=1
            save_model_file_in_name = save_model_file_in_name+'({})'.format(i)

        print("name = " + save_model_file_in_name + ".hdf5")#NOTE:PRINT FOR DEBUGGING , DELETE!

        model_full_path = os.path.join(models_folder_path, save_model_file_in_name + ".hdf5")
        
        checkpointer = ModelCheckpoint(filepath=model_full_path,
                                       monitor='val_loss', 
                                       save_best_only=True,
                                       verbose=1)
        
        history = model.fit(x_train, y_train,
                            epochs=EPOCHS,
                            batch_size=BATCH_SIZE,
                            validation_data=(x_test, y_test),
                            callbacks=[checkpointer],
    #                       shuffle=True,
                            verbose=2)
        print("Done Fit and save model. Model name is : {}".format(save_model_file_in_name)) #NOTE:PRINT FOR DEBUGGING , DELETE!
    
    #fit model
    else:

        print("Fit model.")#NOTE:PRINT FOR DEBUGGING , DELETE!

        history = model.fit(x_train, y_train,
                            epochs=EPOCHS,
                            batch_size=BATCH_SIZE,
                            validation_data=(x_test, y_test),
    #                       shuffle=True,
                            verbose=2)
        print("Done Fit model.")#NOTE:PRINT FOR DEBUGGING , DELETE!
        
    print("Done fit / fit and save / load fitted model.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

    return model , history