from typing import Dict

import requests
import json

def notion_headers(api_key: str) -> dict:
    return {
        'authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
        "accept": "application/json",
    }

def notion_get(path: str, api_key: str):
    url = f"https://api.notion.com/v1/{path}"
    response = requests.get(url, headers=notion_headers(api_key))
    print(response.text)
    res_json = json.loads(response.text)
    print(res_json)
    return res_json

def notion_patch(path: str, content: Dict, api_key: str):
    url = f"https://api.notion.com/v1/{path}"
    response = requests.patch(url, json=content, headers=notion_headers(api_key))
    res_json = response.json()
    return res_json

def add_markdown(page_id: str, markdown: str, api_key: str):
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
    return notion_patch(f"blocks/{page_id}/children", add_text_block, api_key)
