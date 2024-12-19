from fastapi import APIRouter
from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()
bitquery_access_token = os.getenv("BITQUERY_ACCESS_TOKEN")

top_nfts_router = APIRouter()

url = "https://streaming.bitquery.io/eap"


@top_nfts_router.get("/top-nfts")
def token_info():
    payload = json.dumps(
        {
            "query": '{\n  Solana {\n    DEXTradeByTokens(\n      orderBy: {descendingByField: "amt"}\n      where: {Trade: {Currency: {Fungible: false}}}\n      limit: {count: 5}\n    ) {\n      Trade {\n        Dex {\n          ProtocolFamily\n        }\n        Currency {\n          Symbol\n          CollectionAddress\n        }\n      }\n      amt: sum(of: Trade_Amount)\n    }\n  }\n}\n',
            "variables": "{}",
        }
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bitquery_access_token}",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_details = response.json()["data"]["Solana"]
    print(response_details)
    return {
        "status": "success",
        "message": "There are the top 5 Most Traded NFTs Recently",
        "data": response_details,
    }
