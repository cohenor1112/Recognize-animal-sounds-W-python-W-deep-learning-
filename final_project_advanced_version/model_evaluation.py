import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def model_evaluation(model, x_test, y_test):
    '''
    model evaluation prints Test Accuracy calculated with model.evaluate
    '''

    print('Evaluate model on test set.') #NOTE:PRINT FOR DEBUGGING , DELETE!

    # evaluate model on test set
    test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)
    print('Test accuracy: {}%'.format(float(format(test_acc*100,'.3f'))))

    print('Done evaluate model on test set.\n') #NOTE:PRINT FOR DEBUGGING , DELETE!