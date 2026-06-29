from fastapi import FastAPI, Request, Header, HTTPException

from config import WEBHOOK_SECRET
from processor import parse_recurrente_payload
from pandas_converter import TransactionStore

# 1. receives transaction info from Recurrente webhook
# 2. stores information in internal structure Webhook Transaction (processor.py)
# 3. stores it in pandas dataframe (pandas_converter.py)
# 4. allows central program to access pandas dataframe

app = FastAPI()

transaction_store = TransactionStore()

@app.get("/")
def health_check():
    return {"status": "running"}

# this function is the automatic webhook endpoint that Recurrente will call 
# when a transaction is made
# function is automatically called whenever a trasnaction request is made through FastAPI

# FastAPI builds an internal routing table used for mapping by giving a URL path
# this automates the async function recurrente_webhook to be called whenever
# a request is made following a transaction processed by Recurrente app. 
@app.post("/webhooks/recurrente")
async def recurrente_webhook(
    request: Request,
    x_webhook_secret: str | None = Header(default=None)
):
    if WEBHOOK_SECRET and x_webhook_secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret")

    payload = await request.json()
    transaction = parse_recurrente_payload(payload)
    df = transaction_store.add_transaction(transaction)

    return {
        "received": True,
        "transaction_id": transaction.transaction_id,
        "current_dataframe_rows": len(df)
    }

def get_recurrente_dataframe():
    return transaction_store.get_dataframe()