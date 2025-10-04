import asyncio
from dotenv import load_dotenv

load_dotenv()

from textual.app import App
from textual.widgets import Header, Footer, LoadingIndicator, Static, Input
from textual.containers import Vertical

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

    def compose(self):
        yield Header()
        with Vertical():
            yield LoadingIndicator(id="loading")
            yield Static("Starting up...", id="status")
            yield Input(placeholder="Enter a prompt", id="prompt-input", disabled=True)
        yield Footer()
    
    async def on_mount(self):
        # Create a background task for initialization
        asyncio.create_task(self._initialize_models())
    
    async def _initialize_models(self):
        """Background task for model initialization"""
        try:
            loading = self.query_one("#loading", LoadingIndicator)
            status = self.query_one("#status", Static)

            await asyncio.sleep(1)
            
            status.update("Loading dependencies...")
            await asyncio.sleep(0.5)
            
            # Import here to avoid blocking on module import
            from init_models import init
            
            status.update("Initializing models (this may take a few minutes)...")
            await asyncio.sleep(0.5)

            self.repl = await init()
            self.models_loaded = True 

            loading.display = False
            status.update("Ready! Press 'r' to record or 'p' for prompt")
        
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

        input_field = self.query_one("#prompt-input", Input)

        if self.input_visible:
            self._set_prompt_visible(False)
        else:
            self._set_prompt_visible(True)

    def action_hide_input(self):
        if self.input_visible:
            self._set_prompt_visible(False)
    
    async def on_input_submitted(self, event: Input.Submitted):
        if not self.models_loaded:
            self.bell()
            return
        
        prompt = event.value
        if prompt.strip():
            event.input.value = ""

            self._set_prompt_visible(False)

            asyncio.create_task(self._handle_prompt(prompt))


    def _set_prompt_visible(self, visible:bool):
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


    def action_record(self):
        print("Record action triggered")
        if not self.models_loaded:
            self.bell()
            return
        
        asyncio.create_task(self._handle_recording())
        
    async def _handle_prompt(self, prompt: str):
        try:
            status = self.query_one("#status", Static)
            status.update("Processing prompt...")
            await self.repl.handle_prompt(prompt)
            status.update("Ready! Press 'r' to record or 'p' for prompt")
        except Exception as e:
            status = self.query_one("#status", Static)
            status.update(f"Error during prompt handling: {e}")
        
    async def _handle_recording(self):
        
        try:
            if not self.repl._state["is_recording"]:
                await self.repl.handle_command("record")
            else:
                await self.repl.handle_command("stop")
        except Exception as e:
            status = self.query_one("#status", Static)
            status.update(f"Error during recording: {e}")


    def action_quit(self):
        self.exit()

if __name__ == "__main__":
    app = TalkToItApp()
    app.run()