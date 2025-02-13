from fastapi import FastAPI

from config import settings
from container import Container
from interfaces.api.billing_router import router as billing_router

app = FastAPI(title="Billing API", version="1.0")

container = Container()
container.wire(modules=["interfaces.api.billing_router"])

app.include_router(billing_router)


@app.get("/")
def read_root():
    return {"message": settings.PROJECT_NAME}
