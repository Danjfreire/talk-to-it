from chatterbox import ChatterboxTTS
import torchaudio as ta

class TTSClient:
    def __init__(self, model:ChatterboxTTS):
        self.model = model
    
    def tts(self,text:str, output_path:str="outputs/tts-output.wav") -> str:
        wav = self.model.generate(text)
        ta.save(output_path, wav, self.model.sr)
        return output_path

