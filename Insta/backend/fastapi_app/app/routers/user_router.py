import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_app.app.schemas.user_schema import UserRegisterSchema, UserLoginSchema
from fastapi_app.app.database import Session, ENGINE
from fastapi_app.app.models import User
from fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi_pagination import add_pagination, paginate, Page
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

session = Session(bind=ENGINE)

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get('/', response_model=Page)
async def get_users():
    all_posts = session.query(User).all()
    return jsonable_encoder(paginate(all_posts))

add_pagination(user_router)


@user_router.get('/')
async def get_user(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            user = session.query(User).all()
            return jsonable_encoder(user)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@user_router.post("/register")
async def user_register(request: UserRegisterSchema):
    check_user = session.query(User).filter(
        or_(
            User.username == request.username,
            User.email == request.email
        )
    ).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(
        username=request.username,
        email=request.email,
        password=generate_password_hash(request.password)
    )
    session.add(new_user)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="User registered")


@user_router.post('/login')
async def login_user(user: UserLoginSchema, Authorizotion: AuthJWT = Depends()):
    check_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )).first()
    if check_user and check_password_hash(check_user.password, user.password):
        access_token = Authorizotion.create_access_token(subject=check_user.username,
                                                         expires_time=datetime.timedelta(days=1))
        refresh_token = Authorizotion.create_refresh_token(subject=check_user.username,
                                                           expires_time=datetime.timedelta(days=3))
        data = {
            "success": True,
            "code": 200,
            "message": "Login successful",
            "token": {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password or username")
