#all imports:
#-------------------------------
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt

import sys
from io import StringIO
#-------------------------------
#working on dataset :
import prepare_datasets
import load_prepared_datasets
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
#from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
#-------------------------------
#extract features from audio and predict (and get other information) from features:
import extract_features
import predict
#-------------------------------
#get animal information :
import animal_info
#-------------------------------
#sat audio feedback :
from feedback import Feedback
#-------------------------------
import os
import shutil

#-----------------------------------------------------------------------------------------------------------------
'''
Table of Contents: #TODO : UPDATE IT

1)Model variables/defines ........................................ line 75
2)First window : ................................................. line 144
				1)Variables for first window ..................... line 147
				2)Frames for first window ........................ line 172
				3)Widgets for first window ....................... line 205
3)Second window : ................................................ line 314
				1)Variables for second window .................... line 317
				2)Frames for second window ....................... line 340
				3)Widgets for second window ...................... line 373
4)Methods : ...................................................... line 472
				1)First window methods ........................... line 475
				2)Second window methods .......................... line 1140
				3)Other methods................................... line 1505
'''

class App:

	# Constructor

	def __init__(self, master):

		#---------------------------------------
		# Model variables/defines :

		self.DATASETS_PATH = "Datasets"

		self.ESC50_DATASET_NAME = "Environmental_Sound_Classification_50"

		self.RECORDED_AUDIOS_DATASET_NAME = "Recorded_audios"

		self.PREPARED_DATASETS_PATH = "Prepared_Datasets"

		self.SAVE_RECORDS_TMP_PATH = "tmp_recorded_audio"
        
		self.RECORD_TMP_NAME = "tmp_recorded_audio"

		self.PROBABILITY_TRESHOLD = 0

		self.ANIMALS_INFO_PATH = "animals_info"

		self.ANIMALS_INFO_TXT_PATH = "animals_info_texts"

		self.ANIMALS_INFO_IMAGE_PATH = "animals_info_images"

		#---------------------------------------
		# Some Defines to adjust gui for computer screen size :

		# For first window :

		self.TEXT_USER_GUIDE1_HEIGHT = 2 #Ideal for a 13.3-inch screen = 2
		self.TEXT_USER_GUIDE1_WIDTH = 70 #Ideal for a 13.3-inch screen = 70

		self.TEXT_COMMAND_VIEW1_HEIGHT = 8 #Ideal for a 13.3-inch screen = 8
		self.TEXT_COMMAND_VIEW1_WIDTH = 70 #Ideal for a 13.3-inch screen = 70

		self.FIG_MODEL_ANALYSYS_SIZE = (6.55,4.6) #Ideal for a 13.3-inch screen = (6.55,4.6)

		#-------------------
		# For second window :

		self.TEXT_USER_GUIDE2_HEIGHT = 2 #Ideal for a 13.3-inch screen = 2
		self.TEXT_USER_GUIDE2_WIDTH = 55 #Ideal for a 13.3-inch screen = 55

		self.TEXT_COMMAND_VIEW2_HEIGHT = 9 #Ideal for a 13.3-inch screen = 9
		self.TEXT_COMMAND_VIEW2_WIDTH = 55 #Ideal for a 13.3-inch screen = 55

		self.FIG_PROBABILITIES_BAR_GRAPH_SIZE = (7.6,2.6) #Ideal for a 13.3-inch screen = (7.6,2.6)

		self.TEXT_ANIMAL_INFO_HEIGHT = 5 #Ideal for a 13.3-inch screen = 5
		self.TEXT_ANIMAL_INFO_WIDTH = 96 #Ideal for a 13.3-inch screen = 96

		self.FIG_ANIMAL_IMAGE_SIZE = (1.4,1.4) #Ideal for a 13.3-inch screen = (1.4,1.4)

		#---------------------------------------
		# First window and second window :

		self.firstwindow = master

		self.secondwindow = tk.Toplevel(self.firstwindow)

		self.secondwindow.state("withdrawn")

		#---------------------------------------

		# Variables for stdout to be printed on text widget in gui :

		self.command_view_string = StringIO()
		
		sys.stdout = self.command_view_string
		
#-----------------------------------------------------------------------------------------------------------------
		# First window :

#-------------------------------------------------------------------		
		# Variables for first window :

		# Prepare raw/Load dataset :

		self.var_prepare_or_load_dataset = tk.IntVar()
		self.var_dataset_esc50 = tk.IntVar()
		self.var_dataset_recorded_audios = tk.IntVar()

		# Train model :

		self.var_train_model = tk.IntVar()
		self.var_save_fitted_model = tk.IntVar()
		self.var_name_of_fitted_model_to_save = tk.StringVar()

		# Load model :

		self.var_load_model = tk.IntVar()

		# Model Summary, Evaluation and Analysis :
		
		self.fig_model_analysys = Figure(figsize=self.FIG_MODEL_ANALYSYS_SIZE, dpi=100)
		self.plot_model_analysys = self.fig_model_analysys.add_subplot(111)
		self.color_bar_handle = ""

#-------------------------------------------------------------------
		# Frames for first window :

		# Prepare raw/Load dataset Frame (the top side) :

		self.frame_prepare_or_load_dataset = tk.LabelFrame(self.firstwindow, text="Prepare raw/Load dataset :")
		self.frame_prepare_or_load_dataset.grid(row=0, column=0, columnspan=2, padx=5, pady=4)

		# Train Model Frame (the left side) :

		self.frame_train_model = tk.LabelFrame(self.firstwindow, text="Train model :")
		self.frame_train_model.grid(row=1, column=0, padx=5, pady=4)

		# Load Model Frame (the right side) :

		self.frame_load_model = tk.LabelFrame(self.firstwindow, text="Load fitted model :")
		self.frame_load_model.grid(row=1, column=1, padx=5, pady=4)

		# User guide (the buttom side) :
		
		self.frame_user_guide1 = tk.LabelFrame(self.firstwindow, text="User Guide")
		self.frame_user_guide1.grid(row=2, column=0, columnspan=2, padx=5, pady=4)

		# Command view (the buttom side) :

		self.frame_command_view1 = tk.LabelFrame(self.firstwindow, text="Command View")
		self.frame_command_view1.grid(row=3, column=0, columnspan=2, padx=5, pady=4)

		# Model Info Frame (the entire right part) :

		self.frame_model_info = tk.LabelFrame(self.firstwindow, text="Model Summary, Evaluation and Analysis :")
		self.frame_model_info.grid(row=0, column=2, rowspan=4, padx=5, pady=4)

