from fastapi import FastAPI, Request, Header, HTTPException

from config import WEBHOOK_SECRET
from processor import parse_recurrente_payload
from pandas_converter import TransactionStore

app = FastAPI()

transaction_store = TransactionStore()

@app.get("/")
def health_check():
    return {"status": "running"}

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