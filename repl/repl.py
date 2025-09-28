from audio_recorder.recorder import AudioRecorder
from commands.help_command import HelpCommand
from commands.exit_command import ExitCommand
from commands.command_base import Command
from commands.start_recording_command import StartRecordingCommand
from commands.stop_recording_command import StopRecordingCommand 

class ReplConfig:
    def __init__(self, recorder:AudioRecorder):
        self.recorder = recorder

class Repl:
    def __init__(self, config:ReplConfig):
        self.config:ReplConfig = config
        self._state = {"is_recording": False, "should_exit": False}
        self.commands: dict[str, Command] = self._discover_commands()

    def _discover_commands(self):
        command_list:list[Command] = [
            HelpCommand(),
            ExitCommand(),
            StartRecordingCommand(),
            StopRecordingCommand()
        ]

        commands = dict((cmd.name, cmd) for cmd in command_list)

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
        


    
    