import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from fastapi import FastAPI
from .routers import menu_item_popularity
from .routers import feedback_with_low_rating


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)
app.include_router(menu_item_popularity.router)
app.include_router(feedback_with_low_rating.router)



if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)