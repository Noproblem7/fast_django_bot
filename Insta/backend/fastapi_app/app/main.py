from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from .routers.user_router import user_router
from .routers.post_router import post_router
from .routers.comment_router import comment_router
from .routers.like_router import like_router
from .routers.follow_router import follow_router
from .schemas.user_schema import Settings

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(post_router)
app.include_router(user_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(follow_router)
