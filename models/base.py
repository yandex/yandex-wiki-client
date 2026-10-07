from pydantic.v1 import BaseModel


class _Base(BaseModel):
    class Config:
        extra = 'ignore'
        allow_population_by_field_name = True