#-------------------------------------------------------------------
		# Widgets for first window :

		# The widgets for Prepare raw/Load dataset frame :

		self.radiobutton_prepare_raw_dataset = tk.Radiobutton(self.frame_prepare_or_load_dataset, text="Prepare raw dataset", variable=self.var_prepare_or_load_dataset, value=1, padx=5, pady=4,command=self.clicked_prepare_or_load_dataset_radiobuttons)
		self.radiobutton_prepare_raw_dataset.grid(row=0, sticky=tk.W)

		self.radiobutton_load_prepared_dataset = tk.Radiobutton(self.frame_prepare_or_load_dataset, text="Load prepared dataset", variable=self.var_prepare_or_load_dataset, value=2, padx=5, pady=4,command=self.clicked_prepare_or_load_dataset_radiobuttons)
		self.radiobutton_load_prepared_dataset.grid(row=1, sticky=tk.W)

		self.Label_choose_dataset = tk.Label(self.frame_prepare_or_load_dataset, text="Choose a dataset to train from:", padx=5, pady=4)
		self.Label_choose_dataset.grid(row=3, sticky = tk.W)

		self.checkbox_esc50_dataset = tk.Checkbutton(self.frame_prepare_or_load_dataset, text="Environmental Sound\nClassification Dataset", variable=self.var_dataset_esc50, padx=5, pady=4,state=tk.DISABLED, command=self.clicked_esc50_dataset_checkbox)
		self.checkbox_esc50_dataset.grid(row=4, sticky=tk.W)

		self.checkbox_recorded_audios_dataset = tk.Checkbutton(self.frame_prepare_or_load_dataset, text="Recorded audios dataset", variable=self.var_dataset_recorded_audios, padx=5, pady=4,state=tk.DISABLED, command=self.clicked_recorded_audios_dataset_checkbox)
		self.checkbox_recorded_audios_dataset.grid(row=5, sticky=tk.W)

		self.button_prepare_or_load_dataset = tk.Button(self.frame_prepare_or_load_dataset, text="Prepare raw/Load dataset", padx=5, pady=4, state=tk.DISABLED, command=self.clicked_prepare_or_load_dataset_button)
		self.button_prepare_or_load_dataset.grid(row=6, padx=5, pady=4)

		# The widgets for train model frame :

		self.checkbox_train_model = tk.Checkbutton(self.frame_train_model, text="Train a deep learning model", variable=self.var_train_model, state=tk.DISABLED, padx=5, pady=4, command=self.clicked_train_model_checkbox)
		self.checkbox_train_model.grid(row=0, sticky=tk.W)

		self.Label_save_model = tk.Label(self.frame_train_model, text="Save the trained model?", padx=5, pady=4)
		self.Label_save_model.grid(row = 1, sticky = tk.W)

		self.checkbox_save_model = tk.Checkbutton(self.frame_train_model, text="Yes", variable=self.var_save_fitted_model, state=tk.DISABLED, command=self.clicked_save_model_checkbox)
		self.checkbox_save_model.grid(row=1, column=1, sticky=tk.W)

		self.Label_model_name = tk.Label(self.frame_train_model, text="Model name :", padx=5, pady=4)
		self.Label_model_name.grid(row = 2, column=0, sticky = tk.W)

		self.entry_name_of_fitted_model_to_save = tk.Entry(self.frame_train_model, textvariable=self.var_name_of_fitted_model_to_save, state=tk.DISABLED)
		self.entry_name_of_fitted_model_to_save.grid(row=2, column=1, sticky=tk.W, padx=5, pady=4)

		self.button_train_model = tk.Button(self.frame_train_model, text="Train the model!", state=tk.DISABLED, command=self.clicked_train_model_button)
		self.button_train_model.grid(row=3, sticky=tk.W, padx=5, pady=4)

		# The widgets for load model frame :

		self.checkbox_load_model = tk.Checkbutton(self.frame_load_model, text="Load a trained deep learning model", variable=self.var_load_model, state=tk.DISABLED, padx=5, pady=4, command=self.clicked_load_model_checkbox)
		self.checkbox_load_model.grid(row=0, sticky=tk.W)

		self.Label_model_load = tk.Label(self.frame_load_model, text="Choose a model to load : ", padx=5, pady=4)
		self.Label_model_load.grid(row=1, sticky=tk.W)

		self.button_browse_model = tk.Button(self.frame_load_model, text="Browse", state=tk.DISABLED, command=self.clicked_browse_model_button)
		self.button_browse_model.grid(row=2, sticky=tk.W, padx=5, pady=4)

		self.button_load_model = tk.Button(self.frame_load_model, text="Load the model!", state=tk.DISABLED, command=self.clicked_load_model_button)
		self.button_load_model.grid(row=3, sticky=tk.W, padx=5, pady=4)

		# User guide :

		self.scrollbar_text_user_guide1 = tk.Scrollbar(self.frame_user_guide1)
		self.scrollbar_text_user_guide1.grid(row=0, column=2, sticky=tk.N + tk.S)

		self.text_user_guide1 = tk.Text(self.frame_user_guide1, height=self.TEXT_USER_GUIDE1_HEIGHT, width=self.TEXT_USER_GUIDE1_WIDTH, yscrollcommand=self.scrollbar_text_user_guide1.set)
		self.text_user_guide1.grid(row=0, column=0, columnspan=2, padx=5, pady=4)
		self.update_text_user_guide(self.text_user_guide1,"Please choose: 'Prepare raw dataset' / 'Load prepared dataset'.")
		self.text_user_guide1.config(state=tk.DISABLED)

		self.scrollbar_text_user_guide1.config(command=self.text_user_guide1.yview)

		# Command view :

		self.scrollbar_text_command_view1 = tk.Scrollbar(self.frame_command_view1)
		self.scrollbar_text_command_view1.grid(row=0, column=2, sticky=tk.N + tk.S)

		self.text_command_view1 = tk.Text(self.frame_command_view1, height=self.TEXT_COMMAND_VIEW1_HEIGHT, width=self.TEXT_COMMAND_VIEW1_WIDTH, yscrollcommand=self.scrollbar_text_command_view1.set)
		self.text_command_view1.grid(row=0, column=0, columnspan=2, padx=5, pady=4)
		self.text_command_view1.config(state=tk.DISABLED)

		self.scrollbar_text_command_view1.config(command=self.text_command_view1.yview)

		# The widgets for model info frame : 

		self.button_plot_model_accuracy = tk.Button(self.frame_model_info, text="Plot Model Accuracy", state=tk.DISABLED, command=self.clicked_plot_model_accuracy_button)
		self.button_plot_model_accuracy.grid(row=0, column=0, padx=5, pady=4)

		self.button_plot_model_loss = tk.Button(self.frame_model_info, text="Plot Model Loss", state=tk.DISABLED, command=self.clicked_plot_model_loss_button)
		self.button_plot_model_loss.grid(row=0, column=1, padx=5, pady=4)

		self.button_plot_confusion_matrix = tk.Button(self.frame_model_info, text="Plot Confusion Matrix", state=tk.DISABLED, command=self.clicked_plot_confusion_matrix_button)
		self.button_plot_confusion_matrix.grid(row=0, column=2, padx=5, pady=4)

		self.button_clear_info = tk.Button(self.frame_model_info, text="Clear Info", state=tk.DISABLED, command=self.clicked_clear_info_button)
		self.button_clear_info.grid(row=3, column=0, columnspan=3, padx=5, pady=4)

		self.canvas_model_analysys = FigureCanvasTkAgg(self.fig_model_analysys, master=self.frame_model_info)
		self.canvas_model_analysys.get_tk_widget().grid(row=1, columnspan=3, padx=5, pady=4)

		self.toolbar_model_analysys = NavigationToolbar2Tk(self.canvas_model_analysys, self.frame_model_info, pack_toolbar=False)
		self.toolbar_model_analysys.grid(row=2, column=0, columnspan=3, padx=5, pady=4)
		self.toolbar_model_analysys.update()

		# Widgets outside of any frame :

		self.button_next = tk.Button(self.firstwindow, text="Next", state=tk.DISABLED, command=self.clicked_next_button)
		self.button_next.grid(row=4, column=0, columnspan=2, padx=5, pady=4, sticky=tk.E)

		self.button_clear_command_view1 = tk.Button(self.firstwindow, text="Clear Command View", command=self.clicked_clear_command_view1_button)
		self.button_clear_command_view1.grid(row=4, column=0, columnspan=2, padx=5, pady=4, sticky=tk.W)

#-----------------------------------------------------------------------------------------------------------------
		# Second window :

#-------------------------------------------------------------------		
		# Variables for second window :

		# Record audio :

		self.var_record_audio = tk.IntVar()

		# Load audio :

		self.var_load_audio = tk.IntVar()

		# Play, Predict and Save audio :

		self.var_set_audio_feedback = tk.IntVar()

		# Prediction summary : 
		
		self.fig_probabilities_bar_graph = Figure(figsize=self.FIG_PROBABILITIES_BAR_GRAPH_SIZE, dpi=100)
		self.plot_probabilities_bar_graph = self.fig_probabilities_bar_graph.add_subplot(111)

		self.fig_animal_image = Figure(figsize=self.FIG_ANIMAL_IMAGE_SIZE, dpi=100)
		self.plot_animal_image = self.fig_animal_image.add_subplot(111)
		
#-------------------------------------------------------------------
		# Frames for second window :

		# Record Audio File Frame (the left side) :

		self.frame_record_audio = tk.LabelFrame(self.secondwindow, text="Record your own audio")
		self.frame_record_audio.grid(row=0, column=0, padx=5, pady=4)

		# Load Audio File Frame (the right side) :

		self.frame_load_audio = tk.LabelFrame(self.secondwindow, text="Load an audio sample")
		self.frame_load_audio.grid(row=0, column=1, padx=5, pady=4)

		# Analyze and save audio Frame (the middle side) :

		self.frame_analyze_and_save_audio = tk.LabelFrame(self.secondwindow, text="Analyze and Save audio")
		self.frame_analyze_and_save_audio.grid(row=1, column=0, columnspan=2, padx=5, pady=4)

		# User guide (the buttom side) :
		
		self.frame_user_guide2 = tk.LabelFrame(self.secondwindow, text="User Guide")
		self.frame_user_guide2.grid(row=2, column=0, columnspan=2, padx=5, pady=4)

		# Command view (the buttom side) :

		self.frame_command_view2 = tk.LabelFrame(self.secondwindow, text="Command View")
		self.frame_command_view2.grid(row=3, column=0, columnspan=2, padx=5, pady=4)

		# Prediction Info Frame (the entire right side) :

		self.frame_prediction_info = tk.LabelFrame(self.secondwindow, text="Prediction summary")
		self.frame_prediction_info.grid(row=0, column=2, rowspan=4, pady=4)

