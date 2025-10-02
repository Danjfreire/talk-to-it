from transformers import WhisperProcessor, WhisperForConditionalGeneration
from audio_recorder.recorder import AudioRecorder
from audio_player.player import AudioPlayer
from transcriber.transcriber import Transcriber
from repl.repl import Repl, ReplConfig

def main():
    print("Initializing models...")

    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
    model.config.forced_decoder_ids = None
    transcriber = Transcriber(model=model, processor=processor)
    recorder = AudioRecorder(samplerate=44100, filename="outputs/output.wav")
    player = AudioPlayer()

    repl = Repl(ReplConfig(recorder=recorder, player=player,transcriber=transcriber))

    repl.start()

if __name__ == "__main__":
    main()
