from models import WebhookTransaction

# takes transaction information in JSON form and converts it into an internal object
# WebhookTransaction

def parse_recurrente_payload(payload: dict) -> WebhookTransaction:
    data = payload.get("data", {})
    user = data.get("user", {})
    metadata = data.get("metadata", {})

    return WebhookTransaction(
        event_id=payload.get("id"),
        event_type=payload.get("event"),
        transaction_id=data.get("id"),
        amount=data.get("amount"),
        currency=data.get("currency"),
        status=data.get("status"),
        customer_email=user.get("email"),
        customer_name=user.get("name"),
        internal_user_id=metadata.get("user_id_interno"),
        raw_payload=payload,
    )