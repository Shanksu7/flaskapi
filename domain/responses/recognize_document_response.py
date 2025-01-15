from pydantic import BaseModel

class RecognizeDocumentResponse(BaseModel):
    name: str
    score: float
    match: bool
