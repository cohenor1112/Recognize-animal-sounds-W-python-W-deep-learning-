import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 

import os

#ANIMALS_INFO_PATH = "animals_info/"
ANIMALS_INFO_PATH = "animals_info"

def get_animal_info (animal, fig, ax):
    '''
    get fig, ax to plot on the image.
    Get animal info by text and image.
    
    Return animal_info_text , and plot animal_info_image.
    '''

    print("Get animal info by text and image.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    animal_info_text = get_animal_info_text(animal)
    get_animal_info_image(animal, fig, ax)

    print("Done get animal info by text and image.\n") #NOTE:PRINT FOR DEBUGGING , DELETE!

    return animal_info_text

def get_animal_info_text(animal):
    '''
    get animal information from .txt files that in folder ANIMALS_INFO_TEXT_PATH = "animals_info/animals_info_texts/" ,
    input = animal (as str)
    output = animal_info (str) 
    '''

    print("Get animal info by text.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    #some DEFINES:
    #ANIMALS_INFO_TEXT_PATH = ANIMALS_INFO_PATH + "animals_info_texts/"
    ANIMALS_INFO_TEXT_PATH = os.path.join(os.getcwd(),ANIMALS_INFO_PATH)
    ANIMALS_INFO_TEXT_PATH = os.path.join(ANIMALS_INFO_TEXT_PATH,"animals_info_texts")
    ANIMAL_INFO_TEXT_FILE = os.path.join(ANIMALS_INFO_TEXT_PATH,animal)+'.txt'

    if not os.path.exists(ANIMAL_INFO_TEXT_FILE):
        print ("No animal info by text.")
        return "No animal info by text."

    with open (ANIMAL_INFO_TEXT_FILE, 'r') as txt_file:
        animal_info = txt_file.read()

    print("Done get animal info by text.") #NOTE:PRINT FOR DEBUGGING , DELETE!

    return animal_info

def get_animal_info_image(animal, fig, ax):
    '''
    get fig, ax to plot on the image.

    get animal information from .png files that in folder ANIMALS_INFO_IMAGE_PATH = "animals_info/animals_info_images/" ,
    input = animal (as str)
    #NOTE : there is no output , this function show image on plot . 
    '''

    print("Get animal info by image.") #NOTE:PRINT FOR DEBUGGING , DELETE!
    
    #some DEFINES:
    #ANIMALS_INFO_IMAGE_PATH = ANIMALS_INFO_PATH + "animals_info_images/"
    ANIMALS_INFO_IMAGE_PATH = os.path.join(os.getcwd(),ANIMALS_INFO_PATH)
    ANIMALS_INFO_IMAGE_PATH = os.path.join(ANIMALS_INFO_IMAGE_PATH,"animals_info_images")
    ANIMAL_INFO_PNG_FILE = os.path.join(ANIMALS_INFO_IMAGE_PATH,animal)+'.png'
    
    if not os.path.exists(ANIMAL_INFO_PNG_FILE):
        print ("No animal info by image.")
        ANIMAL_INFO_PNG_FILE = os.path.join(ANIMALS_INFO_IMAGE_PATH,"No_image_to_show") + '.png'
        img = mpimg.imread(ANIMAL_INFO_PNG_FILE)
        ax.imshow(img)
        return "No animal info by image."
    
    # Read Images 
    #img = mpimg.imread(ANIMALS_INFO_IMAGE_PATH+animal+'.png') 
    img = mpimg.imread(ANIMAL_INFO_PNG_FILE) 

    # Output Images 
    ax.imshow(img) 

    print("Done get animal info by image.") #NOTE:PRINT FOR DEBUGGING , DELETE!


if __name__ == "__main__":
    animal_info = get_animal_info_text("or") 
    print (animal_info)