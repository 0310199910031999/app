import sys
import os
import sys, os
sys.path.append(os.path.dirname(__file__))
import importlib.util
from fastapi import FastAPI, APIRouter
from shared.db import engine, Base
from mainContext.infrastructure import models  # Asegura que los modelos se registren

# Asegura que el path base esté incluido
sys.path.append(os.path.dirname(__file__))

# Inicializa la app
app = FastAPI(
    title="DAL FastAPI",
    description="A DAL Dealer Group FastAPI application with PostgreSQL and SQLAlchemy",
    version="1.0.0",
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