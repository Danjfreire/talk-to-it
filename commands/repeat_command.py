import os
from commands.command_base import Command 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repl.repl import Repl

class ReapeatCommand(Command):
    name = "repeat"
    description = "Replays the last AI response"

    def execute(self, repl: "Repl"):
        if os.path.exists(repl.config.tts_client.output_path):
            repl.config.player.play(repl.config.tts_client.output_path)
        else:
            print("No previous AI response to repeat.")



