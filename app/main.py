from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import health_router
from app.routes.token_info import token_info_router
from app.routes.top_nfts import top_nfts_router
from app.routes.top_pump_tokens_by_mc import top_pump_tokens_mc_router
from app.routes.top_pump_tokens_gt_10k_mc import top_pump_tokens_gt_10k_mc_router
from app.routes.nft_info import nft_info_router

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
app.include_router(token_info_router,prefix="/data-api", tags=["Token Details"])

# nft info
app.include_router(nft_info_router,prefix="/data-api",tags=["NFT"])

# top traded nfts
app.include_router(top_nfts_router, prefix="/data-api", tags=["NFT"])

# top pump fun tokens by MC
app.include_router(top_pump_tokens_mc_router,prefix="/data-api",tags=["Pump Fun"])

# top pump fun tokens above 10K MC
app.include_router(top_pump_tokens_gt_10k_mc_router,prefix="/data-api",tags=["Pump Fun"])