#-------------------------------------------------------------------
		# Widgets for second window

		# The widgets for record audio frame :

		self.checkbox_record_audio = tk.Checkbutton(self.frame_record_audio, text="Record your own audio\nusing a microphone", variable=self.var_record_audio, padx=5, pady=4, command=self.clicked_record_audio_checkbox)
		self.checkbox_record_audio.grid(row=0, sticky=tk.W)

		self.button_record = tk.Button(self.frame_record_audio, text="Record", state=tk.DISABLED, command=self.clicked_record_audio_button)
		self.button_record.grid(row=0, column=1, padx=5, pady=4, sticky=tk.W)

		# The widgets for load audio frame :

		self.checkbox_load_audio = tk.Checkbutton(self.frame_load_audio, text="Load an audio sample", variable=self.var_load_audio, padx=5, pady=4, command=self.clicked_load_audio_checkbox)
		self.checkbox_load_audio.grid(row=0, sticky=tk.W)

		self.Label_load_audio = tk.Label(self.frame_load_audio, text="Choose an audio sample to load : ", padx=5, pady=4)
		self.Label_load_audio.grid(row=1, sticky=tk.W)

		self.button_browse_audio = tk.Button(self.frame_load_audio, text="Browse", state=tk.DISABLED, command=self.clicked_browse_audio_button)
		self.button_browse_audio.grid(row=2, sticky=tk.W, padx=5, pady=4)

		# Widgets for Analyze and Save audio frame :

		self.button_play_sound = tk.Button(self.frame_analyze_and_save_audio, text="Play audio", state=tk.DISABLED, command=self.clicked_play_audio_button)
		self.button_play_sound.grid(row=0, column=0, columnspan=2, padx=5, pady=4)

		self.button_predict = tk.Button(self.frame_analyze_and_save_audio, text="Predict", state=tk.DISABLED, command=self.clicked_predict_button)
		self.button_predict.grid(row=1, column=0, columnspan=2, padx=5, pady=4)

		self.Label_set_recorded_audio_feedback = tk.Label(self.frame_analyze_and_save_audio, text="Set audio feedback?", padx=5, pady=4)
		self.Label_set_recorded_audio_feedback.grid(row = 2, sticky = tk.W)

		self.checkbox_set_audio_feedback = tk.Checkbutton(self.frame_analyze_and_save_audio, text="Yes", variable=self.var_set_audio_feedback, state=tk.DISABLED, command=self.clicked_set_recorded_audio_feedback_checkbox)
		self.checkbox_set_audio_feedback.grid(row=2, column=1, sticky=tk.W)

		self.button_set_audio_feedback = tk.Button(self.frame_analyze_and_save_audio, text="Set audio feedback", state=tk.DISABLED, command=self.clicked_set_audio_feedback_button)
		self.button_set_audio_feedback.grid(row=4, column=0, columnspan=2, padx=5, pady=4)

		# Widgets for User guide :

		self.scrollbar_text_user_guide2 = tk.Scrollbar(self.frame_user_guide2)
		self.scrollbar_text_user_guide2.grid(row=0, column=2, sticky=tk.N + tk.S)
		
		self.text_user_guide2 = tk.Text(self.frame_user_guide2, height=self.TEXT_USER_GUIDE2_HEIGHT, width=self.TEXT_USER_GUIDE2_WIDTH, yscrollcommand=self.scrollbar_text_user_guide2.set)
		self.text_user_guide2.grid(row=0, column=0, columnspan=2, padx=5, pady=4)
		self.update_text_user_guide(self.text_user_guide2,"Please choose: 'Record your own audio using a microphon' / 'Load an audio sample'.")
		self.text_user_guide2.config(state=tk.DISABLED)
		
		self.scrollbar_text_user_guide2.config(command=self.text_user_guide2.yview)

		# Widgets for Command view :

		self.scrollbar_text_command_view2 = tk.Scrollbar(self.frame_command_view2)
		self.scrollbar_text_command_view2.grid(row=0, column=2, sticky=tk.N + tk.S)

		self.text_command_view2 = tk.Text(self.frame_command_view2, height=self.TEXT_COMMAND_VIEW2_HEIGHT, width=self.TEXT_COMMAND_VIEW2_WIDTH, yscrollcommand=self.scrollbar_text_command_view2.set)
		self.text_command_view2.grid(row=0, column=0, columnspan=2, padx=5, pady=4)
		self.text_command_view2.config(state=tk.DISABLED)

		self.scrollbar_text_command_view2.config(command=self.text_command_view2.yview)

		# The widgets for prediction info frame :

		self.canvas_probabilities_bar_graph = FigureCanvasTkAgg(self.fig_probabilities_bar_graph, master=self.frame_prediction_info)
		self.canvas_probabilities_bar_graph.get_tk_widget().grid(row=0, columnspan=3, pady=4)

		self.toolbar_probabilities_bar_graph = NavigationToolbar2Tk(self.canvas_probabilities_bar_graph, self.frame_prediction_info, pack_toolbar=False)
		self.toolbar_probabilities_bar_graph.grid(row=1, column=0, columnspan=3, padx=5, pady=4)
		self.toolbar_probabilities_bar_graph.update()

		#----------------

		self.scrollbar_text_animal_info = tk.Scrollbar(self.frame_prediction_info)
		self.scrollbar_text_animal_info.grid(row=2, column=3, sticky=tk.N + tk.S)

		self.text_animal_info = tk.Text(self.frame_prediction_info, height=self.TEXT_ANIMAL_INFO_HEIGHT, width=self.TEXT_ANIMAL_INFO_WIDTH, yscrollcommand=self.scrollbar_text_animal_info.set)
		self.text_animal_info.grid(row=2, columnspan=3, pady=4)
		self.text_animal_info.config(state=tk.DISABLED)

		self.scrollbar_text_animal_info.config(command=self.text_animal_info.yview)

		#----------------

		self.canvas_animal_image = FigureCanvasTkAgg(self.fig_animal_image, master=self.frame_prediction_info)
		self.canvas_animal_image.get_tk_widget().grid(row=3, columnspan=3, padx=5, pady=4)

		self.toolbar_animal_image = NavigationToolbar2Tk(self.canvas_animal_image, self.frame_prediction_info, pack_toolbar=False)
		self.toolbar_animal_image.grid(row=4, column=0, columnspan=3, padx=5, pady=4)
		self.toolbar_animal_image.update()

		# Widgets outside of any frame :

		self.button_previous = tk.Button(self.secondwindow, text="Previous", command=self.clicked_previous_button)
		self.button_previous.grid(row=4, column=0, padx=5, pady=0, sticky=tk.W)

		self.button_clear_command_view2 = tk.Button(self.secondwindow, text="Clear Command View", command=self.clicked_clear_command_view2_button)
		self.button_clear_command_view2.grid(row=4, column=0, columnspan=2, padx=5, pady=4, sticky=tk.E)

#-----------------------------------------------------------------------------------------------------------------
	#Methods:

