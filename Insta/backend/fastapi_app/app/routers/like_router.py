import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_app.app.models import Likes, User
from fastapi_app.app.schemas.like_schema import LikeCreateSchema
from fastapi_app.app.database import ENGINE, Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_

session = Session(bind=ENGINE)

like_router = APIRouter(prefix="/likes", tags=["likes"])


@like_router.get("/")
async def get_likes(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()

        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject()
            )).first()
        if current_user:
            likes = session.query(Likes).all()
            return jsonable_encoder(likes)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not logged in")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@like_router.post("/create")
async def create_like(like: LikeCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        current_user = session.query(User).filter(
            or_(
                User.username == Authorization.get_jwt_subject(),
                User.email == Authorization.get_jwt_subject()
            )).first()
        if current_user:
            new_like = Likes(
                user_id=like.user_id,
                post_id=like.post_id,
            )
            new_like.user = current_user

            session.add(new_like)
            session.commit()

            data = {
                "code": 200,
                "success": True,
                "message": f"Successfully created like {Authorization.get_jwt_subject()}",
            }
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
