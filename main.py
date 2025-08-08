import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routers import index as indexRoute

from api.routers import orders, reports, reviews, recipes, resources, sandwiches, payments, promo_codes

from api.models import model_loader
from api.dependencies.config import conf
from api.dependencies.database import engine, Base
from api.models.orders import Order


print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully")

app = FastAPI()

origins = ["*"]


app.include_router(orders.router)

app.include_router(sandwiches.router)
app.include_router(payments.router)
app.include_router(reviews.router)
app.include_router(recipes.router)
app.include_router(resources.router)
app.include_router(promo_codes.router)
app.include_router(reports.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()

# indexRoute.load_routes(app)




if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)