#-------------------------------------------------------------------
	# First window methods

	def clicked_prepare_or_load_dataset_radiobuttons(self):
		'''
		ENABLE and deselct 1 step below : checkbox_esc50_dataset, checkbox_recorded_audios_dataset.
		DISABLE 2 steps below : button_prepare_or_load_dataset.
		DISABLE and deselct 3 steps below : left side, right side.
		DISABLE 4-7 steps below : model info.
		DISABLE 8 steps below : button next.
		update_text_user_guide1.
		'''

		#ENABLE and deselct 1 step below : checkbox_esc50_dataset, checkbox_recorded_audios_dataset
		self.checkbox_esc50_dataset.config(state=tk.NORMAL)
		self.checkbox_esc50_dataset.deselect()
		self.checkbox_recorded_audios_dataset.config(state=tk.NORMAL)
		self.checkbox_recorded_audios_dataset.deselect()

		#DISABLE 2 steps below : button_prepare_or_load_dataset
		self.button_prepare_or_load_dataset.config(state=tk.DISABLED)

		#DISABLE and deselct 3 steps below : left side, right side 
		#DISABLE and deselct all left side
		self.checkbox_train_model.deselect()
		self.checkbox_train_model.config(state=tk.DISABLED)
		self.checkbox_save_model.deselect()
		self.checkbox_save_model.config(state=tk.DISABLED)
		self.entry_name_of_fitted_model_to_save.delete(0, tk.END)
		self.entry_name_of_fitted_model_to_save.config(state=tk.DISABLED)
		self.button_train_model.config(state=tk.DISABLED)
		#DISABLE and deselct all right side
		self.checkbox_load_model.deselect()
		self.checkbox_load_model.config(state=tk.DISABLED)
		self.button_browse_model.config(state=tk.DISABLED)
		
		#DISABLE 4-7 steps below : model info
		self.button_plot_model_accuracy.config(state=tk.DISABLED)
		self.button_plot_model_loss.config(state=tk.DISABLED)
		self.button_plot_confusion_matrix.config(state=tk.DISABLED)
		#clear canvas
		if self.color_bar_handle != "":
			self.color_bar_handle.remove()
			self.color_bar_handle = ""
		self.plot_model_analysys.cla()
		self.canvas_model_analysys.draw()
		#DISABLE button_clear_info
		self.button_clear_info.config(state=tk.DISABLED)

		#DISABLE 8 steps below : button next
		self.button_next.config(state=tk.DISABLED)

		#update_text_user_guide1
		self.update_text_user_guide(self.text_user_guide1,"Please choose a dataset to train from.")

	def clicked_esc50_dataset_checkbox(self):
		'''
		if esc50_dataset_checkbox is pressed on or off or if esc50_dataset_checkbox and recorded_audios_checkbox are pressed off:
			DISABLE 1 steps below : button_prepare_or_load_dataset.
			DISABLE and deselct 2 steps below : left side, right side.
			DISABLE 3-6 steps below : model info.
			DISABLE 7 steps below : button next.

			if esc50_dataset_checkbox is pressed on or off:
				ENABLE 1 step below : button_prepare_or_load_dataset.

		update_text_user_guide1.
		'''

		#if esc50_dataset_checkbox is pressed on or if esc50_dataset_checkbox and recorded_audios_checkbox are pressed off :
		if self.var_dataset_esc50.get() == 1 or self.var_dataset_esc50.get() == 0 or (self.var_dataset_esc50.get() == 0 and self.var_dataset_recorded_audios.get() == 0):

			#DISABLE 1 steps below : button_prepare_or_load_dataset
			self.button_prepare_or_load_dataset.config(state=tk.DISABLED)

			#DISABLE and deselct 2 steps below : left side, right side
			#DISABLE and deselct all left side
			self.checkbox_train_model.deselect()
			self.checkbox_train_model.config(state=tk.DISABLED)
			self.checkbox_save_model.deselect()
			self.checkbox_save_model.config(state=tk.DISABLED)
			self.entry_name_of_fitted_model_to_save.delete(0, tk.END)
			self.entry_name_of_fitted_model_to_save.config(state=tk.DISABLED)
			self.button_train_model.config(state=tk.DISABLED)
			#DISABLE and deselct all right side
			self.checkbox_load_model.deselect()
			self.checkbox_load_model.config(state=tk.DISABLED)
			self.button_browse_model.config(state=tk.DISABLED)

			#DISABLE 3-6 steps below : model info
			self.button_plot_model_accuracy.config(state=tk.DISABLED)
			self.button_plot_model_loss.config(state=tk.DISABLED)
			self.button_plot_confusion_matrix.config(state=tk.DISABLED)
			#clear canvas
			if self.color_bar_handle != "":
				self.color_bar_handle.remove()
				self.color_bar_handle = ""
			self.plot_model_analysys.cla()
			self.canvas_model_analysys.draw()
			#DISABLE button_clear_info
			self.button_clear_info.config(state=tk.DISABLED)

			#DISABLE 7 steps below : button next
			self.button_next.config(state=tk.DISABLED)

			if self.var_dataset_esc50.get() == 1 or self.var_dataset_esc50.get() == 0:
				#ENABLE 1 step below :button_prepare_or_load_dataset
				self.button_prepare_or_load_dataset.config(state=tk.NORMAL)

				#update_text_user_guide1
				self.update_text_user_guide(self.text_user_guide1,"Please click 'Prepare raw/Load dataset' button.")
		
			#if esc50_dataset_checkbox and recorded_audios_checkbox are pressed off :
			if self.var_dataset_esc50.get() == 0 and self.var_dataset_recorded_audios.get() == 0:

				#DISABLE 1 steps below : button_prepare_or_load_dataset
				self.button_prepare_or_load_dataset.config(state=tk.DISABLED)

				#update_text_user_guide1
				self.update_text_user_guide(self.text_user_guide1,"Please choose a dataset to train from.")

	def clicked_recorded_audios_dataset_checkbox(self):
		'''
		if checkbox_recorded_audios_dataset is pressed on or off or esc50_dataset_checkbox and recorded_audios_checkbox are pressed off:
			DISABLE 1 steps below : button_prepare_or_load_dataset.
			DISABLE and deselct 2 steps below : left side, right side.
			DISABLE 3-6 steps below : model info.
			DISABLE 7 steps below : button next.
			
			if checkbox_recorded_audios_dataset is pressed on or off:
				ENABLE 1 step below : button_prepare_or_load_dataset. 

		update_text_user_guide1.
		'''

		#if checkbox_recorded_audios_dataset is pressed on or if esc50_dataset_checkbox and recorded_audios_checkbox are pressed off :
		if self.var_dataset_recorded_audios.get() == 1 or self.var_dataset_recorded_audios.get() == 0 or (self.var_dataset_esc50.get() == 0 and self.var_dataset_recorded_audios.get() == 0):

			#DISABLE 1 steps below : button_prepare_or_load_dataset
			self.button_prepare_or_load_dataset.config(state=tk.DISABLED)

			#DISABLE and deselct 2 steps below : left side, right side
			#DISABLE and deselct all left side
			self.checkbox_train_model.deselect()
			self.checkbox_train_model.config(state=tk.DISABLED)
			self.checkbox_save_model.deselect()
			self.checkbox_save_model.config(state=tk.DISABLED)
			self.entry_name_of_fitted_model_to_save.delete(0, tk.END)
			self.entry_name_of_fitted_model_to_save.config(state=tk.DISABLED)
			self.button_train_model.config(state=tk.DISABLED)
			#DISABLE and deselct all right side
			self.checkbox_load_model.deselect()
			self.checkbox_load_model.config(state=tk.DISABLED)
			self.button_browse_model.config(state=tk.DISABLED)

			#DISABLE 3-6 steps below : model info
			self.button_plot_model_accuracy.config(state=tk.DISABLED)
			self.button_plot_model_loss.config(state=tk.DISABLED)
			self.button_plot_confusion_matrix.config(state=tk.DISABLED)
			#clear canvas
			if self.color_bar_handle != "":
				self.color_bar_handle.remove()
				self.color_bar_handle = ""
			self.plot_model_analysys.cla()
			self.canvas_model_analysys.draw()
			#DISABLE button_clear_info
			self.button_clear_info.config(state=tk.DISABLED)

			#DISABLE 7 steps below : button next
			self.button_next.config(state=tk.DISABLED)

			if self.var_dataset_recorded_audios.get() == 1  or self.var_dataset_recorded_audios.get() == 0:			
				#ENABLE 1 step below :button_prepare_or_load_dataset
				self.button_prepare_or_load_dataset.config(state=tk.NORMAL)

				#update_text_user_guide1
				self.update_text_user_guide(self.text_user_guide1,"Please click 'Prepare raw/Load dataset' button.")
		
			#if esc50_dataset_checkbox and recorded_audios_checkbox are pressed off :
			if self.var_dataset_esc50.get() == 0 and self.var_dataset_recorded_audios.get() == 0:
			
				#DISABLE 1 steps below : button_prepare_or_load_dataset
				self.button_prepare_or_load_dataset.config(state=tk.DISABLED)

				#update_text_user_guide1
				self.update_text_user_guide(self.text_user_guide1,"Please choose a dataset to train from.")

	def clicked_prepare_or_load_dataset_button(self):
		'''
		Prepare raw dataset/Load prepared dataset.
		Divide dataset to x_train ,x_test ,y_train ,y_test.
		build and compile model.                                       #NO - does overfitting!

		DISABLE button prepare_or_load_dataset.
		ENABLE 1 step below : checkbox_train_model, checkbox_load_model.
		update_text_user_guide1, update_command_view1.
		'''

		#Prepare raw dataset
		if self.var_prepare_or_load_dataset.get() == 1:
			self.np_arr_all_data ,self.np_arr_all_labels ,self.np_arr_all_numeric_labels, self.animals = prepare_datasets.prepare_datasets(Environmental_Sound_Classification_50=self.var_dataset_esc50.get(), Recorded_dataset=self.var_dataset_recorded_audios.get(), save_prepared_datasets_f=True)
		
		#Load prepared dataset
		elif self.var_prepare_or_load_dataset.get() == 2:
			self.np_arr_all_data ,self.np_arr_all_labels ,self.np_arr_all_numeric_labels, self.animals = load_prepared_datasets.load_prepared_datasets(Environmental_Sound_Classification_50=self.var_dataset_esc50.get(), Recorded_dataset=self.var_dataset_recorded_audios.get(), prepared_dataset_path=self.PREPARED_DATASETS_PATH)

		if len(self.animals) == 0 :
			self.message1 = messagebox.showinfo(title="Error", message="Please Prepare raw / Load prepared dataset that are not empty!")
			#DISABLE button prepare_or_load_dataset
			self.button_prepare_or_load_dataset.config(state=tk.DISABLED)
			return
			
		#DISABLE button prepare_or_load_dataset
		self.button_prepare_or_load_dataset.config(state=tk.DISABLED)

		#ENABLE 1 step below : checkbox_train_model, checkbox_load_model
		self.checkbox_train_model.config(state=tk.NORMAL)
		self.checkbox_load_model.config(state=tk.NORMAL)

		#update_text_user_guide1, update_command_view1
		self.update_text_user_guide(self.text_user_guide1,"Please choose: 'Train a deep learning model' / 'Load a trained deep learning model'.")
		self.update_command_view1()

