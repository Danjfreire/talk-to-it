import asyncio
from audio_recorder.recorder import AudioRecorder
from audio_player.player import AudioPlayer 
from tts.tts_client import TTSClient
from characters.character import Character
from transcriber.transcriber import Transcriber
from commands.help_command import HelpCommand
from commands.exit_command import ExitCommand
from commands.command_base import Command
from commands.start_recording_command import StartRecordingCommand
from commands.stop_recording_command import StopRecordingCommand 
from commands.repeat_command import ReapeatCommand
from commands.prompt_command import PromptCommand
from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

class ReplConfig:
    def __init__(
            self, 
            recorder:AudioRecorder,
            player:AudioPlayer,
            transcriber:Transcriber, 
            llm_model:BaseChatModel, 
            tts_client:TTSClient, 
            character:Character
            ):
        self.llm_model = llm_model
        self.player = player
        self.recorder = recorder
        self.transcriber = transcriber
        self.tts_client=tts_client 
        self.character=character

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
            StopRecordingCommand(),
            PromptCommand(),
            ReapeatCommand()
        ]

        commands = dict((cmd.name, cmd) for cmd in command_list)

        return commands

    async def handle_command(self, command_name:str):
        if command_name in self.commands:
            command = self.commands[command_name]
            await command.execute(self)
        else:
            print(f'unknown command : {command_name}, type "help" for a list of commands')

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
        
    async def handle_prompt(self, prompt:str):
            loop = asyncio.get_event_loop()

            messages = [
                SystemMessage(content=f"{self.config.character.description}\n Your answers should not include any code block or markdown. Answer with sentences like a human would."),
                HumanMessage(content=prompt)
            ]

            res = await loop.run_in_executor(
                None,
                lambda: self.config.llm_model.invoke(messages)
            ) 
            ai_text = res.content
            print(f"AI: {ai_text}")
            tts_output_path = await loop.run_in_executor(
                None,
                lambda: self.config.tts_client.tts(ai_text, audio_prompt_path=self.config.character.audio_sample_path)
            )

            await loop.run_in_executor(
                None,
                lambda: self.config.player.play(tts_output_path)
            )
