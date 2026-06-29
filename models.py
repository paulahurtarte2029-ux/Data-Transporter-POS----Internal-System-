from pydantic import BaseModel
from typing import Optional, Dict, Any

class WebhookTransaction(BaseModel):
    event_id: Optional[str]
    event_type: Optional[str]
    transaction_id: Optional[str]
    amount: Optional[float]
    currency: Optional[str]
    status: Optional[str]
    customer_email: Optional[str]
    customer_name: Optional[str]
    internal_user_id: Optional[str]
    raw_payload: Dict[str, Any]