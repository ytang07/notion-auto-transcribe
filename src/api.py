"""Description of your app."""
from typing import Type
import time
from steamship import Steamship
from steamship.base import TaskState
import os
import requests
import json

from dotenv import load_dotenv
from pathlib import Path

from steamship.invocable import Config, create_handler, post, PackageService

class MyPackageConfig(Config):
    """Config object containing required parameters to initialize a MyPackage instance."""

    # This config should match the corresponding configuration in your steamship.json
    default_name: str  # Required
    enthusiastic: bool = False  # Not required


class MyPackage(PackageService):
    """Example steamship Package."""

    config: MyPackageConfig

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        env_path = Path('.')/'.env'
        load_dotenv(dotenv_path=env_path)

        NOTION_KEY = os.environ.get("NOTION_KEY")
        self.headers = {'authorization': f"Bearer {NOTION_KEY}",
                    'Content-Type': 'application/json',
                    'Notion-Version': '2022-06-28',
                    "accept": "application/json",
                    }

    def config_cls(self) -> Type[Config]:
        """Return the Configuration class."""
        return MyPackageConfig

    @post("transcribe")
    def transcribe(self, url: str = None) -> str:
        """Return a greeting to the user."""
        instance = Steamship.use("audio-markdown", "audio-markdown-crows-v27")
        block_id = url.split("#")[1]
        url = f"https://api.notion.com/v1/blocks/{block_id}"
        response = requests.get(url, headers=self.headers)
        print(response.text)
        res_json = json.loads(response.text)
        print(res_json)

        audio_url = res_json['audio']['file']['url']
        page_id = res_json['parent']['page_id']

        transcribe_task = instance.invoke("transcribe_url", url=audio_url)
        task_id = transcribe_task["task_id"]
        status = transcribe_task["status"]

        # Wait for completion
        retries = 0
        while retries <= 100 and status != TaskState.succeeded:
            response = instance.invoke("get_markdown", task_id=task_id)
            status = response["status"]
            if status == TaskState.failed:
                print(f"[FAILED] {response}['status_message']")
                break

            print(f"[Try {retries}] Transcription {status}.")
            if status == TaskState.succeeded:
                break
            time.sleep(2)
            retries += 1

        # Get Markdown
        markdown = response["markdown"]

        # this page id points to the page housing both the mp3 file and the returned markdown
        add_text_block = {
            "children":
            [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                "type": "text",
                "text": {
                    "content": markdown,
                }
                }]
            }
            }]
        }

        create_response = requests.patch(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            json=add_text_block, headers=self.headers)
        return (create_response.json())

handler = create_handler(MyPackage)
