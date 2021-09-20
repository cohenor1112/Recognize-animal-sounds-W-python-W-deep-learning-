import os

import importlib
try:
	importlib.import_module('tensorflow')
except ImportError:
	os.system('pip install tensorflow')
try:
	importlib.import_module('pandas')
except ImportError:
	os.system('pip install pandas')
try:
	importlib.import_module('librosa')
except ImportError:
	os.system('pip install librosa')
try:
	importlib.import_module('matplotlib')
except ImportError:
	os.system('pip install matplotlib')
try:
	importlib.import_module('pyaudio')
except ImportError:
	os.system('pip install pipwin')
	os.system('pipwin install pyaudio')
try:
	importlib.import_module('playsound')
except ImportError:
	os.system('pip install playsound')