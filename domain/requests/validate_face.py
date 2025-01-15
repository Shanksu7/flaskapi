from pydantic import BaseModel


class ValidateFace(BaseModel):
    imageb64: str