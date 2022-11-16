"""Unit tests for the package."""
import os
from pathlib import Path

from dotenv import load_dotenv
from steamship import Steamship

from notion import notion_page_to_audio_url
from src.api import NotionAutoTranscribe

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


def test_transcription_page():
    """Tests that we're getting the audio url correctly."""
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    NOTION_KEY = os.environ.get("NOTION_KEY")
    url = "https://www.notion.so/Mind-stack-057b827f994f4ef2ac0e18777e197efb"
    page_id, audio_url = notion_page_to_audio_url(url, NOTION_KEY)
    assert page_id
    assert audio_url


def test_transcription():
    """You can test your app like a regular Python object."""
    print("Running")
    client = Steamship()
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    NOTION_KEY = os.environ.get("NOTION_KEY")

    app = NotionAutoTranscribe(client=client, config={"notion_key": NOTION_KEY})

    app.transcribe(
        url="https://www.notion.so/69f267134bd44249817339cad1a2e140#6575059dc4f14ead922e8e09f0afee6b"
    )
