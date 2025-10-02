from commands.command_base import Command 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repl.repl import Repl

class PromptCommand(Command):
    name = "prompt"
    description = "Enter a textual prompt for the AI character"

    def execute(self, repl: "Repl"):
        prompt = input("Enter your prompt:")

        if prompt == "":
            return

        repl.handle_prompt(prompt)       




