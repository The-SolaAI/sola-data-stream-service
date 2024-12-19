from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import health_router
from app.routes.token_info import token_info_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "This is Sola AI data stream service"}


# health route
app.include_router(health_router, prefix="/data-api", tags=["Health"])

# token info
app.include_router(token_info_router,prefix="/token-info", tags=["Token Details"])