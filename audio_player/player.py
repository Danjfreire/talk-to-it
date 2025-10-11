import os
from contextlib import contextmanager
from pydub import AudioSegment
from pydub.playback import play

@contextmanager
def suppress_stdout_stderr():
    """Context manager to suppress stdout and stderr at the file descriptor level."""
    # In Textual apps, sys.stdout/stderr may not have valid file descriptors
    # So we redirect the actual OS-level stdout/stderr (fd 1 and 2)
    
    # Save copies of the original file descriptors 1 (stdout) and 2 (stderr)
    try:
        stdout_dup = os.dup(1)
        stderr_dup = os.dup(2)
    except OSError:
        # If file descriptors aren't available, just yield without suppression
        yield
        return
    
    # Open devnull
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    
    try:
        # Redirect stdout and stderr to devnull at the file descriptor level
        os.dup2(devnull_fd, 1)
        os.dup2(devnull_fd, 2)
        yield
    finally:
        # Restore the original file descriptors
        os.dup2(stdout_dup, 1)
        os.dup2(stderr_dup, 2)
        
        # Close the duplicates and devnull
        os.close(stdout_dup)
        os.close(stderr_dup)
        os.close(devnull_fd)

class AudioPlayer:

    def play(self, file_path: str):
        audio = AudioSegment.from_wav(file_path)
        # Suppress pydub's verbose output during playback
        with suppress_stdout_stderr():
            play(audio)