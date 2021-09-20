import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Activation, Dense

'''
#TODO : understand in build: why Sequential ,why thats amount of layers, why thats amount of nuirons in every layer , why activation 'relu' in every layer, why activation 'softmax' in last layer.
#TODO : understand in compile: why loss = 'sparse_categorical_crossentropy' , why optimizer Adam and why his parameters are.
'''

OPTIMIZER = keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)

def build_and_compile_model(input_dim,n_classes):
  '''
  Build and compile deep learning model for our classifier (match dynamically input and output dimension).

  Return model
  '''

  print ("Build and compile deep learning model for our classifier.") #NOTE:PRINT FOR DEBUGGING , DELETE!

  model = Sequential()
  model.add(Dense(256, activation='relu',  input_dim=input_dim))
  model.add(Dense(128, activation='relu'))
  model.add(Dense(64, activation='relu'))
  model.add(Dense(n_classes, activation='softmax')) # sigmoid

  model.compile(loss='sparse_categorical_crossentropy', optimizer=OPTIMIZER, metrics=['accuracy'])

  print ("Done build and compile deep learning model for our classifier.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

  return model


