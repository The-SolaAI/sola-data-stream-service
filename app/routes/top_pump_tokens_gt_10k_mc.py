from fastapi import APIRouter
from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()
bitquery_access_token = os.getenv("BITQUERY_ACCESS_TOKEN")

top_pump_tokens_gt_10k_mc_router = APIRouter()

url = "https://streaming.bitquery.io/eap"


@top_pump_tokens_gt_10k_mc_router.get("/top-pump-tokens-gt-10k-mc")
def token_info():
    payload = json.dumps(
        {
            "query": '{\n  Solana {\n    DEXTrades(\n      limitBy: {count: 1, by: Trade_Buy_Currency_MintAddress}\n      limit: {count: 5}\n      orderBy: {descending: Trade_Buy_Price}\n      where: {Trade: {Buy: {Price: {gt: 0.000001}, Currency: {MintAddress: {notIn: ["11111111111111111111111111111111"]}}}, Dex: {ProtocolName: {is: "pump"}}}, Transaction: {Result: {Success: true}}}\n    ) {\n      Trade {\n        Buy {\n          Currency {\n            Name\n            MintAddress\n            Uri\n          }\n        }\n        Sell {\n          Currency {\n            Name\n            Symbol\n            MintAddress\n            Decimals\n            Fungible\n            Uri\n          }\n        }\n      }\n    }\n  }\n}\n',
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
        "message": "These are the top 5 Pump Fun tokens above 10K Marketcap",
        "data": response_details,
    }
