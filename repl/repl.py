from audio_recorder.recorder import AudioRecorder
from commands.help_command import HelpCommand
from commands.exit_command import ExitCommand
from commands.command_base import Command

class ReplConfig:
    def __init__(self, recorder=AudioRecorder):
        self.recorder = recorder

class Repl:
    def __init__(self, config=ReplConfig):
        self._config = config
        self._state = {"is_recording": False, "should_exit": False}
        self.commands: dict[str, Command] = self._discover_commands()

    def _discover_commands(self):
        help_cmd = HelpCommand()
        exit_cmd = ExitCommand()

        commands = {
            help_cmd.name: help_cmd,
            exit_cmd.name: exit_cmd
        }

        return commands
    
    def start(self):
        while True:
            user_input = input(">> ").strip().lower()

            if not user_input:
                continue

            command_name = user_input.split()[0]

            if command_name in self.commands:
                command = self.commands[command_name]
                command.execute(self)
            else:
                print(f'unknown command : {command_name}, type "help" for a list of commands')

            if self._state["should_exit"]:
                print("Exiting REPL...")
                break
        


    
    