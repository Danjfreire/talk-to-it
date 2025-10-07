import os
import asyncio
from functools import partial


async def init(status_callback: callable = None) -> dict:
    """Initialize the repl with lazy imports to avoid blocking the UI"""
    
    # Move all heavy imports here so they don't block app startup
    if status_callback:
        status_callback("Importing dependencies...")
    
    # These imports might be heavy and block the UI
    from audio_recorder.recorder import AudioRecorder
    from characters.character import Character
    from audio_player.player import AudioPlayer
    from tts.tts_client import TTSClient
    from transcriber.transcriber import Transcriber
    from repl.repl import Repl, ReplConfig
    from langchain.chat_models import init_chat_model
    from chatterbox import ChatterboxTTS
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    
    # TODO: Move character config somewhere else
    arguments = os.sys.argv
    character_name = "shadowheart" if len(arguments) <= 1 else arguments[1]
    
    def _load_models_sync():
        """Synchronous model loading function to run in thread pool"""
        print("Loading character configuration...")
        character = Character(character_name=character_name)
        
        if not os.environ.get("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not set")
        
        if status_callback:
            status_callback("Loading LLM model...")

        llm_model = init_chat_model("gemini-2.5-flash", model_provider="google-genai")

        if status_callback:
            status_callback("Loading TTS model...")
        tts_model = ChatterboxTTS.from_pretrained(device="cuda")


        if status_callback:
            status_callback("Loading Speech Recognition model...")

        processor = WhisperProcessor.from_pretrained("openai/whisper-base")
        speech_rec_model= WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
        speech_rec_model.config.forced_decoder_ids = None
        
        if status_callback:
            status_callback("Models loaded successfully!")

        return {
            'character': character,
            'llm_model': llm_model,
            'tts_model': tts_model,
            'processor': processor,
            'speech_rec_model': speech_rec_model 
        }
    
    loop = asyncio.get_event_loop()
    models = await loop.run_in_executor(None, _load_models_sync)
    
    transcriber = Transcriber(model=models['speech_rec_model'], processor=models['processor'])
    recorder = AudioRecorder(samplerate=44100, filename="outputs/output.wav")
    tts_client = TTSClient(models['tts_model'])
    player = AudioPlayer()

    models_dict = {
        "transcriber": transcriber,
        "recorder": recorder,
        "tts_client": tts_client,
        "player": player,
        "llm_model": models['llm_model'],
        "character": models['character']
    }

    return models_dict
