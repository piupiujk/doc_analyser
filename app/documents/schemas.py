from pydantic import BaseModel


class SDoc(BaseModel):
    image_base64: str


class UploadDeleteResponse(BaseModel):
    status_code: int
    id: int
    message: str
