import os

import requests

NOTION_API = "https://api.notion.com/v1"
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22",
}


class NotionConnections:
    @staticmethod
    def query_db(database_id: str) -> dict or None:
        url = f"{NOTION_API}/databases/{database_id}/query"
        payload = {
            "filter": {"property": "Checked", "checkbox": {"equals": False}},
            "sorts": [{"property": "Created time", "direction": "ascending"}],
        }
        r = requests.post(url, headers=NOTION_HEADERS, json=payload)
        r.raise_for_status()
        if r.status_code == 200:
            res = r.json()
            return res

    @staticmethod
    def update_page(page_id: str) -> dict or None:
        page_id = page_id.replace("-", "")
        url = f"https://api.notion.com/v1/pages/{page_id}"
        r = requests.patch(
            url,
            headers=NOTION_HEADERS,
            json={"properties": {"Checked": {"checkbox": True}}},
        )
        r.raise_for_status()
        if r.status_code == 200:
            res = r.json()
            return res
