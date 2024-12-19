from fastapi import APIRouter
from app.data.nfts import NFT_SYMBOLS
from pydantic import BaseModel
import requests


class NftRequest(BaseModel):
    symbol: str


nft_info_router = APIRouter()


@nft_info_router.post("/nft-info")
def token_info(request: NftRequest):
    symbol = request.symbol
    symbol = symbol.lower()

    if symbol not in NFT_SYMBOLS:
        return {
            "status": "failed",
            "message": "opps we don't have the nft in our database yet.",
        }

    url = f"https://api-mainnet.magiceden.dev/v2/collections/{symbol}/stats"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    response_details = response.json()

    converted_details = {
        "symbol": response_details["symbol"],
        "floorPrice": response_details["floorPrice"] / 1_000_000_000,
        "listedCount": response_details["listedCount"],
        "avgPrice24hr": response_details["avgPrice24hr"] / 1_000_000_000,
        "volumeAll": response_details["volumeAll"] / 1_000_000_000,
    }

    return {
        "status": "success",
        "message": "This is the all time stats of the collection",
        "data": converted_details,
    }
