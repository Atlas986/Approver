import pydantic
class BaseModel(pydantic.BaseModel):
    class Config:
        from_attributes = True
        strict = False
from . import scripts, utils, outer_models
from .database import engine