import pyaudio
import wave
import os
import numpy as np
import time
import warnings
import cPickle as pickle
warnings.filterwarnings("ignore")
from collections import deque
import collections
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

if __name__ == '__main__':

	config = {
		"database": {
			"host": "127.0.0.1",
			"user": "root",
			"passwd": "",
			"db": "dejavu",
		},
		"database_type" : "mysql",
	}

	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 11000
	SIZE = 80

	p = pyaudio.PyAudio()
	djv = Dejavu(config)

	print("* analyzing")
	frames = deque()
	WAVE_OUTPUT_FILENAME = ""
	num = 0

	while True:
		WAVE_OUTPUT_FILENAME = "%d.wav" % num
		print(WAVE_OUTPUT_FILENAME)
		# Recognize audio from a file
		print "From file we recognized: %s\n" % djv.recognize(FileRecognizer, WAVE_OUTPUT_FILENAME)
		num += 1
		if num == 10:
			num = 0
