from commands.command_base import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repl.repl import Repl

class HelpCommand(Command):
    name = "help"
    description = "List all available commands"

    def execute(self, repl: "Repl"):
        print("Available commands:")
        for name, command in repl.commands.items():
            print(f"- {name}: {command.description}")