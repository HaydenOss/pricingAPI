from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.import_export import download, upload
from app.routes.services import stores

app = FastAPI()

app.include_router(upload.router, prefix="/upload")
app.include_router(download.router, prefix="/download")
app.include_router(stores.router, prefix="/services")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
def home() -> None:
    return {"Something"}
