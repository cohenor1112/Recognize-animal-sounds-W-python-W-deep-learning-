import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

#TODO : understand model accuracy and model loss parameters (what can i learn from them).
#TODO : understand the code that build the confusion_matrix.


def model_analysys(model ,x_test ,y_test, history, animals, fig, ax, plot_acc, plot_loss, plot_cm):
    '''
    get fig, ax to plot on.

    if plot_acc = True -> Plot history , Plots accuracy versus epochs.
    if plot_loss = True -> Plot history , Plots loss/error versus epochs.
    if plot_cm = True -> Plot confusion_matrix = Plots true_labels vs predictions_labels.

    return colorbar handle if plot_cm , so i can delelte him when needed (cm use colorbar).
    '''

    print("Do model analysys.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    cb = ""
    #Plot history = Plots accuracy & loss/error versus epochs
    if plot_acc == True or plot_loss == True:
        plot_history(plot_acc, plot_loss, ax, history)

    #Plot confusion_matrix:
    if plot_cm == True:
        #Make predictions on test set
        y_pred_percentages = model.predict(x_test) # predicted percentages
        y_pred = np.argmax(y_pred_percentages, axis=1) # Most prevalent prediction
        #Build confusion_matrix true_labels vs predictions_labels
        cm = confusion_matrix(y_test, y_pred)
        print (cm)                                                              ###
        #Plot confusion_matrix
        try:
            cb = plot_confusion_matrix(cm,animals, fig, ax)
        except:
            print("Error building confusion matrix because of imbalanced dataset.")

    print("Done model analysys.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

    return cb

def plot_history(plot_acc, plot_loss, ax, history = None):
    '''
    get ax to plot on.

    Plot history = Plots accuracy & loss/error versus epochs . made by history object.
    if plot_acc = True -> Plot history , Plots accuracy versus epochs.
    if plot_loss = True -> Plot history , Plots loss/error versus epochs.

    NOTE : history object is built on train and validation sets.
    '''

    print("Plot history = Plots accuracy & loss/error versus epochs.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    if not history:
        print("No history to plot.")
        return

    if plot_acc == True:
        #plot model accuracy in train/test sets
        ax.plot(history.history['accuracy'])
        ax.plot(history.history['val_accuracy'])
        ax.set_title('model accuracy')
        ax.set_ylabel('accuracy')
        ax.set_xlabel('epoch')
        ax.legend(['train', 'test'], loc='upper right')

    if plot_loss == True:
        #plot model loss in train/test sets
        ax.plot(history.history['loss'])
        ax.plot(history.history['val_loss'])
        ax.set_title('model loss')
        ax.set_ylabel('loss')
        ax.set_xlabel('epoch')
        ax.legend(['train', 'test'], loc='upper right')
        
    print("Done plot history.") #NOTE:PRINT FOR DEBUGGING , DELETE!


def plot_confusion_matrix(cm, animals, fig, ax):
    '''
    get fig, ax to plot on.

    Plot confusion_matrix = Plots true_labels vs predictions_labels .
    NOTE : confusion_matrix is built on test set.

    return colorbar handle if plot_cm , so i can delelte him when needed.
    '''

    cb = ""
    #if dataset imbalanced so cannot plot confusion matrix!!
    if len(np.arange(cm.shape[1])) == len(animals) and np.arange(cm.shape[0]) == len(animals) :

        print("Plot confusion_matrix = Plots true_labels vs predictions_labels.") #NOTE:PRINT FOR DEBUGGING , DELETE!

        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        cb = ax.figure.colorbar(im, ax=ax)
        # We want to show all ticks...
        ax.set(xticks=np.arange(cm.shape[1]),
                yticks=np.arange(cm.shape[0]),
                # ... and label them with the respective list entries
                xticklabels=animals,
                yticklabels=animals,
                title="Confusion Matrix",
                ylabel='True label',
                xlabel='Predicted label')
        ax.set_ylim(len(animals)-0.5, -0.5)
        ax.set_aspect('auto')

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

        plt.grid(None)
        # plt.show()

        print("Done plot confusion_matrix.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    else:

        print("Error building confusion matrix because of imbalanced dataset.")

    return cb