import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import shutil


class Feedback:

	def __init__(self, master, animals, src_wav_file, dst_wav_file, dst_info_txt_file, dst_info_png_file):

		self.window = master

#----------------------------------------------------------------------------------------------
#variables:
		self.animals = animals
		self.src_wav_file = src_wav_file
		self.dst_wav_file = dst_wav_file
		self.dst_info_text_file = dst_info_txt_file
		self.dst_info_png_file = dst_info_png_file

		self.var_selection = tk.IntVar()
		self.var_selection.set(-1)
		self.var_name = tk.StringVar()

		self.name_to_save = ""
		self.image_file = ""
#----------------------------------------------------------------------------------------------
#frame 1:

		self.frame_predefined_animals = tk.LabelFrame(self.window, text="Choose an animal :")
		self.frame_predefined_animals.grid(row=0, padx=5, pady=5)

#radiobuttons in frame 1:

		self.animals_len = len(self.animals)

		if self.animals_len == 1:
			self.columns = 1
		else:
			self.columns = self.animals_len - 1

		for item in enumerate(self.animals):

			radiobutton_animal = tk.Radiobutton(self.frame_predefined_animals, text=item[1], variable=self.var_selection, value=item[0], command=self.clicked_predefined_animals_radiobuttons)
			radiobutton_animal.grid(row=0, column=item[0], padx=5, pady=5, sticky=tk.W)

#----------------------------------------------------------------------------------------------
#frame 2:
		self.frame_other_animal = tk.LabelFrame(self.window, text="Other animal :")
		self.frame_other_animal.grid(row=1, padx=5, pady=5)

#Buttons and widgets in frame 2

		self.radiobutton_other = tk.Radiobutton(self.frame_other_animal, text="Other", variable=self.var_selection, value=self.animals_len, command=self.clicked_other_radiobutton)
		self.radiobutton_other.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

		self.label_name = tk.Label(self.frame_other_animal, text="Name")
		self.label_name.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

		self.entry_name = tk.Entry(self.frame_other_animal, textvariable=self.var_name, state=tk.DISABLED)
		self.entry_name.grid(row=1, column=1, columnspan=self.columns, padx=5, pady=5, sticky=tk.W)

		self.label_info_text = tk.Label(self.frame_other_animal, text="Info")
		self.label_info_text.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

		self.text_info = tk.Text(self.frame_other_animal, height=3, state=tk.DISABLED)
		self.text_info.grid(row=2, column=1, columnspan=self.columns, padx=5, pady=5, sticky=tk.W)

		self.label_image = tk.Label(self.frame_other_animal, text="Image")
		self.label_image.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

		self.button_image_browse = tk.Button(self.frame_other_animal, text="Browse", state=tk.DISABLED, command=self.clicked_browse_button)
		self.button_image_browse.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

#----------------------------------------------------------------------------------------------

# Buttons outside of any frame

		self.button_save_feedback = tk.Button(self.window, text="Save feedback", state=tk.DISABLED, command=self.clicked_save_feedback_button)
		self.button_save_feedback.grid(row=2, padx=5, pady=5)

#----------------------------------------------------------------------------------------------
#methods:

#methods of frame 1:

	def clicked_predefined_animals_radiobuttons(self):
		#enable/disable
		
		self.entry_name.config(state=tk.DISABLED)
		self.text_info.config(state=tk.DISABLED)
		self.button_image_browse.config(state=tk.DISABLED)

		self.button_save_feedback.config(state=tk.NORMAL)

#----------------------------------------------------------------------------------------------

#methods of frame 2:

	def clicked_other_radiobutton(self):
		#enable/disable

		self.entry_name.config(state=tk.NORMAL)
		self.text_info.config(state=tk.NORMAL)
		self.button_image_browse.config(state=tk.NORMAL)
		self.button_save_feedback.config(state=tk.NORMAL)


	def clicked_browse_button(self):
		
		self.image_file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select an image", filetype = (("PNG files","*.png"),))

#----------------------------------------------------------------------------------------------

#methods of outside frame:

	def clicked_save_feedback_button(self):

		#predifined animals	
		if self.var_selection.get() != self.animals_len:

			self.name_to_save = self.animals[self.var_selection.get()]

		#other animal
		else:
			
			#name entered not correctly
			if self.entry_name.get() == "" :

				self.message1 = messagebox.showinfo(title="Error", message="Please enter the name of your animal")
				return

			#name entered correctly
			self.name_to_save = self.entry_name.get()

			#save txt file
			if self.text_info.get("0.0", tk.END) != False :
				
				txt_file_full_path = os.path.join (self.dst_info_text_file, self.name_to_save)+'.txt'
				with open(txt_file_full_path, "w") as output:
					output.write(self.text_info.get("0.0", tk.END))
				print("{} was made and saved in {}.".format(self.name_to_save+".txt", self.dst_info_text_file))

			#save png file
			if self.image_file != '' :
				image_file_full_path= os.path.join(self.dst_info_png_file, self.name_to_save)+'.png'
				shutil.copyfile(self.image_file, image_file_full_path)
				print("{} was imported and saved in {}.".format(self.name_to_save+".png",self.dst_info_png_file))

		#make valid name to save
		self.save_in_name() # renames the file and puts -1, -2 at the end

		#copy .wav file
		wav_file_full_path = os.path.join(self.dst_wav_file, self.name_to_save)+'.wav'
		shutil.copyfile(self.src_wav_file, wav_file_full_path)

		print("Done save audio sample in name : {}, in {}.\n".format(self.name_to_save, self.dst_wav_file))

		self.button_save_feedback.config(state=tk.DISABLED)

		self.window.destroy()


	def save_in_name(self):
		#name => name-<1/2/3...> if name was already exist

		counter = 1
		while (str(self.name_to_save) + '-' + str(counter) + '.wav') in os.listdir(self.dst_wav_file):
			counter += 1
		self.name_to_save = str(self.name_to_save) + '-' + str(counter)


################################################################################################################

if __name__ == "__main__":

	root = tk.Tk()

	root.title("Feedback window")

	l = ["Dog"]

	src_wav_file = os.path.join(os.getcwd(), "folder")
	src_wav_file = os.path.join(src_wav_file, "cow-2") + ".wav"
	
	dst_wav_file = os.getcwd()
	
	dst_info_txt_file = os.getcwd()

	dst_info_png_file = os.getcwd()

	e = Feedback(root, l, src_wav_file, dst_wav_file, dst_info_txt_file, dst_info_png_file)

	root.mainloop()
