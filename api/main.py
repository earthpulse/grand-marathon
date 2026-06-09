import argparse
import matplotlib
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.alerts import router as alerts_router
from routers.actions import router as actions_router
from routers.reports import router as reports_router
from routers.news import router as news_router
from routers.map import router as map_router

matplotlib.use("Agg")

app = FastAPI(title="api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
app.include_router(actions_router, prefix="/actions", tags=["actions"])
app.include_router(reports_router, prefix="/report", tags=["report"])
app.include_router(news_router, prefix="/news", tags=["news"])
app.include_router(map_router, tags=["map"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run("main:app", host=args.host, port=args.port, reload=False)
