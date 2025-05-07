from pydantic import BaseModel, constr
from typing import Annotated

class SUserAuth(BaseModel): 
    username: str
    password: str

class SUserCreate(BaseModel):
    username: Annotated[str, constr(strip_whitespace=True, min_length=3, max_length=50)]
    password: Annotated[str, constr(min_length=6, max_length=100)]

class SUserPublic(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}