import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .routers import orders, reports, payments
from .models import model_loader
from .dependencies.config import conf
from .dependencies.database import engine, Base
from .models.orders import Order


print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully")

app = FastAPI()

origins = ["*"]


app.include_router(orders.router)
app.include_router(reports.router)
app.include_router(payments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)