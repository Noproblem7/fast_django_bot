from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy import or_
from fastapi_app.app.database import ENGINE, Session
from fastapi_app.app.models import User, Post
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi_app.app.schemas.post_schema import PostCreateSchema, PostUpdateSchema
from fastapi_pagination import Page, paginate, add_pagination

session = Session(bind=ENGINE)

post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.get('/', response_model=Page)
async def get_users():
    all_posts = session.query(Post).all()
    return jsonable_encoder(paginate(all_posts))

add_pagination(post_router)


@post_router.get("/")
async def get_posts(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(
            or_(
                User.username == Authorization.get_jwt_subject(),
                User.email == Authorization.get_jwt_subject()
            )).first()
        if check_user:
            posts = session.query(Post).filter(Post.user == check_user).all()
            return jsonable_encoder(posts)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER Not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@post_router.post("/create")
async def create_post(post: PostCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        current_user = session.query(User).filter(
            or_(
                User.username == Authorization.get_jwt_subject(),
                User.email == Authorization.get_jwt_subject()
            )).first()
        if current_user:
            new_post = Post(
                caption=post.caption,
                image_path=post.image_path,
            )
            new_post.user = current_user

            session.add(new_post)
            session.commit()

            data = {
                "code": 200,
                "success": True,
                "message": f"Successfully created post {Authorization.get_jwt_subject()}",
            }
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@post_router.put("/{id}")
async def update_router(id: int, post: PostUpdateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            check_post = session.query(Post).filter(Post.id == id).first()
            if check_post:
                for key, value in post.dict().items():
                    setattr(check_post, key, value)

                    data = {
                        "code": 200,
                        "success": True,
                        "message": "Successfully updated post",
                        "object": {
                            "caption": check_post.caption,
                            "user_id": check_post.id,
                            "image_path": check_post.image_path,
                        }
                    }
                    session.add(check_post)
                    session.commit()
                    return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@post_router.delete("/{id}")
async def delete_post(id: int, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            post = session.query(Post).filter(Post.id == id).first()
            if post:
                session.delete(post)
                session.commit()
                return jsonable_encoder({"code": 200, "message": "Successfully deleted post"})
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
