import asyncio
from dotenv import load_dotenv

load_dotenv()

from textual.app import App
from textual.widgets import Header, Footer, LoadingIndicator, Static, Input
from textual.containers import Vertical, VerticalScroll, Right, Horizontal
from services.conversation_service import ConversationService
from services.audio_sevice import AudioService
from tts.tts_client import TTSClient

class RecordingIndicator(Horizontal):
    def __init__(self):
        super().__init__()
        self._animation_task = None

    def compose(self):
        yield Static("●", id="recording-dot")
        yield Static("Recording...", id="recording-text")
    
    def on_mount(self):
        self._start_animation()
    
    def _start_animation(self):
        self.styles.opacity = 1.0
        self.styles.animate("opacity", value=0.0, duration=1, on_complete=self._fade_in)
    
    def _fade_in(self):
        self.styles.opacity = 0.0
        self.styles.animate("opacity", value=1.0, duration=1, on_complete=self._start_animation)


class AiTypingIndicator(Horizontal):
    def __init__(self, character_name: str):
        self.character_name = character_name
        self._animation_task = None
        super().__init__()

    def compose(self):
        yield Static(id="typing-text")
    
    def on_mount(self):
        self._animation_task = asyncio.create_task(self._animate_dots())
    
    def on_unmount(self):
        if self._animation_task:
            self._animation_task.cancel()
    
    async def _animate_dots(self):
        typing_indicator = self.query_one("#typing-text", Static)
        dots_states = [".", "..", "...", ""]
        index = 0
        
        try:
            while True:
                typing_indicator.update(f"{self.character_name} is typing{dots_states[index]}")
                index = (index + 1) % len(dots_states)
                await asyncio.sleep(0.5) 
        except asyncio.CancelledError:
            pass 
    

class ChatWindow(VerticalScroll):
    def append_message(self, message: str, speaker: str):
        msg = Static(f"{message}")
        msg.add_class("message")

        if speaker == "user":
            msg.add_class("user-message")
            self.mount(Right(msg))
        else:
            msg.add_class("ai-message")
            self.mount(msg)
        
        self.scroll_end(animate=False)
        

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
        self.models_loaded = False
        self.input_visible = False
        self.audio_service: AudioService = None
        self.conversation_service: ConversationService = None
        self.tts_client: TTSClient = None
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

            models = await init(status_callback=self.set_loading_status)
            self.conversation_service = ConversationService(llm_model=models['llm_model'], character= models['character'])
            self.audio_service = AudioService(recorder=models['recorder'], transcriber=models['transcriber'], player=models['player'])
            self.tts_client = models['tts_client']
            self.models_loaded = True 

            loading.display = False
            status.display = False
            chat_window.disabled = False
            chat_window.add_class("visible")
            self.chat_window = chat_window
        except Exception as e:
            loading = self.query_one("#loading", LoadingIndicator)
            status = self.query_one("#status", Static)
            loading.display = False
            status.update(f"Error: {e}")
            print(f"Full error: {e}")

# ---------------------------------------------------------------------------------------------------------------------- 
# ACTION HANDLERS

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
    
    async def action_record(self):
        print("Record action triggered")
        if not self.models_loaded:
            self.bell()
            return

        is_recording = self.audio_service.is_recording

        if not is_recording:
            recording_indicator = RecordingIndicator()
            recording_indicator.id = "recording-indicator"

            self.mount(recording_indicator, after=self.chat_window)
            await self.audio_service.start_recording()
        else:
            transcription = await self.audio_service.stop_recording()
            self.query_one("#recording-indicator").remove()
            print(f"Transcription: {transcription}")
            self.chat_window.append_message(transcription, "user")

            if transcription:
                asyncio.create_task(self._handle_prompt(transcription))
                # await self._handle_prompt(transcription)

    def action_quit(self):
        self.exit()
# ----------------------------------------------------------------------------------------------------------------------
# EVENT HANDLERS

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

# ----------------------------------------------------------------------------------------------------------------------
# INTERNAL LOGIC
        
    async def _handle_prompt(self, prompt: str):
        typing_indicator = AiTypingIndicator(self.conversation_service.character.name)
        self.chat_window.mount(typing_indicator)

        ai_text = await self.conversation_service.handle_prompt(prompt)
        audio_response = await self.tts_client.tts(ai_text, self.conversation_service.character.audio_sample_path)
        typing_indicator.remove()

        self.chat_window.append_message(ai_text, "ai")
        await self.audio_service.play_audio(audio_response)

#-----------------------------------------------------------------------------------------------------------------------
# UTILITY METHODS

    def set_loading_status(self, message: str):
        status = self.query_one("#status", Static)
        status.update(f">> {message}")

if __name__ == "__main__":
    app = TalkToItApp()
    app.run()