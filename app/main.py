from fastapi import FastAPI
from app.routers import graph

app = FastAPI()
app.include_router(graph.router)
