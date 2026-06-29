import pandas as pd
from models import WebhookTransaction


class TransactionStore:

    COLUMNS = [
        "event_id",
        "event_type",
        "transaction_id",
        "amount",
        "currency",
        "status",
        "customer_email",
        "customer_name",
        "internal_user_id",
        "raw_payload",
    ]

    def __init__(self):
        self.transactions_df = pd.DataFrame(columns=self.COLUMNS)

    def add_transaction(self, transaction: WebhookTransaction):

        row = transaction.model_dump()

        if row["event_id"] in self.transactions_df["event_id"].values:
            return self.transactions_df

        new_row = pd.DataFrame([row])

        self.transactions_df = pd.concat(
            [self.transactions_df, new_row],
            ignore_index=True
        )

        return self.transactions_df

    def get_dataframe(self):

        return self.transactions_df.copy()