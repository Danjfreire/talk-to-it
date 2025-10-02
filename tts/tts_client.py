from chatterbox import ChatterboxTTS
import torchaudio as ta

class TTSClient:
    def __init__(self, model:ChatterboxTTS):
        self.model = model
    
    def tts(self,text:str, audio_prompt_path: str, output_path:str="outputs/tts-output.wav",) -> str:
        wav = self.model.generate(text,audio_prompt_path=audio_prompt_path)
        ta.save(output_path, wav, self.model.sr)
        return output_path

