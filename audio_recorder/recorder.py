import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

class AudioRecorder:
    def __init__(self,samplerate=44100, filename="output.wav"):
        self.samplerate = samplerate
        self.filename = filename
        self._recording_data = []
        self._stream = None
    
    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self._recording_data.append(indata.copy())

    def record(self):
        self._recording_data = []
        self._stream = sd.InputStream(samplerate=self.samplerate, channels=1, dtype='int16', callback=self._callback)
        self._stream.start()
        print("Recording started...")
    
    def stop(self):
        if self._stream is None:
            print("No active recording to stop")
            return
        
        self._stream.stop()
        self._stream.close()
        self._stream = None
        print("Recording stopped.")

        if not self._recording_data:
            print("no data recorded")
            return
        
        recording = np.concatenate(self._recording_data, axis=0)
        write(self.filename, self.samplerate, recording)
        print(f"Recording saved to {self.filename}")

