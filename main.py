from transformers import WhisperProcessor, WhisperForConditionalGeneration
from audio_recorder.recorder import AudioRecorder
from transcriber.transcriber import Transcriber
from repl.repl import Repl, ReplConfig

def main():
    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
    model.config.forced_decoder_ids = None
    transcriber = Transcriber(model=model, processor=processor)
    recorder = AudioRecorder(samplerate=44100, filename="outputs/output.wav")

    repl = Repl(ReplConfig(recorder=recorder, transcriber=transcriber))

    repl.start()

if __name__ == "__main__":
    main()
