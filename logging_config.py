import logging
import sys
from pathlib import Path

def setup_logging():
    """
    Configure logging to send library logs to a file and suppress console output.
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "app.log"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Capture INFO and above (not DEBUG)
    
    # Remove any existing handlers
    root_logger.handlers.clear()
    
    # File handler - logs INFO and above to file
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler - only show warnings and errors
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.WARNING)  # Only show warnings and above
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Silence specific noisy libraries (only show warnings/errors)
    logging.getLogger('transformers').setLevel(logging.ERROR)
    logging.getLogger('datasets').setLevel(logging.WARNING)
    logging.getLogger('langchain').setLevel(logging.WARNING)
    logging.getLogger('tensorflow').setLevel(logging.ERROR)
    logging.getLogger('torch').setLevel(logging.WARNING)
    logging.getLogger('torchaudio').setLevel(logging.WARNING)
    logging.getLogger('torio').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('pydub').setLevel(logging.WARNING)
    logging.getLogger('pydub.converter').setLevel(logging.WARNING)
    
    # Log the setup
    logging.info(f"Logging configured. Logs will be written to: {log_file}")
    
    return log_file
