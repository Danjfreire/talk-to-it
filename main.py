import asyncio
from dotenv import load_dotenv

load_dotenv()

from textual.app import App
from textual.widgets import Header, Footer, LoadingIndicator, Static
from textual.containers import Vertical

class TalkToItApp(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("p", "prompt", "Prompt"),
        ("r", "record", "Record"),
    ]

    def __init__(self):
        super().__init__()
        self.repl = None
        self.models_loaded = False

    def compose(self):
        yield Header()
        with Vertical():
            yield LoadingIndicator(id="loading")
            yield Static("Starting up...", id="status")
        yield Footer()
    
    async def on_mount(self):
        # Create a background task for initialization
        asyncio.create_task(self._initialize_models())
    
    async def _initialize_models(self):
        """Background task for model initialization"""
        try:
            # loading = self.query_one("#loading", LoadingIndicator)
            status = self.query_one("#status", Static)

            status.update("App mounted! UI is working.")
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

    def action_record(self):
        if not self.models_loaded:
            self.bell()
            return
        print("Record action triggered")

    def action_quit(self):
        self.exit()

if __name__ == "__main__":
    app = TalkToItApp()
    app.run()