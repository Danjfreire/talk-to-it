import asyncio
from dotenv import load_dotenv

load_dotenv()

from textual.app import App
from textual.widgets import Header, Footer, LoadingIndicator, Static, Input
from textual.containers import Vertical, VerticalScroll, Horizontal, Right
from services.conversation_service import ConversationService
from services.audio_sevice import AudioService
from controllers.app_controller import AppController

class ChatMessage(Horizontal):
    def __init__(self, message: str, speaker: str = "user"):
        super().__init__()
        self.message = message
        self.speaker = speaker

    def on_mount(self) -> None:
        print(f"Mounting message: {self.message} from {self.speaker}")
        msg = Static(f"{self.message}")
        msg.add_class("message")

        if self.speaker == "user":
            msg.add_class("user-message")
        else:
            msg.add_class("ai-message")
        self.mount()


class ChatWindow(VerticalScroll):
    def append_message(self, message: str, speaker: str):
        # container = Horizontal()
        # container.styles.width = "100%"
        # container.styles.height = "auto"
        # self.mount(container)
        
        msg = Static(f"{message}")
    
        msg.add_class("message")

        if speaker == "user":
            msg.add_class("user-message")
            self.mount(Right(msg))
        else:
            msg.add_class("ai-message")
            self.mount(msg)
        
        

class TalkToItApp(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("p", "prompt", "Prompt"),
        ("r", "record", "Record"),
        ("escape", "hide_input", "Hide Input")
    ]

    def __init__(self):
        super().__init__()
        self.repl = None
        self.models_loaded = False
        self.input_visible = False
        self.controller: AppController = None
        self.chat_window: ChatWindow = None

    def compose(self):
        yield Header()
        with Vertical():
            yield LoadingIndicator(id="loading")
            yield Static("Starting up...", id="status")
            yield ChatWindow(id="chat-window")
            yield Input(placeholder="Enter a message", id="prompt-input", disabled=True)
        yield Footer()
    
    async def on_mount(self):
        asyncio.create_task(self._initialize())
    
    async def _initialize(self):
        try:
            loading = self.query_one("#loading", LoadingIndicator)
            status = self.query_one("#status", Static)
            chat_window = self.query_one("#chat-window", ChatWindow)

            await asyncio.sleep(1)
            
            status.update("Loading dependencies...")
            await asyncio.sleep(0.5)
            
            # Import here to avoid blocking on module import
            from init_models import init
            
            status.update("Initializing models (this may take a few minutes)...")
            await asyncio.sleep(0.5)

            models = await init()
            self.models_loaded = True 
            conversation_service = ConversationService(llm_model=models['llm_model'], character= models['character'])
            audio_service = AudioService(recorder=models['recorder'], transcriber=models['transcriber'], player=models['player'])
            self.controller = AppController(audio_service=audio_service, conversation_service=conversation_service, tts_client=models['tts_client'])

            loading.display = False
            chat_window.disabled = False
            self.chat_window = chat_window
        except Exception as e:
            loading = self.query_one("#loading", LoadingIndicator)
            status = self.query_one("#status", Static)
            loading.display = False
            status.update(f"Error: {e}")
            print(f"Full error: {e}")

    def action_prompt(self):
        if not self.models_loaded:
            self.bell()
            return
        print("Prompt action triggered")

        if self.input_visible:
            self._set_input_visibility(False)
        else:
            self._set_input_visibility(True)

    def action_hide_input(self):
        if self.input_visible:
            self._set_input_visibility(False)
    
    async def on_input_submitted(self, event: Input.Submitted):
        if not self.models_loaded:
            self.bell()
            return
        
        prompt = event.value
        if prompt.strip():
            event.input.value = ""
            self.chat_window.append_message(prompt, "user")
            self._set_input_visibility(False)
            await self._handle_prompt(prompt)


    def _set_input_visibility(self, visible:bool):
        input_field = self.query_one("#prompt-input", Input)
        if visible:
            input_field.disabled = False
            input_field.add_class("visible")
            input_field.focus()
            self.input_visible = True
        else:
            input_field.disabled = True
            input_field.remove_class("visible")
            self.input_visible = False


    async def action_record(self):
        print("Record action triggered")
        if not self.models_loaded:
            self.bell()
            return

        is_recording = self.controller.is_recording()

        if not is_recording:
            # asyncio.create_task(self.controller.start_recording())
            await self.controller.start_recording()
        else:
            transcription = await self.controller.stop_recording()
            # transcription = await result
            print(f"Transcription: {transcription}")

            if transcription:
                await self._handle_prompt(transcription)
        
    async def _handle_prompt(self, prompt: str):
        ai_text = await self.controller.handle_text_prompt(prompt)
        audio_response = await self.controller.generate_audio_response(ai_text)
        self.chat_window.append_message(ai_text, "ai")
        await self.controller.play_response(audio_response)

    def action_quit(self):
        self.exit()

if __name__ == "__main__":
    app = TalkToItApp()
    app.run()