#--------------------------------------------------------------

	def clicked_train_model_checkbox(self):
		'''
		if train_model_checkbox is pressed on : 
			ENABLE 1 and 3 steps below : checkbox_save_model, button_train_model.
			DISABLE "right side" : checkbox_load_model.
		else :
			DISABLE 1 ,2 and 3 steps below : "the left side".
			DISABLE 4-7 steps below : all frame of model info.
			DISABLE 8 steps below : button_next.
			ENABLE load checkbox.
		ENABLE/DISABLE checkboxes, buttons.
		update_text_user_guide1.
		'''

		#if train_model_checkbox is pressed on:
		if self.var_train_model.get() == 1:

			#ENABLE 1 and 3 steps below : checkbox_save_model, button_train_model
			self.checkbox_save_model.config(state=tk.NORMAL)
			self.button_train_model.config(state=tk.NORMAL)

			#DISABLE "right side" : checkbox_load_model
			self.checkbox_load_model.config(state=tk.DISABLED)

			#update_text_user_guide1
			self.update_text_user_guide(self.text_user_guide1,"Please choose rather to Save your trained model by setting 'Yes' in 'Save the trained model' checkbox/ Train model without saving by 'Train the model' button.")

		#if train_model_checkbox is pressed off:
		elif self.var_train_model.get() == 0:
			
			#DISABLE 1 ,2 and 3 steps below : "the left side"
			self.checkbox_save_model.deselect()
			self.checkbox_save_model.config(state=tk.DISABLED)
			self.entry_name_of_fitted_model_to_save.config(state=tk.NORMAL)
			self.entry_name_of_fitted_model_to_save.delete(0, tk.END)
			self.entry_name_of_fitted_model_to_save.config(state=tk.DISABLED)
			self.button_train_model.config(state=tk.DISABLED)

			#DISABLE 4-7 steps below : all frame of model info
			self.button_plot_model_accuracy.config(state=tk.DISABLED)
			self.button_plot_model_loss.config(state=tk.DISABLED)
			self.button_plot_confusion_matrix.config(state=tk.DISABLED)
			#clear canvas
			if self.color_bar_handle != "":
				self.color_bar_handle.remove()
				self.color_bar_handle = ""
			self.plot_model_analysys.cla()
			self.canvas_model_analysys.draw()
			#DISABLE button_clear_info
			self.button_clear_info.config(state=tk.DISABLED)

			#DISABLE 8 steps below : button_next
			self.button_next.config(state=tk.DISABLED)

			#ENABLE load model checkbox
			self.checkbox_load_model.config(state=tk.NORMAL)

			#update_text_user_guide1
			self.update_text_user_guide(self.text_user_guide1,"Please choose: 'Train a deep learning model' / 'Load a trained deep learning model'.")
			
	def clicked_save_model_checkbox(self):
		'''
		if save_model_checkbox is pressed on :
			ENABLE 1 step below : the entry textbox.
		else :
			DISABLE and delete 1 step below : the entry textbox.
		update_text_user_guide1.
		'''

		#If save_model_checkbox is pressed on:
		if self.var_save_fitted_model.get() == 1:

			#ENABLE 1 step below : the entry textbox
			self.entry_name_of_fitted_model_to_save.config(state=tk.NORMAL)

			#update_text_user_guide1
			self.update_text_user_guide(self.text_user_guide1,"Please enter trained model name to save with in 'Model name' entry.\nThen click 'Train the model!' button")

		#If save_model_checkbox is pressed off:
		else:

			#DISABLE and delete 1 step below : the entry textbox
			self.entry_name_of_fitted_model_to_save.delete(0, tk.END)
			self.entry_name_of_fitted_model_to_save.config(state=tk.DISABLED)

			#update_text_user_guide1
			self.update_text_user_guide(self.text_user_guide1,"Please select 'Yes' in 'Save the trained model' checkbox if you want save the trained model. Else, click 'Train the model!' button.")

	def clicked_train_model_button(self):
		'''
		Divide dataset to x_train ,x_test ,y_train ,y_test
		build and compile model.
		fit / fit and save.
		get name from entry of model name to save.
		if name wasnt entered correctly so pop an error message, else fit and save model in name = name(<1/2/3...>).
		print self.model.summary() , and model evaluation.
		DISABLE train model frame.
		ENABLE 1-4 steps below : all plots frame.
		ENABLE 5 step below : button_next.
		update_text_user_guide1, update_command_view1.
		'''

		if len(self.animals) == 0 or len(self.np_arr_all_labels) < 2 :
			self.message1 = messagebox.showinfo(title="Error", message="Please Prepare raw / Load prepared dataset that are not empty , or at least 2 sounds!")
			#DISABLE button prepare_or_load_dataset
			self.button_prepare_or_load_dataset.config(state=tk.DISABLED)
			return
			
		#Divide dataset to x_train ,x_test ,y_train ,y_test:
		self.x_train, self.x_test, self.y_train, self.y_test = divide_dataset.divide_dataset(self.np_arr_all_data, self.np_arr_all_numeric_labels)

		#get name from entry of model name to save
		name = self.var_name_of_fitted_model_to_save.get()

		#if name wasnt entered correctly pop an error message:
		if self.var_save_fitted_model.get() == 1 and name == '':
			self.message1 = messagebox.showinfo(title="Error", message="Please enter the name of your trained model!")
			return

		# Build and compile model
		self.INPUT_DIM = self.x_train.shape[1]
		self.N_CLASSES = len(self.animals)
		self.model = build_and_compile_model.build_and_compile_model(self.INPUT_DIM, self.N_CLASSES)

		#fit and save model in name = name(<1/2/3...>)
		self.model, self.history = fit_save_or_load_fitted_model.fit_save_or_load_fitted_model(self.model, False, name, self.x_train, self.y_train,self.x_test, self.y_test)
		
		#print self.model.summary() , and model evaluation
		print ("Model summary:")
		self.model.summary()
		print ("\n")
		model_evaluation.model_evaluation(self.model, self.x_test, self.y_test)
		
		#DISABLE train model frame
		self.button_train_model.config(state=tk.DISABLED)
		self.entry_name_of_fitted_model_to_save.config(state=tk.DISABLED)
		self.checkbox_save_model.config(state=tk.DISABLED)		
		
		#ENABLE 1-4 steps below : all plots frame
		self.button_plot_model_accuracy.config(state=tk.NORMAL)
		self.button_plot_model_loss.config(state=tk.NORMAL)
		self.button_plot_confusion_matrix.config(state=tk.NORMAL)
		#clear canvas
		if self.color_bar_handle != "":
			self.color_bar_handle.remove()
			self.color_bar_handle = ""
		self.plot_model_analysys.cla()
		self.canvas_model_analysys.draw()
		#DISABLE button_clear_info
		self.button_clear_info.config(state=tk.DISABLED)

		#ENABLE 5 step below : button_next
		self.button_next.config(state=tk.NORMAL)

		#update_text_user_guide1, update_command_view1
		self.update_text_user_guide(self.text_user_guide1,"Please now you can get your model analysis in 'Plot <...>' buttons. Else, To continue click 'Next' button.")
		self.update_command_view1()

