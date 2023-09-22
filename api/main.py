import logging
import os
from typing import Annotated

from fastapi import FastAPI, Query

from connections import NotionConnections

logger = logging.getLogger(__name__)

app = FastAPI()

DATABASE_ID = os.environ.get("DATABASE_ID", "")


@app.get("/")
async def root():
    return {"message": "Notion API Connection Demo"}


@app.post("/notion/")
async def get_notion_page(
    database_id: Annotated[
        str, Query(..., title="DATABASE_ID 測試", description="DATABASE_ID 測試")
    ] = DATABASE_ID
):
    res = NotionConnections.query_db(database_id)
    target_data = res.get("results")[0]
    page_id = target_data.get("id")
    res = NotionConnections.update_page(page_id)
    if res.get("id") == page_id:
        title = res["properties"]["Name"]["title"][0]["text"]["content"]
        public_url = res["public_url"]
        logger.warning(f"{title}, page_id: {page_id} has been shared.")
        return {"code": 0, "msg": f"{title} share url: {public_url}"}
    return {"code": -1, "msg": "update resp no id"}
