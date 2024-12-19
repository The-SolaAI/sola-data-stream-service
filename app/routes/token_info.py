from fastapi import APIRouter
from app.data.token_mapping import TOKENS
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
import requests
import json


class TokenRequest(BaseModel):
    symbol: str


load_dotenv()
bitquery_access_token = os.getenv("BITQUERY_ACCESS_TOKEN")

token_info_router = APIRouter()

url = "https://streaming.bitquery.io/eap"


@token_info_router.post("/token-info")
def token_info(request: TokenRequest):
    symbol = request.symbol
    symbol = symbol.upper()
    print(symbol)
    if symbol not in TOKENS:
        return {
            "status": "failed",
            "message": "opps we don't have the token in our database yet.",
        }

    current_time = datetime.utcnow()
    time_5min_ago = current_time - timedelta(minutes=5)
    time_1h_ago = current_time - timedelta(hours=1)

    variables = {
        "token": TOKENS[symbol]["MINT"],
        "side_token": "So11111111111111111111111111111111111111112",
        "pair_address": TOKENS[symbol]["PAIR"],
        "time_5min_ago": time_5min_ago.isoformat() + "Z",
        "time_1h_ago": time_1h_ago.isoformat() + "Z",
    }

    payload = json.dumps(
        {
            "query": "query MyQuery($token: String!, $side_token: String!, $pair_address: String!, $time_5min_ago: DateTime!, $time_1h_ago: DateTime!) {\n  Solana(dataset: realtime) {\n    DEXTradeByTokens(\n      where: {Transaction: {Result: {Success: true}}, Trade: {Currency: {MintAddress: {is: $token}}, Side: {Currency: {MintAddress: {is: $side_token}}}, Market: {MarketAddress: {is: $pair_address}}}, Block: {Time: {since: $time_1h_ago}}}\n    ) {\n      Trade {\n        Currency {\n          Name\n          MintAddress\n          Symbol\n        }\n        start: PriceInUSD(minimum: Block_Time)\n        min5: PriceInUSD(\n          minimum: Block_Time\n          if: {Block: {Time: {after: $time_5min_ago}}}\n        )\n        end: PriceInUSD(maximum: Block_Time)\n        Side {\n          Currency {\n            Symbol\n            Name\n            MintAddress\n          }\n        }\n        Dex {\n          ProtocolFamily\n        }\n        Market {\n          MarketAddress\n        }\n      }\n      sells_5min: count(\n        if: {Trade: {Side: {Type: {is: sell}}}, Block: {Time: {after: $time_5min_ago}}}\n      )\n    }\n  }\n}\n",
            "variables": json.dumps(variables),
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
        "message": "This is the token info from the past 1 hour",
        "data": response_details,
    }
