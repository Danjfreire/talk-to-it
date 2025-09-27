from audio_recorder.recorder import AudioRecorder

def main():
    recorder = AudioRecorder(samplerate=44100, filename="outputs/output.wav")
    recorder.record()
    input("Press Enter to stop recording...")
    recorder.stop()


if __name__ == "__main__":
    main()
