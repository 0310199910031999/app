import sys
import os
import sys, os
sys.path.append(os.path.dirname(__file__))
import importlib.util
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from shared.db import engine, Base
from mainContext.infrastructure import models  # Asegura que los modelos se registren
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

# Asegura que el path base esté incluido
sys.path.append(os.path.dirname(__file__))

# Inicializa la app
app = FastAPI(
    title="DAL FastAPI",
    root_path="/dal",
    description="A DAL Dealer Group FastAPI application with PostgreSQL and SQLAlchemy",
    version="1.0.0",
    swagger_ui_parameters={
        "docExpansion": "none",  # contrae todos los endpoints
    }

)


# === CONFIGURACIÓN CORS ===
origins = [
    "http://localhost",          # <--- ¡ESTE ES EL QUE TE FALTA! (Origen de Capacitor)
    "http://localhost:4200",     # Tu Angular en desarrollo web
    "http://10.0.2.2",           # IP mágica del emulador
    "http://10.0.2.2:8000",
    "*"                          # ÚSALO SOLO PARA PROBAR si sigue fallando
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,       # Usa True solo si usas cookies/token en headers
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MIDDLEWARE DE COMPRESIÓN GZIP ===
# Comprime respuestas mayores a 1KB (especialmente útil para imágenes y archivos grandes)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# === MIDDLEWARE DE CACHÉ PARA ARCHIVOS ESTÁTICOS ===
class StaticFileCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Agregar headers de caché solo para archivos estáticos
        if request.url.path.startswith("/static/"):
            # Cache por 1 año para archivos inmutables (imágenes, etc)
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
            response.headers["ETag"] = f'"{hash(request.url.path)}"'
            
            # Permitir caché en navegador y CDN
            response.headers["Pragma"] = "public"
            response.headers["Expires"] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', 
                                                        time.gmtime(time.time() + 31536000))
        
        return response

app.add_middleware(StaticFileCacheMiddleware)



# Función para incluir routers desde cualquier subpaquete
def include_routers_from_package(package):
    package_path = package.__path__[0]
    package_name = package.__name__

    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                rel_path = os.path.relpath(os.path.join(root, file), package_path)
                module_name = rel_path.replace(os.sep, ".").replace(".py", "")
                full_module_name = f"{package_name}.{module_name}"

                spec = importlib.util.find_spec(full_module_name)
                if spec:
                    module = importlib.import_module(full_module_name)
                    for attr in vars(module).values():
                        if isinstance(attr, APIRouter):
                            app.include_router(attr)

# Importa el paquete raíz de routers
import api.v1.routers
include_routers_from_package(api.v1.routers)


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import mimetypes

# Configurar tipos MIME adicionales para mejor rendimiento
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/avif', '.avif')

# Montar archivos estáticos con configuración optimizada
app.mount("/static", StaticFiles(directory="mainContext/static", html=False, check_dir=False), name="static")

@app.get("/")
def read_root():
    return {"mensaje": "Hola desde /dal"}
