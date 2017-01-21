import pyaudio
import wave
from dejavu import Dejavu

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 11000
RECORD_SECONDS = 4

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

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
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