#--------------------------------------------------------------			

	def clicked_load_model_checkbox(self):
		'''
		if load_model_checkbox is pressed on :
			ENABLE right side : browse button.
			DISABLE left side checkbox : checkbox_train_model.
		else:
			DISABLE 1 and 2 steps below : right side : both browse and load buttons.
			DISABLE 3-7 steps below : all frame of model info.
			DISABLE 8 steps below : button_next.
			ENABLE train checkbox.
		update_text_user_guide1.
		'''

		#if load_model_checkbox is pressed on:
		if self.var_load_model.get() == 1:

			#ENABLE right side : browse button
			self.button_browse_model.config(state=tk.NORMAL)
			
			#DISABLE left side checkbox : checkbox_train_model
			self.checkbox_train_model.config(state=tk.DISABLED)

			#update_text_user_guide1
			self.update_text_user_guide(self.text_user_guide1,"Please Browse a trained model by 'Browse' button.")

		#if load_model_checkbox is pressed off:
		elif self.var_load_model.get() == 0:
			
			#DISABLE 1 and 2 steps below : right side : both browse and load buttons
			self.button_browse_model.config(state=tk.DISABLED)
			self.button_load_model.config(state=tk.DISABLED)

			#DISABLE 3-7 steps below : all frame of model info
			self.button_plot_model_accuracy.config(state=tk.DISABLED)
			self.button_plot_model_loss.config(state=tk.DISABLED)
			self.button_plot_confusion_matrix.config(state=tk.DISABLED)
			#clear canvas
			if self.color_bar_handle != "":
				self.color_bar_handle.remove()
				self.color_bar_handle = ""
			self.plot_model_analysys.cla()
			self.canvas_model_analysys.draw()
			#DISABLE button_clear_info
			self.button_clear_info.config(state=tk.DISABLED)

			#DISABLE 8 steps below : button_next
			self.button_next.config(state=tk.DISABLED)

			# ENABLE train checkbox
			self.checkbox_train_model.config(state=tk.NORMAL)

			#update_text_user_guide1.
			self.update_text_user_guide(self.text_user_guide1,"Please choose: 'Train a deep learning model' / 'Load a trained deep learning model'.")

	def clicked_browse_model_button(self):
		'''
		first DISABLE button_load_model.
		ask .hdf5 file from "models" folder.
		if chose correctly so :
			load model (self.LOAD_MODEL_FILE_NAME = name of the model) DISABLE button_browse_model and ENABLE button_load_model.
		else:
			else pop error message! 
		update_text_user_guide1.
		'''

		#DISABLE button_load_model
		self.button_load_model.config(state=tk.DISABLED)

		path = os.path.join(os.getcwd(), "models")
		is_path = os.path.isdir(path)
		# if not is_path:
		# 	os.mkdir(path)
		if (not is_path) or (not os.listdir(path)):
			self.message1 = messagebox.showinfo(title="Error", message="There are no models available.")
			#DISABLE button_browse_model
			self.button_browse_model.config(state=tk.DISABLED)
			return

		#NOTE: filedialog.askopenfilename sometimes freeze python 3.8!
		self.LOAD_MODEL_FILE_NAME = filedialog.askopenfilename(title="Choose a model to open", initialdir=path, filetype = (("HDF5 files","*.hdf5"),))

		#check if model chose correctly, if yes so load model and ENABLE button_load_model, else pop error message! 
		path_to_file = '\\'.join(self.LOAD_MODEL_FILE_NAME.split('/')[:-1])
		if path_to_file == path:

			splitted_name = self.LOAD_MODEL_FILE_NAME.split('.')
			splitted_name.pop(-1)
			self.LOAD_MODEL_FILE_NAME = '.'.join(splitted_name)
			
			#self.LOAD_MODEL_FILE_NAME = name of loaded model
			self.LOAD_MODEL_FILE_NAME = self.LOAD_MODEL_FILE_NAME.split('/').pop(-1)
			
			#DISABLE button_browse_model
			self.button_browse_model.config(state=tk.DISABLED)

			#ENABLE 1 step below : button_load_model
			self.button_load_model.config(state=tk.NORMAL)

			#update_text_user_guide1
			self.update_text_user_guide(self.text_user_guide1,"Please click 'Load the model!' button")
		
		else:

			#if model wansnt chose correctly pop an error message:
			self.message1 = messagebox.showinfo(title="Error", message="Please browse model in 'models' path!")

	def clicked_load_model_button(self):
		'''
		Divide dataset to x_train ,x_test ,y_train ,y_test:
		build and compile model.
		load fitted model.
		print self.model.summary() , and model evaluation.
		DISABLE button_load_model.
		ENABLE 1 and 2 steps below : button_plot_confusion_matrix, button_next.
		update_text_user_guide1, update_command_view1.
		'''

		if len(self.animals) == 0 or len(self.np_arr_all_labels) < 2 :
			self.message1 = messagebox.showinfo(title="Error", message="Please Prepare raw / Load prepared dataset that are not empty , or at least 2 sounds!")
			#DISABLE button prepare_or_load_dataset
			self.button_prepare_or_load_dataset.config(state=tk.DISABLED)
			return
			
		#Divide dataset to x_train ,x_test ,y_train ,y_test:
		self.x_train, self.x_test, self.y_train, self.y_test = divide_dataset.divide_dataset(self.np_arr_all_data, self.np_arr_all_numeric_labels)
		
		# Build and compile model
		self.INPUT_DIM = self.x_train.shape[1]
		self.N_CLASSES = len(self.animals)
		self.model = build_and_compile_model.build_and_compile_model(self.INPUT_DIM, self.N_CLASSES)

		#load fitted model
		self.model, self.history = fit_save_or_load_fitted_model.fit_save_or_load_fitted_model(self.model, self.LOAD_MODEL_FILE_NAME, False, self.x_train, self.y_train, self.x_test, self.y_test)
		
		#print self.model.summary() , and model evaluation
		print ("Model summary:")
		self.model.summary()
		print ("\n")
		model_evaluation.model_evaluation(self.model, self.x_test, self.y_test)

		#DISABLE button_load_model
		self.button_load_model.config(state=tk.DISABLED)

		#ENABLE 1 and 2 steps below : button_plot_confusion_matrix, button_next
		self.button_plot_confusion_matrix.config(state=tk.NORMAL)
		self.button_next.config(state=tk.NORMAL)

		#update_text_user_guide1, update_command_view1
		self.update_text_user_guide(self.text_user_guide1,"Please now you can get your model analysis in 'Plot <...>' buttons. Else, To continue click 'Next' button.")
		self.update_command_view1()

#--------------------------------------------------------------

	def clicked_plot_model_accuracy_button(self):
		'''
		clear canvas.
		draw plot model accuracy.
		ENABLE 1 step below : button_clear_info.
		update_text_user_guide1, update_command_view1.
		'''

		#clear canvas
		if self.button_clear_info["state"] == 'normal' :
			if self.color_bar_handle != "":
				self.color_bar_handle.remove()
				self.color_bar_handle = ""
			self.plot_model_analysys.cla()
			self.canvas_model_analysys.draw()

		#draw plot model accuracy
		self.color_bar_handle = analyze_model.model_analysys(self.model, self.x_test, self.y_test, self.history, self.animals, self.fig_model_analysys, self.plot_model_analysys, True, False, False)
		self.canvas_model_analysys.draw()

		#ENABLE 1 step below : button_clear_info
		self.button_clear_info.config(state=tk.NORMAL)

		#update_text_user_guide1, update_command_view1
		self.update_text_user_guide(self.text_user_guide1,"Please now you can get your model analysis in 'Plot <...>' buttons. You can Clear info by click 'Clear Info' button. To continue click 'Next' button.")
		self.update_command_view1()

	def clicked_plot_model_loss_button(self):
		'''
		clear canvas.
		draw plot model loss.
		ENABLE 1 step below : button_clear_info.
		update_text_user_guide1, update_command_view1.
		'''

		#clear canvas
		if self.button_clear_info["state"] == 'normal' :
			if self.color_bar_handle != "":
				self.color_bar_handle.remove()
				self.color_bar_handle = ""
			self.plot_model_analysys.cla()
			self.canvas_model_analysys.draw()

		#draw plot model loss
		self.color_bar_handle = analyze_model.model_analysys(self.model, self.x_test, self.y_test, self.history, self.animals, self.fig_model_analysys, self.plot_model_analysys, False, True, False)
		self.canvas_model_analysys.draw()

		#ENABLE 1 step below : button_clear_info
		self.button_clear_info.config(state=tk.NORMAL)

		#update_text_user_guide1, update_command_view1
		self.update_text_user_guide(self.text_user_guide1,"Please now you can get your model analysis in 'Plot <...>' buttons. You can Clear info by click 'Clear Info' button. To continue click 'Next' button.")
		self.update_command_view1()

	def clicked_plot_confusion_matrix_button(self):
		'''
		clear canvas.
		draw plot model confusion matrix.
		ENABLE 1 step below : button_clear_info.
		update_text_user_guide1, update_command_view1.
		'''

		#clear canvas
		if self.button_clear_info["state"] == 'normal' :
			if self.color_bar_handle != "":
				self.color_bar_handle.remove()
				self.color_bar_handle = ""
			self.plot_model_analysys.cla()
			self.canvas_model_analysys.draw()

		#draw plot model confusion matrix
		self.color_bar_handle = analyze_model.model_analysys(self.model, self.x_test, self.y_test, self.history, self.animals, self.fig_model_analysys, self.plot_model_analysys, False, False, True)
		self.canvas_model_analysys.draw()

		#ENABLE 1 step below : button_clear_info
		self.button_clear_info.config(state=tk.NORMAL)

		#update_text_user_guide1, update_command_view1
		self.update_text_user_guide(self.text_user_guide1,"Please now you can get your model analysis in 'Plot <...>' buttons. You can Clear info by click 'Clear Info' button. To continue click 'Next' button.")
		self.update_command_view1()

	def clicked_clear_info_button(self):
		'''
		clear canvas.
		DISABLE button_clear_info.
		update_text_user_guide1, update_command_view1.
		'''

		#clear canvas
		if self.color_bar_handle != "":
			self.color_bar_handle.remove()
			self.color_bar_handle = ""
		self.plot_model_analysys.cla()
		self.canvas_model_analysys.draw()

		#DISABLE button_clear_info
		self.button_clear_info.config(state=tk.DISABLED)

		#update_text_user_guide1, update_command_view1
		self.update_text_user_guide(self.text_user_guide1,"Please now you can get your model analysis in 'Plot <...>' buttons. To continue click 'Next' button.")
		self.update_command_view1()

	def clicked_next_button(self):
		'''
		make first window "Invisible" , and second window "Visible" and lift it.
		reset_command_view_string.
		'''
		# Make first window "Invisible"
		self.firstwindow.state("withdrawn")

		# Make second window "Visible" and lift it
		self.secondwindow.state("normal")
		self.secondwindow.lift()

		#reset_command_view_string
		self.reset_command_view_string()

	def clicked_clear_command_view1_button(self):
		'''
		clear command view1.
		'''

		self.reset_command_view_string()
		self.text_command_view1.config(state=tk.NORMAL)
		self.text_command_view1.delete('0.0', tk.END)
		self.text_command_view1.config(state=tk.DISABLED)

