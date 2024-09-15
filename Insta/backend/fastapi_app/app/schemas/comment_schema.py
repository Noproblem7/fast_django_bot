from pydantic import BaseModel
from typing import Optional


class CommentCreateSchema(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    content: Optional[str]


class CommentUpdateSchema(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    content: Optional[str]
