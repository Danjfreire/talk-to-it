from chatterbox import ChatterboxTTS
import torchaudio as ta

class TTSClient:
    def __init__(self, model:ChatterboxTTS, output_path:str="outputs/tts-output.wav"):
        self.model = model
        self.output_path = output_path
    
    def tts(self,text:str, audio_prompt_path: str ) -> str:
        wav = self.model.generate(text,audio_prompt_path=audio_prompt_path)
        ta.save(self.output_path, wav, self.model.sr)
        return self.output_path
    

    

