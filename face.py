from domain.base.status import Status
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
from mtcnn import MTCNN
import base64
import numpy as np
from domain.requests.validate_face import ValidateFace
from domain.base.api_response import ApiResponse
from domain.responses.validate_face_response import ValidateFaceResponse

router = APIRouter()
# Initialize MTCNN face detector
detector = MTCNN()

def base64_to_image(base64_string):
    # Decode the base64 string
    img_data = base64.b64decode(base64_string)
    
    # Convert to image using PIL
    image = Image.open(BytesIO(img_data)).convert("RGB")
    
    # Convert the image to a NumPy array (OpenCV format)
    return np.array(image)

def has_face_val(base64_string):
    # Decode base64 to image
    image = base64_to_image(base64_string)

    # Detect faces
    faces = detector.detect_faces(image)

    # Return true if any faces are detected, otherwise false
    print(faces)
    return len(faces) > 0


@router.post("/validate-face/", response_model=ApiResponse[ValidateFaceResponse])
async def validate_face(input_data: ValidateFace):
    try:

        b64 = input_data.imageb64

        if b64 is None:
            raise HTTPException(status_code=400, detail="La imagen no es válida.")

        if ',' in input_data.imageb64:
            b64 = input_data.imageb64.split(',')[1]  # Take only the Base64-encoded part
        # Decodificar la imagen Base64

        # Verificar si hay rostros en la imagen
        has_face = has_face_val(b64)

        documentData = ValidateFaceResponse(hasFace=has_face)
        result = ApiResponse(error=False, data=documentData, status=Status.OK).model_dump()
        return result
    
    except Exception as e:
        result = ApiResponse(error=True, message=str(e), status=Status.BAD_REQUEST)
        return JSONResponse(content=result.dict(), status_code=400)