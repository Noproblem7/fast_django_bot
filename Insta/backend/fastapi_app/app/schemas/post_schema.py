from pydantic import BaseModel
from typing import Optional


class PostCreateSchema(BaseModel):
    caption: Optional[str]
    image_path: Optional[str]


class PostUpdateSchema(BaseModel):
    caption: Optional[str]
    image_path: Optional[str]
