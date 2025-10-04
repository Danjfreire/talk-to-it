from commands.command_base import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repl.repl import Repl


class StartRecordingCommand(Command):
    name="record"
    description="Starts recording audio input"

    async def execute(self, repl:"Repl"):
        repl.config.recorder.record()
        repl._state["is_recording"] = True