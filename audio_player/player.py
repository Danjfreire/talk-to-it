from pydub import AudioSegment
from pydub.playback import play

class AudioPlayer:

    def play(self, file_path: str):
        audio = AudioSegment.from_wav(file_path)
        play(audio)