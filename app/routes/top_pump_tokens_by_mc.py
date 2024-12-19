from fastapi import APIRouter
from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()
bitquery_access_token = os.getenv("BITQUERY_ACCESS_TOKEN")

top_pump_tokens_mc_router = APIRouter()

url = "https://streaming.bitquery.io/eap"


@top_pump_tokens_mc_router.get("/top-pump-tokens-mc")
def token_info():
    payload = json.dumps(
        {
            "query": '{\n  Solana {\n    DEXTrades(\n      limitBy: {by: Trade_Buy_Currency_MintAddress, count: 1}\n      orderBy: {descending: Trade_Buy_Price}\n      where: {Trade: {Dex: {ProtocolName: {is: "pump"}}, Buy: {Currency: {MintAddress: {notIn: ["11111111111111111111111111111111"]}}}}, Transaction: {Result: {Success: true}}}\n      limit: {count: 5}\n    ) {\n      Trade {\n        Buy {\n          Price\n          PriceInUSD\n          Currency {\n            Name\n            Symbol\n            MintAddress\n            Decimals\n            Fungible\n            Uri\n          }\n        }\n      }\n    }\n  }\n}\n',
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
        "message": "These are the top 5 Pump Fun tokens based on Marketcap",
        "data": response_details,
    }
