"""Helper functions for Notion."""
import json
import uuid
from typing import Dict

import requests


def notion_headers(api_key: str) -> dict:
    """Prepare notion api headers."""
    return {
        "authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
        "accept": "application/json",
    }


def notion_get(path: str, api_key: str):
    """Send a notion get request."""
    url = f"https://api.notion.com/v1/{path}"
    response = requests.get(url, headers=notion_headers(api_key))
    print(response.text)
    res_json = json.loads(response.text)
    print(res_json)
    return res_json


def notion_patch(path: str, content: Dict, api_key: str):
    """Send a notion patch request."""
    url = f"https://api.notion.com/v1/{path}"
    response = requests.patch(url, json=content, headers=notion_headers(api_key))
    res_json = response.json()
    return res_json


PageId = str
AudioUrl = str


def notion_block_to_audio_url(block: dict) -> (PageId, AudioUrl):
    """Get the audio url from the notion block json."""
    audio_url = block["audio"]["file"]["url"]
    page_id = block["parent"]["page_id"]
    return (page_id, audio_url)


def notion_page_to_audio_url(url: str, api_key: str) -> (PageId, AudioUrl):
    """Get the audio url from the notion page url."""
    if "#" in url:
        # We assume someone has copied the block.
        block_id = url.split("#")[1]
        block = notion_get(f"blocks/{block_id}", api_key)
        return notion_block_to_audio_url(block)
    else:
        # This is what the incoming Zapier page reference will look like.
        # from: https://www.notion.so/Creating-Page-Sample-ee18b8779ae54f358b09221d6665ee15
        # to: Creating-Page-Sample-ee18b8779ae54f358b09221d6665ee15
        block_id = url.split("/")[-1]
        # from: Creating-Page-Sample-ee18b8779ae54f358b09221d6665ee15
        # to: ee18b8779ae54f358b09221d6665ee15
        block_id = block_id.split("-")[-1]

        # This is necessary because the URL doesn't have the hyphens in 8-4-4-4-12 format, but the API requires it
        block_uuid = uuid.UUID(block_id)
        notion_page_children = notion_get(f"blocks/{block_uuid}/children", api_key)
        return notion_block_to_audio_url(notion_page_children["results"][0])


def add_markdown(page_id: str, markdown: str, api_key: str):
    """Add markdown to the page."""
    add_text_block = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": markdown,
                            },
                        }
                    ]
                },
            }
        ]
    }
    return notion_patch(f"blocks/{page_id}/children", add_text_block, api_key)
