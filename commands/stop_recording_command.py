from commands.command_base import Command
from typing import TYPE_CHECKING
from langchain_core.messages import HumanMessage, SystemMessage

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
            transcription = repl.config.transcriber.transcribe(file_path=file_path)
            # repl.config.player.play(file_path)
            # TEST 
            messages = [
                SystemMessage(content="" \
                "You are an expert programmer. Talk to the user in a concise and clear manner as if you are in a conversation. " \
                "Your answers should not include any code block or markdown. Answer with sentences like a human would." \
                ""),
                HumanMessage(content=transcription)
            ]

            res = repl.config.llm_model.invoke(messages)
            print(f"Ai: {res.content}")

        else:
            print("system must be recording to stop recording")