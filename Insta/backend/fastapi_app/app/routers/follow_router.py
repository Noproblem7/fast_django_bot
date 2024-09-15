import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_app.app.models import Followers, User
from fastapi_app.app.schemas.follow_schema import FollowCreateSchema
from fastapi_app.app.database import ENGINE, Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_

session = Session(bind=ENGINE)

follow_router = APIRouter(prefix="/follow", tags=["Follow"])


@follow_router.get("/")
async def get_follow(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject()
            )).first()
        if current_user:
            follow = session.query(Followers).all()
            return jsonable_encoder(follow)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not logged in")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@follow_router.post("/create")
async def create_follow(follow: FollowCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        current_user = session.query(User).filter(
            or_(
                User.username == Authorization.get_jwt_subject(),
                User.email == Authorization.get_jwt_subject()
            )).first()
        if current_user:
            new_follow = Followers(
                follower_id=follow.follower_id,
                following_id=follow.following_id,
            )
            new_follow.user = current_user

            session.add(new_follow)
            session.commit()

            data = {
                "code": 200,
                "success": True,
                "message": f"Successfully created follow {Authorization.get_jwt_subject()}",
            }
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
