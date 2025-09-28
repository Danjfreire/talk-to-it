from commands.command_base import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repl.repl import Repl


class StopRecordingCommand(Command):
    name="stop"
    description="Stop recording audio input"

    def execute(self, repl:"Repl"):
        if repl._state["is_recording"]:
            file_path = repl.config.recorder.stop()
            repl._state["is_recording"] = False
            if file_path is None:
                return
            repl.config.transcriber.transcribe(file_path=file_path)
        else:
            print("system must be recording to stop recording")