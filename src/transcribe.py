import time

from steamship import Steamship, TaskState


def transcribe_audio(audio_url: str, ship: Steamship):
    instance = ship.use("audio-markdown", "audio-markdown-crows-v27")
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
    return markdown