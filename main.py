from fastapi import FastAPI
from routers.auth import auth_router
from routers.post import post_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(post_router)
