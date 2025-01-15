# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from document import router as items_router 
from face import router as face_router
from fastapi.middleware.cors import CORSMiddleware

# Crear la instancia de FastAPI
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Incluir las rutas del router de items
app.include_router(items_router)
app.include_router(face_router)

# Ruta principal
@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')
