"""Description of your app."""
from typing import Type

from steamship.invocable import Config, PackageService, create_handler, post

# NOTE: It should be `notion` not `src.notion` here.
from notion import add_markdown, notion_page_to_audio_url

# NOTE: It should be `transcribe` not `src.transcribe` here.
from transcribe import transcribe_audio


class NotionAutoTranscribeConfig(Config):
    """Config object containing required parameters to initialize a NotionAutoTranscribe instance."""

    notion_key: str  # Required


class NotionAutoTranscribe(PackageService):
    """Example steamship Package."""

    config: NotionAutoTranscribeConfig

    def config_cls(self) -> Type[Config]:
        """Return the Configuration class."""
        return NotionAutoTranscribeConfig

    @post("transcribe")
    def transcribe(self, url: str = None) -> str:
        """Transcribe the audio in the first Notion block of the page at `url` and append to the page.

        This uses the API Key provided at configuration time to fetch the Notion Page, transcribe the
        attached audio file, and then post the transcription results back to Notion as Markdown Text.
        """
        page_id, audio_url = notion_page_to_audio_url(url, self.config.notion_key)
        print(f"Audio url: {audio_url}")
        print(f"Page ID: {page_id}")

        # Transcribe the file into Markdown
        markdown = transcribe_audio(audio_url, self.client)

        print(f"Markdown: {markdown}")

        # Add it to Notion
        res_json = add_markdown(page_id, markdown, self.config.notion_key)

        print(f"Res JSON: {res_json}")

        return res_json


handler = create_handler(NotionAutoTranscribe)
