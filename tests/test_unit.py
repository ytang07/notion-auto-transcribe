"""Unit tests for the package."""
import os
from pathlib import Path

from steamship import Steamship

from src.api import NotionAutoTranscribe

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def test_transcription():
    """You can test your app like a regular Python object."""
    print("Running")
    client = Steamship()
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    NOTION_KEY = os.environ.get("NOTION_KEY")

    app = NotionAutoTranscribe(client=client, config={"notion_key": NOTION_KEY})

    app.transcribe(url="https://www.notion.so/69f267134bd44249817339cad1a2e140#6575059dc4f14ead922e8e09f0afee6b")