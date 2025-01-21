# items.py
from http.client import HTTPException
from fastapi import APIRouter, FastAPI, Body
from fastapi.responses import JSONResponse
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
from io import BytesIO
import numpy as np
import base64
from pydantic import BaseModel
from domain.requests.recognize_document_request import RecognizeDocumentRequest
from domain.responses.recognize_document_response import RecognizeDocumentResponse
from domain.responses.validate_face_response import ValidateFaceResponse
from domain.base.api_response import ApiResponse
from domain.base.status import Status

# Crear una instancia de APIRouter
router = APIRouter()
print('starting setup keras')

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("dataset/keras_model.h5", compile=False)

# Load the labels
class_names = open("dataset/labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
print('finished setup keras')
# Replace this with the path to your image

@router.post("/rec/base64", response_model=ApiResponse[RecognizeDocumentResponse])
def read_item(request: RecognizeDocumentRequest):   
    try:    
        if ',' in request.b64:
            request.b64 = request.b64.split(',')[1]  # Take only the Base64-encoded part
        
        # Add padding if necessary
        missing_padding = len(request.b64) % 4
        if missing_padding:
            request.b64 += "=" * (4 - missing_padding)  # Add the padding to the base64 string

        image = Image.open(BytesIO(base64.b64decode(request.b64)))
        
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        # Turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        
        # Load the image into the array
        data[0] = normalized_image_array

        # Predict using the model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]    
        ismatch = class_name[2:].strip() == request.type

        print(class_name)
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", confidence_score)
        print("match: ", ismatch)
        documentData =  RecognizeDocumentResponse(name=class_name[2:].strip(), score=confidence_score*100, match=ismatch )
        result = ApiResponse(error=False, data=documentData, status=Status.OK).model_dump()
        return result
    
    except Exception as e:
        # Converting result to string for detail
        result = ApiResponse(error=True, message=str(e), status=Status.BAD_REQUEST)
        raise HTTPException(status_code=400, detail=str(result.model_dump()))  # Pass string to detail
