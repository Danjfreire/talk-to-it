import asyncio
from commands.command_base import Command
from typing import TYPE_CHECKING
from langchain_core.messages import HumanMessage, SystemMessage


if TYPE_CHECKING:
    from repl.repl import Repl


class StopRecordingCommand(Command):
    name="stop"
    description="Stop recording audio input"

    async def execute(self, repl:"Repl"):
        if repl._state["is_recording"]:
            loop = asyncio.get_event_loop()

            file_path =  await loop.run_in_executor(None, repl.config.recorder.stop)
            repl._state["is_recording"] = False
            if file_path is None:
                return

            transcription = await loop.run_in_executor(
                None,
                lambda: repl.config.transcriber.transcribe(file_path=file_path)
            )

            await repl.handle_prompt(transcription)
        else:
            print("system must be recording to stop recording")