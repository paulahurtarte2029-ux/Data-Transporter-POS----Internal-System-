import os

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
EXPORT_FILE = os.getenv("EXPORT_FILE", "output/recurrente_transactions.csv")