from fastapi import FastAPI
from app.api.routes import user, image
from app.containers import Container
from fastapi.openapi.utils import get_openapi
from app.core.logging_config import setup_logger

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="Image Gallery API with JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def create_app() -> FastAPI:
    container = Container()
    container.init_resources()
    app = FastAPI()
    app.container = container

    logger = setup_logger()
    app.state.logger = logger

    app.include_router(user.router, prefix="/users", tags=["Users"])
    app.include_router(image.router, prefix="/images", tags=["Images"])
    
    app.openapi = lambda: custom_openapi(app)

    return app

app = create_app()