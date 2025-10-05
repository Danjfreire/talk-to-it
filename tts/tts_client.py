import asyncio

from chatterbox import ChatterboxTTS
import torchaudio as ta
import time

class TTSClient:
    def __init__(self, model:ChatterboxTTS, output_path:str="outputs/tts-output.wav"):
        self.model = model
        self.output_path = output_path
    
    async def tts(self,text:str, audio_prompt_path: str ) -> str:
        start_time = time.perf_counter()
        loop = asyncio.get_event_loop()
        wav = await loop.run_in_executor(None, lambda: self.model.generate(text, audio_prompt_path=audio_prompt_path))
        await loop.run_in_executor(None, lambda: ta.save(self.output_path, wav, self.model.sr))
        end_time = time.perf_counter()
        print(f"TTS generation took {end_time - start_time:.2f} seconds")
        return self.output_path
        

        # wav = self.model.generate(text,audio_prompt_path=audio_prompt_path)
        # ta.save(self.output_path, wav, self.model.sr)
    

    

