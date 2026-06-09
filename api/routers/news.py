import json
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def retrieve_news():
    with open("data/news.json", "r") as f:
        news = json.load(f)
    return news