#--------------------------------------------------------------------------------------------
	# Second window methods

	def clicked_record_audio_checkbox(self):
		'''
		if record_audio_checkbox is pressed on:
			ENABLE the record button.
			DISABLE load audio checkbox.
		else:
			DISABLE 1 step below : all the left side.
			DISABLE 2,3,4,5 steps below : all frame of Analyze and Save audio.
			RESET all prediction info frame.
			ENABLE load audio checkbox.
		update_text_user_guide2.
		'''

		#if record_audio_checkbox is pressed on:
		if self.var_record_audio.get() == 1:

			#ENABLE the record button
			self.button_record.config(state=tk.NORMAL)

			#DISABLE load audio checkbox
			self.checkbox_load_audio.config(state=tk.DISABLED)

			#update_text_user_guide2
			self.update_text_user_guide(self.text_user_guide2,"Please click 'Record' button.")
		
		#if record_audio_checkbox is pressed off:
		else:

			#DISABLE 1 step below : all the left side
			self.button_record.config(state=tk.DISABLED)
			
			#DISABLE 2,3,4,5 steps below : all frame of Analyze and Save audio
			self.button_play_sound.config(state=tk.DISABLED)
			self.button_predict.config(state=tk.DISABLED)
			self.checkbox_set_audio_feedback.deselect()
			self.checkbox_set_audio_feedback.config(state=tk.DISABLED)
			self.button_set_audio_feedback.config(state=tk.DISABLED)

			#RESET all prediction info frame:
			self.plot_probabilities_bar_graph.cla()
			self.canvas_probabilities_bar_graph.draw()
			self.text_animal_info.config(state=tk.NORMAL)
			self.text_animal_info.delete(0.0, tk.END)
			self.text_animal_info.config(state=tk.DISABLED)
			self.plot_animal_image.cla()
			self.canvas_animal_image.draw()
			
			#ENABLE load audio checkbox
			self.checkbox_load_audio.config(state=tk.NORMAL)

			#update_text_user_guide2
			self.update_text_user_guide(self.text_user_guide2,"Please choose: 'Record your own audio using a microphon' / 'Load an audio sample'.")

	def clicked_record_audio_button(self):
		'''
		DISABLE button_play_sound and button_predict.
		record audio and put it in file = os.path.join(os.getcwd(),relative_path) . relative_path = os.path.join(self.SAVE_RECORDS_TMP_PATH , self.RECORD_TMP_NAME) + '.wav' .
		fname = recorded audio.
		DISABLE button_record.
		ENABLE 1 and 2 steps: button_play_sound and button_predict.
		update_text_user_guide2, update_command_view2.
		'''

		#DISABLE button_play_sound and button_predict
		self.button_play_sound.config(state=tk.DISABLED)
		self.button_predict.config(state=tk.DISABLED)

		#record audio and put it in file = os.path.join(os.getcwd(),relative_path) . relative_path = os.path.join(self.SAVE_RECORDS_TMP_PATH , self.RECORD_TMP_NAME) + '.wav'
		audio_from_mic.audio_from_mic_5_sec(self.SAVE_RECORDS_TMP_PATH,self.RECORD_TMP_NAME)
		relative_path = os.path.join(self.SAVE_RECORDS_TMP_PATH , self.RECORD_TMP_NAME) + '.wav'
		#fname = recorded audio
		self.fname = os.path.join(os.getcwd(),relative_path)

		#DISABLE button_record
		self.button_record.config(state=tk.DISABLED)

		#ENABLE 1 and 2 steps: button_play_sound and button_predict
		self.button_play_sound.config(state=tk.NORMAL)
		self.button_predict.config(state=tk.NORMAL)

		#update_text_user_guide2, update_command_view2.
		self.update_text_user_guide(self.text_user_guide2, "Please click 'Play audio' button to play the audio, or click 'Predict' button to get predicion analysis.")
		self.update_command_view2()

#--------------------------------------------------------------
	
	def clicked_load_audio_checkbox(self):
		'''
		if load_audio_checkbox is pressed on:
			ENABLE the browse button.
			DISABLE record audio checkbox.
		else:
			DISABLE all the right side.
			DISABLE 2,3,4,5 steps below : all frame of Analyze and Save audio.
			RESET all prediction info frame.
			ENABLE record audio checkbox.
		update_text_user_guide2.
		'''

		#if load_audio_checkbox is pressed on:
		if self.var_load_audio.get() == 1:

			#ENABLE the browse button
			self.button_browse_audio.config(state=tk.NORMAL)

			#DISABLE record audio checkbox
			self.checkbox_record_audio.config(state=tk.DISABLED)
			
			#update_text_user_guide2
			self.update_text_user_guide(self.text_user_guide2,"Please Browse an audio sample by 'Browse' button.")

		#if load_audio_checkbox is pressed off:
		else:

			#DISABLE all the right side
			self.button_browse_audio.config(state=tk.DISABLED)

			#DISABLE 2,3,4,5 steps below : all frame of Analyze and Save audio
			self.button_play_sound.config(state=tk.DISABLED)
			self.button_predict.config(state=tk.DISABLED)
			self.checkbox_set_audio_feedback.deselect()
			self.checkbox_set_audio_feedback.config(state=tk.DISABLED)
			self.button_set_audio_feedback.config(state=tk.DISABLED)

			#RESET all prediction info frame:
			self.plot_probabilities_bar_graph.cla()
			self.canvas_probabilities_bar_graph.draw()
			self.text_animal_info.config(state=tk.NORMAL)
			self.text_animal_info.delete(0.0, tk.END)
			self.text_animal_info.config(state=tk.DISABLED)
			self.plot_animal_image.cla()
			self.canvas_animal_image.draw()
			
			#ENABLE record audio checkbox
			self.checkbox_record_audio.config(state=tk.NORMAL)

			#update_text_user_guide2
			self.update_text_user_guide(self.text_user_guide2,"Please choose: 'Record your own audio using a microphon' / 'Load an audio sample'.")

	def clicked_browse_audio_button(self):
		'''
		make sure self.SAVE_RECORDS_TMP_PATH folder is exist for saving file there.
		copy audio file to SAVE_RECORDS_TMP_PATH in name RECORD_TMP_NAME.wav and load it to self.fname.
		DISABLE button_browse_audio.
		ENABLE 1 and 2 steps below : button_play_sound, button_predict.
		update_text_user_guide2, update_command_view2.
		'''

		print("Browse an audio sample.")

		path = os.path.join(os.getcwd(), "animals_sounds")
		is_path = os.path.isdir(path)
		if not is_path:
			path=os.getcwd()

		#make sure self.SAVE_RECORDS_TMP_PATH folder is exist for saving file there
		tmp_recorded_audio_folder_path = os.path.join(os.getcwd() ,self.SAVE_RECORDS_TMP_PATH)
		if not os.path.isdir(tmp_recorded_audio_folder_path):
			os.mkdir(tmp_recorded_audio_folder_path)

		#NOTE: filedialog.askopenfilename sometimes freeze python 3.8!
		audio_file = filedialog.askopenfilename(title="Choose an audio sample to open", initialdir=path, filetype = (("WAV files","*.wav"),))
		
		#copy audio file to SAVE_RECORDS_TMP_PATH in name RECORD_TMP_NAME.wav and load it to self.fname
		tmp_file_relative_path = os.path.join(self.SAVE_RECORDS_TMP_PATH, self.RECORD_TMP_NAME) +'.wav'
		tmp_file = os.path.join(os.getcwd(), tmp_file_relative_path)
		shutil.copyfile(audio_file, tmp_file)
		self.fname=tmp_file

		print("Done browse an audio sample.\n")
		
		#DISABLE button_browse_audio
		self.button_browse_audio.config(state=tk.DISABLED)

		#ENABLE 1 and 2 steps below : button_play_sound, button_predict
		self.button_play_sound.config(state=tk.NORMAL)
		self.button_predict.config(state=tk.NORMAL)

		#update_text_user_guide2, update_command_view2
		self.update_text_user_guide(self.text_user_guide2, "Please click 'Play audio' button to play the audio, or click 'Predict' button to get predicion analysis.")
		self.update_command_view2()

