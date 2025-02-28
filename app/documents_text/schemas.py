from pydantic import BaseModel


class Analyse(BaseModel):
    status_code: int
    id: int
    message: str
