from pydantic import BaseModel

class ValidateFaceResponse(BaseModel):
    hasFace: bool
