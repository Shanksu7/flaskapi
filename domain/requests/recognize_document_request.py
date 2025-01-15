from pydantic import BaseModel


class RecognizeDocumentRequest(BaseModel):
    b64: str
    type: str