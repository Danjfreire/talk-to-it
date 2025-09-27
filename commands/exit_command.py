from commands.command_base import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repl.repl import Repl


class ExitCommand(Command):
    name: str = "exit"
    description: str = "Exit the REPL" 

    def execute(self, repl: "Repl"):
        repl._state["should_exit"] = True