#--------------------------------------------------------------

	def clicked_play_audio_button(self):
		'''
		Play sound of file = self.fname
		update_text_user_guide2 , update_command_view2.
		'''
		print("play the audio sample.")

		#playsound(self.fname) #sometimes dont work!(bug in this library, "Error 275 for command: open <path> alias playsound_<...> Cannot find the specified file.  Make sure the path and filename are correct.")
		audio = AudioSegment.from_wav(self.fname)
		play(audio)

		print("Done play the audio sample.\n")

		#update_text_user_guide2
		self.update_text_user_guide(self.text_user_guide2, "Please click 'Predict' button to get predicion analysis.")
		self.update_command_view2()

	def clicked_predict_button(self):
		'''
		reset all plots.
		extract features of self.fname , then get predicting on it, show probabilities_bar_graph.
		if probability_array_percentages[predicted_index] >= self.PROBABILITY_TRESHOLD , so get animal info .
		DISABLE button_predict.
		ENABLE 1 step below : checkbox_set_audio_feedback.
		update_text_user_guide2, update_command_view2.
		'''

		#reset all plots
		self.plot_probabilities_bar_graph.cla()
		self.canvas_probabilities_bar_graph.draw()
		self.text_animal_info.config(state=tk.NORMAL)
		self.text_animal_info.delete(0.0, tk.END)
		self.text_animal_info.config(state=tk.DISABLED)
		self.plot_animal_image.cla()
		self.canvas_animal_image.draw()

		#extract features of self.fname , then get predicted_index , self.predicted_animal , probability_array_percentages by predict method
		features = extract_features.extract_features_from_1wav_file(self.fname)
		predicted_index , self.predicted_animal , probability_array_percentages = predict.predict_input_features(self.model , features , self.animals)
		
		#create plot probabilities_bar_graph and draw it
		predict.show_probabilities_hist(self.animals , probability_array_percentages, self.fig_probabilities_bar_graph, self.plot_probabilities_bar_graph)
		self.canvas_probabilities_bar_graph.draw()

		#if probability_array_percentages[predicted_index] >= self.PROBABILITY_TRESHOLD , so get animal info .
		if probability_array_percentages[predicted_index] >= self.PROBABILITY_TRESHOLD:
			
			print ("The model is {}% sure that the sound heard is from a {}\n".format(probability_array_percentages[predicted_index], self.predicted_animal))
			
			#get animal_info_text , insert it to text_animal_info .
			self.animal_info_text = animal_info.get_animal_info(self.predicted_animal, self.fig_animal_image, self.plot_animal_image)
			self.text_animal_info.config(state=tk.NORMAL)
			self.text_animal_info.insert(tk.END, self.animal_info_text)
			self.text_animal_info.config(state=tk.DISABLED)
			#create plot animal_image and draw it
			self.canvas_animal_image.draw()

		else :

			print ("The model is not sure which animal it is")

		#DISABLE button_predict
		self.button_predict.config(state=tk.DISABLED)

		#ENABLE 1 step below : checkbox_set_audio_feedback
		self.checkbox_set_audio_feedback.config(state=tk.NORMAL)

		#update_text_user_guide2, update_command_view2
		self.update_text_user_guide(self.text_user_guide2, "You can see now the prediction result. Now you can Save the audio sample , to do that click 'Yes' in 'Save the audio' checkbox.")
		self.update_command_view2()

	def clicked_set_recorded_audio_feedback_checkbox(self):
		'''
		if set_audio_feedback is pressed on :
			ENABLE 1 step below : button_set_audio_feedback.
		else :
			DISABLE 1 step below : button_set_audio_feedback
		update_text_user_guide2. 
		'''

		#if set_audio_feedback is pressed on:
		if self.var_set_audio_feedback.get() == 1:

			#ENABLE button_set_audio_feedback		
			self.button_set_audio_feedback.config(state=tk.NORMAL)

			#update_text_user_guide2
			self.update_text_user_guide(self.text_user_guide2,"Please enter audio sample name to save with in 'Recording name' entry.\nThen click 'Save audio' button.")
		
		else:

			#DISABLE button_set_audio_feedback
			self.button_set_audio_feedback.config(state=tk.DISABLED)

			#update_text_user_guide2
			self.update_text_user_guide(self.text_user_guide2,"Please select 'Yes' in 'save the audio' checkbox if you want save the audio sample.")

	def clicked_set_audio_feedback_button(self):
		'''
		set feedback to audio file. 	
		DISABLE every checkboxex, entries, and buttons and reset plots . (reset all second page).
		reset all plots.
		update_text_user_guide2, update_command_view2.
		'''

		print("Set audio sample feedback.")

		#make sure self.RECORDED_AUDIOS_DATASET_NAME exist
		dst_wav_file = os.path.join(os.getcwd(), self.DATASETS_PATH)
		dst_wav_file = os.path.join(dst_wav_file, self.RECORDED_AUDIOS_DATASET_NAME)
		is_path = os.path.isdir(dst_wav_file)
		if not is_path:
			os.mkdir(dst_wav_file)

		src_wav_file = self.fname
		dst_animals_info_path = os.path.join(os.getcwd(), self.ANIMALS_INFO_PATH)
		dst_info_txt_path =  os.path.join(dst_animals_info_path, self.ANIMALS_INFO_TXT_PATH)
		dst_info_image_path = os.path.join(dst_animals_info_path, self.ANIMALS_INFO_IMAGE_PATH)

		self.thirdwindow = tk.Toplevel(self.secondwindow)
		self.thirdwindow.state("withdrawn")		

		Feedback(self.thirdwindow, self.animals, src_wav_file, dst_wav_file, dst_info_txt_path, dst_info_image_path)
		
		self.thirdwindow.state("normal")
		self.thirdwindow.lift()

		#DISABLE every checkboxex, entries, and buttons . (reset second page)
		self.button_set_audio_feedback.config(state=tk.DISABLED)
		self.checkbox_set_audio_feedback.deselect()
		self.checkbox_set_audio_feedback.config(state=tk.DISABLED)
		self.button_predict.config(state=tk.DISABLED)
		self.button_play_sound.config(state=tk.DISABLED)
		self.button_browse_audio.config(state=tk.DISABLED)
		self.button_record.config(state=tk.DISABLED)

		#reset all plots
		self.plot_probabilities_bar_graph.cla()
		self.canvas_probabilities_bar_graph.draw()
		self.text_animal_info.config(state=tk.NORMAL)
		self.text_animal_info.delete(0.0, tk.END)
		self.text_animal_info.config(state=tk.DISABLED)
		self.plot_animal_image.cla()
		self.canvas_animal_image.draw()

		print("Done set audio sample feedback.")

		#update_text_user_guide2, update_command_view2
		self.update_text_user_guide(self.text_user_guide2,"Please choose: 'Record your own audio using a microphon' / 'Load an audio sample'.")
		self.update_command_view2()

#--------------------------------------------------------------

	def clicked_previous_button(self):
		'''
		make second window "Invisible" , and first window "Visible" and lift it.
		reset_command_view_string.
		'''

		# Make second window "Invisible"
		self.secondwindow.state("withdrawn")

		# Make first window "visible"
		self.firstwindow.state("normal")
		self.firstwindow.lift()

		self.reset_command_view_string()

	def clicked_clear_command_view2_button(self):
		'''
		clear command view1.
		'''

		self.reset_command_view_string()
		self.text_command_view2.config(state=tk.NORMAL)
		self.text_command_view2.delete('0.0', tk.END)
		self.text_command_view2.config(state=tk.DISABLED)

#--------------------------------------------------------------
#Other methods:

	def update_command_view1(self):
		'''
		update command view1.
		'''

		self.text_command_view1.config(state=tk.NORMAL)
		self.text_command_view1.delete('0.0', tk.END)
		self.text_command_view1.insert(tk.END, self.command_view_string.getvalue())
		self.text_command_view1.see(tk.END)
		self.text_command_view1.config(state=tk.DISABLED)

	def update_command_view2(self):
		'''
		update command view2.
		'''

		self.text_command_view2.config(state=tk.NORMAL)
		self.text_command_view2.delete('0.0', tk.END)
		self.text_command_view2.insert(tk.END, self.command_view_string.getvalue())
		self.text_command_view2.see(tk.END)
		self.text_command_view2.config(state=tk.DISABLED)

	def reset_command_view_string(self):
		'''
		reset command_view_string.
		'''

		self.command_view_string.close()
		self.command_view_string = StringIO()
		sys.stdout = self.command_view_string

	def update_text_user_guide(self, text_widget, string):
		'''
		get text_widget and update it with string.
		'''

		text_widget.config(state=tk.NORMAL)
		text_widget.delete('0.0', tk.END)
		text_widget.insert(tk.END, string)
		text_widget.config(state=tk.DISABLED)

#-----------------------------------------------------------------------------------------------------------------
# Main

def on_closing():
	'''
	on closing (pressed X on firstwindow/secondwindow) - delete tmp_recorded_audio folder and all files in it
	'''
	tmp_recorded_audio_folder = os.path.join(os.getcwd() ,'tmp_recorded_audio')
	if os.path.isdir(tmp_recorded_audio_folder):
		shutil.rmtree(tmp_recorded_audio_folder)
	exit()

if __name__=="__main__":

	window = tk.Tk()

	window.title('GUI Application For Final Project')

	e = App(window)

	e.firstwindow.protocol("WM_DELETE_WINDOW", on_closing)

	e.secondwindow.protocol("WM_DELETE_WINDOW", on_closing)

	window.mainloop()
