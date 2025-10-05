import asyncio

from audio_recorder.recorder import AudioRecorder
from audio_player.player import AudioPlayer
from transcriber.transcriber import Transcriber

class AudioService:
    def __init__(self, recorder: AudioRecorder, player:AudioPlayer, transcriber:Transcriber):
        self.recorder = recorder
        self.player = player
        self.transcriber = transcriber
        self._is_recording = False

    @property
    def is_recording(self) -> bool:
        return self._is_recording
    
    async def start_recording(self):
        if self._is_recording:
            print("Already recording")
            return
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.recorder.record)
        self._is_recording = True
    
    async def stop_recording(self) -> str | None:
        if not self._is_recording:
            print("Not currently recording")
            return
        
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, self.recorder.stop)
        self._is_recording = False

        if file_path:
            transcription = await loop.run_in_executor(
                None,
                lambda: self.transcriber.transcribe(file_path)
            )
            return transcription
        return None
    
    async def play_audio(self, file_path: str):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: self.player.play(file_path))

