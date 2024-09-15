from pydantic import BaseModel
from typing import Optional


class LikeCreateSchema(BaseModel):
    user_id: Optional[str]
    post_id: Optional[str]