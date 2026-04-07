# app/settings.py
import os
from dotenv import load_dotenv
from .business_logic import CONFIG

load_dotenv()

VOICE_HOST = os.getenv("VOICE_HOST", "localhost:8000")
DG_API_KEY = os.environ["DEEPGRAM_API_KEY"]

AGENT_LANGUAGE = os.getenv("AGENT_LANGUAGE", "en")
SPEAK_PROVIDER = {"type": "deepgram", "model": os.getenv("AGENT_TTS_MODEL", "aura-2-odysseus-en")}
LISTEN_PROVIDER = {"type": "deepgram", "model": os.getenv("AGENT_STT_MODEL", "flux-general-en")}
THINK_PROVIDER  = {"type": "anthropic", "model": os.getenv("AGENT_THINK_MODEL", "claude-4-5-haiku-latest")}

# --- Build prompt from config template ---
def _build_prompt() -> str:
    cfg = CONFIG
    menu = cfg["menu"]
    limits = cfg["limits"]

    drinks_list = ", ".join(d.title() for d in menu["drinks"])
    addons_list = "\n".join(a.title() for a in menu.get("addons", []))
    sweetness_list = "\n".join(s.title() for s in menu["sweetness_levels"])

    return cfg["voice_prompt_template"].format(
        brand_name=cfg["brand"]["name"],
        menu_intro=cfg["menu_intro"],
        drinks_list=drinks_list,
        addons_list=addons_list,
        sweetness_list=sweetness_list,
        max_drinks=limits["max_drinks_per_order"],
        max_active=limits["max_active_drinks_per_phone"],
    )

AGENT_PROMPT = _build_prompt()

def build_deepgram_settings() -> dict:
    return {
        "type": "Settings",
        "audio": {
            "input":  {"encoding": "linear16", "sample_rate": 48000},
            "output": {"encoding": "linear16", "sample_rate": 24000, "container": "none"},
        },
        "agent": {
            "language": AGENT_LANGUAGE,
            "listen": {"provider": LISTEN_PROVIDER},
            "think": {
                "provider": THINK_PROVIDER,
                "prompt": AGENT_PROMPT,
            },
            "speak": {"provider": SPEAK_PROVIDER},
            "greeting": CONFIG["greeting"],
        },
    }
