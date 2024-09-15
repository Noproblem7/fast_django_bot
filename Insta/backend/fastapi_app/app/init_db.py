from .database import Base, ENGINE
from .models import User, Post, Tags, Messages, Comments, Followers, Likes, PostTags

def migrate():
    Base.metadata.create_all(bind=ENGINE)