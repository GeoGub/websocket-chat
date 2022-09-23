from pydantic import BaseModel
from fastapi import Query

def to_camel(string):
    split_string = string.split("_")
    if split_string == 1:
        return string
    camel_case_string = split_string[0] + ''.join(item.title() for item in split_string[1:])
    return camel_case_string


class CamalModel(BaseModel):

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

class Params(BaseModel):
    limit: int = Query(50, ge=1, le=100, description="Limit items on page")
    offset: int = Query(0, ge=0, description="Page number")

class Meta(Params):
    total: int