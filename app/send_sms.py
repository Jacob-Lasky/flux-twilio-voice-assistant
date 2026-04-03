# app/send_sms.py
import os
import re
from dotenv import load_dotenv
from twilio.rest import Client
from .business_logic import CONFIG

load_dotenv()

SID  = os.environ.get("MSG_TWILIO_ACCOUNT_SID")
TOK  = os.environ.get("MSG_TWILIO_AUTH_TOKEN")
FROM = os.environ.get("MSG_TWILIO_FROM_E164")

_client = Client(SID, TOK) if SID and TOK else None
E164_RE = re.compile(r"^\+\d{10,15}$")

_SMS = CONFIG.get("sms", {})
_BRAND = CONFIG["brand"]

def _fmt(template: str, order_no: str) -> str:
    return template.format(
        brand_name=_BRAND["name"],
        brand_emoji=_BRAND["emoji"],
        order_number=order_no,
    )

def _ok_e164(p: str | None) -> bool:
    return bool(p and E164_RE.fullmatch(p))

def send_received_sms(order_no: str, to_phone_no: str):
    """Confirmation SMS (sent right after order is placed)."""
    if not _client:
        print("❌ Twilio client not configured"); return None
    if not _ok_e164(to_phone_no):
        print(f"❌ Invalid E.164 phone for SMS: {to_phone_no}"); return None
    print(f"📱 SMS (received) to {to_phone_no}: order {order_no}")
    body = _fmt(_SMS.get("order_received",
        "Thanks for your order with {brand_name}! {brand_emoji} Your order number is {order_number}. We’ll text you again when it’s ready for pickup.\nReply STOP to opt out."
    ), order_no)
    return _client.messages.create(from_=FROM, to=to_phone_no, body=body)

def send_ready_sms(order_no: str, to_phone_no: str):
    """Notify order is ready (triggered by /staff Done)."""
    if not _client:
        print("❌ Twilio client not configured"); return None
    if not _ok_e164(to_phone_no):
        print(f"❌ Invalid E.164 phone for SMS: {to_phone_no}"); return None
    print(f"📱 SMS (ready) to {to_phone_no}: order {order_no}")
    body = _fmt(_SMS.get("order_ready",
        "Hi! Your order #{order_number} is now ready for pickup at {brand_name}. {brand_emoji} See you soon!\nReply STOP to opt out."
    ), order_no)
    return _client.messages.create(from_=FROM, to=to_phone_no, body=body)
