import sys
import os
import sys, os
sys.path.append(os.path.dirname(__file__))
import importlib.util
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from shared.db import engine, Base
from mainContext.infrastructure import models  # Asegura que los modelos se registren

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

app.mount("/static", StaticFiles(directory="mainContext/static"), name="static")

@app.get("/")
def read_root():
    return {"mensaje": "Funcionando"}