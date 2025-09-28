from commands.command_base import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repl.repl import Repl


class StopRecordingCommand(Command):
    name="stop"
    description="Stop recording audio input"

    def execute(self, repl:"Repl"):
        if repl._state["is_recording"]:
            repl.config.recorder.stop()
            repl._state["is_recording"] = False
        else:
            print("system must be recording to stop recording")