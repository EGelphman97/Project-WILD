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
from gpio_96boards import GPIO

def record(gpio):
	if gpio.digital_read(recbut) == 1:
		gpio.digital_write(recled, GPIO.HIGH)
		
		config = { 
			"database": {
				"host": "127.0.0.1",
				"user": "root",
				"passwd": "",
				"db": "dejavu",
			},
			"database_type" : "mysql",
		}
		
		pR = pyaudio.PyAudio()
		
		stream = pR.open(format=FORMAT,
		                channels=CHANNELS,
		                rate=RATE,
		                input=True,
		                frames_per_buffer=CHUNK)
		
		print("* recording")
		
		framesR = []
		
		while gpio.digital_read(recbut) == 1:
		    dataR = stream.read(CHUNK)
		    framesR.append(dataR)
		
		print("* done recording")
		
		stream.stop_stream()
		stream.close()
		pR.terminate()
		
		wf = wave.open("train/rec.wav", 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(pR.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(framesR))
		wf.close()
		
		djvR = Dejavu(config)
		djvR.fingerprint_directory("train", [".wav"])
	
		gpio.digital_write(recled, GPIO.LOW)


def activate(gpio):
	if gpio.digital_read(actbut) == 1:
		gpio.digital_write(actled, GPIO.LOW)
		micON1 = False
	else:
		micON1 = True
		gpio.digital_write(actled, GPIO.HIGH)
	return micON1



if __name__ == '__main__':

	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 11000
	SIZE = 80

	recbut = GPIO.gpio_id('GPIO_A') # GPIO_36, pin = 23
	actbut = GPIO.gpio_id('GPIO_B') # GPIO_12, pin = 24
	recled = GPIO.gpio_id('GPIO_C') # GPIO_13, pin = 25
	actled = GPIO.gpio_id('GPIO_D') # GPIO_69, pin = 26
	pins = ((recbut, 'in'), (actbut, 'in'), (recled, 'out'), (actled, 'out'))

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
		        channels=CHANNELS,
		        rate=RATE,
		        input=True,
		        frames_per_buffer=CHUNK)

	print("* listening")
	frames = deque()
	WAVE_OUTPUT_FILENAME = ""
	num = 0
	count = 0
	micON = True

	while True:
		#RECORD CHECK
		with GPIO(pins) as gpio:
			record(gpio)
			micON = activate(gpio)
		#print(micON)
		data = stream.read(CHUNK)
		frames.append(data)
		count +=1
		if len(frames) > SIZE:
			frames.popleft()

		if (count % 10 == 0) & micON:
			WAVE_OUTPUT_FILENAME = "%d.wav" % num
			print(WAVE_OUTPUT_FILENAME)
			wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
			wf.setnchannels(CHANNELS)
			wf.setsampwidth(2)
			wf.setframerate(RATE)
			wf.writeframes(b''.join(frames))
			wf.close()
			num += 1
			if num == 5:
				num = 0

	stream.stop_stream()
	stream.close()
	p.terminate()