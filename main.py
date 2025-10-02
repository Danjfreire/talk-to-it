import os
from dotenv import load_dotenv
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from audio_recorder.recorder import AudioRecorder
from audio_player.player import AudioPlayer
from transcriber.transcriber import Transcriber
from repl.repl import Repl, ReplConfig
from langchain.chat_models import init_chat_model

load_dotenv()

def main():
    print("Initializing models...")

    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not set.")
        exit(1)
    
    llm_model = init_chat_model("gemini-2.5-flash", model_provider="google-genai")
    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    speech_rec_model= WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
    speech_rec_model.config.forced_decoder_ids = None
    transcriber = Transcriber(model=speech_rec_model, processor=processor)
    recorder = AudioRecorder(samplerate=44100, filename="outputs/output.wav")
    player = AudioPlayer()

    repl = Repl(ReplConfig(recorder=recorder, player=player,transcriber=transcriber, llm_model=llm_model))

    repl.start()

if __name__ == "__main__":
    main()
