from domain.base.status import Status
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
import base64
import numpy as np
import face_recognition
import cv2
from domain.requests.validate_face import ValidateFace
from domain.base.api_response import ApiResponse
from domain.responses.validate_face_response import ValidateFaceResponse

router = APIRouter()

@router.post("/validate-face/", response_model=ApiResponse[ValidateFaceResponse])
async def validate_face(input_data: ValidateFace):
    try:
        b64 = input_data.imageb64
        if ',' in input_data.imageb64:
            b64 = input_data.imageb64.split(',')[1]  # Take only the Base64-encoded part
        # Decodificar la imagen Base64
        image_data = base64.b64decode(b64)
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Validar si la imagen fue decodificada correctamente
        if image is None:
            raise HTTPException(status_code=400, detail="La imagen no es válida.")

        # Verificar si hay rostros en la imagen
        has_face = detect_faces(image)

        documentData = ValidateFaceResponse(hasFace=has_face)
        result = ApiResponse(error=False, data=documentData, status=Status.OK).model_dump()
        return result
    
    except Exception as e:
        result = ApiResponse(error=False, message=str(e), status=Status.INTERNAL_SERVER_ERROR)
        raise HTTPException(status_code=500, detail=result.model_dump())
    
def detect_faces(image: np.ndarray) -> bool:
    """
    Detecta rostros en la imagen utilizando la librería face-recognition.
    """
    # Convertir la imagen de BGR (OpenCV) a RGB (face-recognition usa RGB)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Detectar rostros en la imagen
    face_locations = face_recognition.face_locations(rgb_image)
    
    # Si se detectan rostros, devolver True
    return len(face_locations) > 0