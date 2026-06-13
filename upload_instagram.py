import os
import json
import glob
import time
import requests

ACCESS_TOKEN = os.environ["IG_ACCESS_TOKEN"]
IG_USER_ID = os.environ["IG_USER_ID"]
GRAPH_URL = "https://graph.facebook.com/v19.0"


def publish_reel(video_url, caption):
    resp = requests.post(
        f"{GRAPH_URL}/{IG_USER_ID}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": ACCESS_TOKEN,
        },
    )
    resp.raise_for_status()
    creation_id = resp.json()["id"]
    print(f"Created container: {creation_id}")

    for _ in range(30):
        status = requests.get(
            f"{GRAPH_URL}/{creation_id}",
            params={"fields": "status_code", "access_token": ACCESS_TOKEN},
        ).json()
        if status.get("status_code") == "FINISHED":
            break
        print("Processing...", status)
        time.sleep(10)

    resp = requests.post(
        f"{GRAPH_URL}/{IG_USER_ID}/media_publish",
        data={"creation_id": creation_id, "access_token": ACCESS_TOKEN},
    )
    resp.raise_for_status()
    print("Published:", resp.json())


if __name__ == "__main__":
    meta_files = sorted(glob.glob("output/meta_*.json"))
    meta = json.load(open(meta_files[-1]))
    video_url = os.environ["VIDEO_PUBLIC_URL"]
    publish_reel(video_url, meta["description"])
