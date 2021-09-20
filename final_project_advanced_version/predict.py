import numpy as np
import matplotlib.pyplot as plt

def predict_input_features(model , input_features , animals):
    '''
    Predict a single sound using the trained model

    :param model: Trained classifier
    :param input_features: Input data = numpy array of features of the sound
    :param animals : decoder for output

    Show predictions probabilities on a bar graph.
    Returns predicted_index (int) , predicted_animal (str) , probability_array_percentages (arr of floats)
    '''

    print("Predict input features.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    #input_features shape is (187,) . so to adjust its shape for model.predict() - add a dimension to be (1,187). 
    input_features = input_features[np.newaxis, ...] # now input_features shape (1,187) adjusted to model.predict

    # perform predictions . model.predict return numpy array of numpy arrays of predictions
    predictions = model.predict(input_features)

    #prediction = model prediction for that single input data
    prediction = predictions[0]

    #calculate and show predictions probabilities.
    probability_array = prediction / np.sum(prediction)
    probability_array_percentages = [float(format(value*100,'.3f')) for value in probability_array]
    #show_probabilities_hist(animals,probability_array_percentages)

    # get index with max value
    predicted_index = np.argmax(prediction)
    #get predicted animal using decoder animals
    predicted_animal = animals[predicted_index]

    #print("Predicted animal: {}".format(predicted_animal))

    print("Done predict input features.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

    return predicted_index , predicted_animal , probability_array_percentages


def show_probabilities_hist(animals , probability_array_percentages, fig, ax):
    '''
    get  fig, ax to plot on.
    Plot a bar graph of predictions probabilites.
    -show on every bar its value .
    -paint bar with max value in red .
    TODO: adjust axis y to fit size of figure *for every animals size* .
    '''

    print("Plot a bar graph of predictions probabilites.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    ax.set_ylabel("Animals")
    ax.set_xlabel("Predictions percentages[%]")
    ax.set_xlim(0,100)
    max_probability = np.max(probability_array_percentages)
    clrs = ['blue' if (probability < max_probability) else 'red' for probability in probability_array_percentages]
    for i, v in enumerate(probability_array_percentages):
        ax.text(v, i-0.19, str(v) ,color = clrs[i],  fontweight='bold')
    ax.barh(animals,probability_array_percentages,color = clrs)

    print("Done plot a bar graph of predictions probabilites.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!