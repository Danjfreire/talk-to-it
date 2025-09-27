from audio_recorder.recorder import AudioRecorder
from repl.repl import Repl, ReplConfig

def main():
    recorder = AudioRecorder(samplerate=44100, filename="outputs/output.wav")

    repl = Repl(ReplConfig(recorder=recorder))

    repl.start()

if __name__ == "__main__":
    main()
