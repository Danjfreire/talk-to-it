from services.conversation_service import ConversationService
from services.audio_sevice import AudioService
from tts.tts_client import TTSClient

class AppState:
    models_loaded: bool = False
    is_recording: bool = False


class AppController:
    def __init__(self, conversation_service:  ConversationService, audio_service: AudioService, tts_client: TTSClient):
        self.state = AppState() 
        self.conversation_service = conversation_service
        self.audio_service = audio_service
        self.tts_client = tts_client
    
    async def handle_text_prompt(self, prompt: str):
        ai_text = await self.conversation_service.process_prompt(prompt)
        return ai_text
    
    def is_recording(self) -> bool: 
        return self.audio_service.is_recording

    async def start_recording(self):
        if self.audio_service.is_recording:
            print("Already recording")
            return
        
        await self.audio_service.start_recording()
    
    async def stop_recording(self) -> str | None:
        if not self.audio_service.is_recording:
            print("Not currently recording")
            return
        
        transcription = await self.audio_service.stop_recording()
        return transcription
    
    async def play_response(self, text: str):
        response_path = await self.tts_client.tts(text, self.conversation_service.character.audio_sample_path)
        await self.audio_service.play_audio(response_path)
