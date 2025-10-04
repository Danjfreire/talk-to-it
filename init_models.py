import os
import asyncio
from functools import partial


async def init():
    """Initialize the repl with lazy imports to avoid blocking the UI"""
    
    # Move all heavy imports here so they don't block app startup
    print("Importing dependencies...")
    
    # These imports might be heavy and block the UI
    from audio_recorder.recorder import AudioRecorder
    from characters.character import Character
    from audio_player.player import AudioPlayer
    from tts.tts_client import TTSClient
    from transcriber.transcriber import Transcriber
    from repl.repl import Repl, ReplConfig
    from langchain.chat_models import init_chat_model
    
    arguments = os.sys.argv
    character_name = "shadowheart" if len(arguments) <= 1 else arguments[1]
    
    def _load_models_sync():
        """Synchronous model loading function to run in thread pool"""
        print("Loading character configuration...")
        character = Character(character_name=character_name)
        
        if not os.environ.get("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not set")
        
        print("Loading LLM model...")
        llm_model = init_chat_model("gemini-2.5-flash", model_provider="google-genai")
        
        print("Models loaded successfully!")
        return {
            'character': character,
            'llm_model': llm_model,
            'tts_model': None,
            'processor': None,
            'speech_rec_model': None
        }
    
    # Run the blocking model loading in a thread pool
    loop = asyncio.get_event_loop()
    models = await loop.run_in_executor(None, _load_models_sync)
    
    # Create the components
    transcriber = Transcriber(model=models['speech_rec_model'], processor=models['processor'])
    recorder = AudioRecorder(samplerate=44100, filename="outputs/output.wav")
    tts_client = TTSClient(models['tts_model'])
    player = AudioPlayer()

    repl = Repl(ReplConfig(
        recorder=recorder, 
        player=player,
        transcriber=transcriber, 
        llm_model=models['llm_model'], 
        tts_client=tts_client, 
        character=models['character']
    ))

    return repl
