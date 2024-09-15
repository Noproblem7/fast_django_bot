from pydantic import BaseModel
from typing import Optional


class FollowCreateSchema(BaseModel):
    follower_id: Optional[str]
    following_id: Optional[str]