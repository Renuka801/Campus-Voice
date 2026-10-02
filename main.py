from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth_routes, complaint_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Voice API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your frontend URL before going live
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(complaint_routes.router)


@app.get("/")
def root():
    return {"message": "Campus Voice API is running"}
