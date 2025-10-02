import time
import librosa
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration

class Transcriber:
    def __init__(self, model,processor):
        self._model: WhisperForConditionalGeneration = model
        self._processor: WhisperProcessor = processor
    
    def transcribe(self, file_path: str) -> str:
        audio_input, sampling_rate = librosa.load(file_path, sr=16000)
        start_time = time.perf_counter()
        input_features = self._processor(audio_input, sampling_rate=sampling_rate, return_tensors="pt").input_features

        # generate token ids
        predicted_ids = self._model.generate(input_features)

        end_time = time.perf_counter()
        # decode token ids to text
        transcription = self._processor.batch_decode(predicted_ids, skip_special_tokens=True)

        print(f"Transcription took {end_time - start_time:.2f} seconds")
        print(transcription)
        return transcription[0]
