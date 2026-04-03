# Deepgram Drinks - Voice Ordering System

A production-ready voice ordering system built with **FastAPI**, **Twilio**, and **Deepgram Agent API**. Features real-time voice conversations, SMS notifications, and live order dashboards.

## What is Deepgram Drinks?

Deepgram Drinks is an AI-powered voice ordering system that allows customers to call a phone number and place drink orders through natural conversation. The system uses advanced speech recognition, natural language processing, and text-to-speech to create a seamless ordering experience.

The menu is fully configurable via `app/menu_config.json`, currently set up for an espresso/coffee cart (latte, cappuccino, espresso, americano, macchiato, hot chocolate).

### Key Features

-  **Natural Voice Ordering**: Customers call and speak naturally to place orders
-  **AI-Powered Assistant**: Uses Deepgram's Agent API for intelligent conversation
-  **SMS Notifications**: Automatic order confirmations and ready notifications
-  **Real-time Dashboards**: Live order tracking for staff and customers
-  **Production Ready**: Containerized, scalable, and secure

## Demo

### How It Works

1. **Customer calls** your Twilio phone number
2. **AI greets** them: "Hey! Welcome to Deepgram Drinks. What can I get started for you?"
3. **Natural conversation** - Customer says: "I'd like a latte with vanilla syrup"
4. **AI confirms** order details and asks for phone number
5. **Order placed** - Customer receives SMS confirmation with order number
6. **Staff sees** order on dashboard and prepares it
7. **Ready notification** - Customer gets SMS when order is ready

### Sample Conversation

```
Customer: "Hi, I'd like a cappuccino with soy milk"
AI: "One cappuccino with soy milk. Is that correct?"
Customer: "Yes, that's right"
AI: "Great! Would you like anything else?"
Customer: "No, that's all"
AI: "Can I please get your phone number for this order?"
Customer: "555-123-4567"
AI: "Thank you! Your order number is 4782. We'll text you when it's ready for pickup!"
```

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Customer      │    │   Twilio Voice   │    │   Your Server   │
│   (Phone Call)  │◄──►│   (Webhook)      │◄──►│   (FastAPI)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │  Deepgram Agent │
                                               │(STT + LLM + TTS)│
                                               └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │  Twilio SMS     │
                                               │  (Notifications)│
                                               └─────────────────┘
```

### Core Components

- **FastAPI Backend**: REST API + WebSocket bridge for audio streaming
- **Deepgram Agent**: Real-time speech-to-text, LLM reasoning, text-to-speech
- **Twilio Integration**: Voice calls + SMS notifications
- **Real-time Dashboard**: Server-Sent Events for live order updates
- **Containerized**: Podman/Docker with production-ready configuration

## Quick Start

### Prerequisites

- Python 3.11+
- Podman or Docker
- ngrok (for local testing)
- Twilio account with A2P 10DLC approval
- Deepgram API key

### 5-Minute Setup

```bash
# 1. Clone and setup
git clone <repo-url>
cd flux-twilio-voice-assistant
cp sample.env.txt .env

# 2. Edit .env with your API keys
# - Get Deepgram API key: https://console.deepgram.com/
# - Get Twilio credentials: https://console.twilio.com/

# 3. Start the application
./podman-start.sh

# 4. Expose to internet (separate terminal)
ngrok http 8000

# 5. Configure Twilio webhook
# Use ngrok URL: https://your-ngrok-url.ngrok-free.app/voice
```

### Test Your Setup

1. **Call your Twilio number** - You should hear the AI greeting
2. **Place a test order** - Try: "I'd like a latte with vanilla syrup"
3. **Check dashboards** - Visit `http://localhost:8000/orders` and `http://localhost:8000/staff`

### Production Deployment

For production deployment on AWS EC2, see the guides in `documentations/` (note: these were written for the original "BobaRista" deployment and still reference that branding, but the setup steps are the same):

- **[Deployment Guide](documentations/doc-04-deployment.md)** - Complete production setup
- **[AWS EC2 Setup](documentations/doc-02-ec2-setup.md)** - Server configuration
- **[Twilio Setup](documentations/doc-03-twilio-setup.md)** - Phone number configuration
- **[Architecture Guide](documentations/doc-05-architecture.md)** - System design details

## Project Structure

```
flux-twilio-voice-assistant/
├── app/                          # Main application code
│   ├── main.py                   # FastAPI application entrypoint
│   ├── app_factory.py            # Application factory with lifecycle hooks
│   ├── settings.py               # Configuration and environment variables
│   ├── http_routes.py            # REST endpoints (Twilio webhooks, dashboards)
│   ├── ws_bridge.py              # WebSocket bridge for Twilio <> Deepgram audio
│   ├── agent_client.py           # Deepgram Agent API client
│   ├── agent_functions.py        # AI tool definitions and state management
│   ├── business_logic.py         # Core business logic (menu, cart, orders)
│   ├── menu_config.json          # Menu and branding configuration
│   ├── orders_store.py           # Thread-safe JSON persistence layer
│   ├── events.py                 # Pub/sub system for real-time updates
│   ├── audio.py                  # Audio format conversion (u-law <> Linear16)
│   ├── send_sms.py               # Twilio SMS integration
│   ├── session.py                # User session management
│   ├── call_logger.py            # Call logging and debugging
│   ├── order_ids.py              # Order ID generation utilities
│   └── orders.json               # Order storage (auto-reset on startup)
│
├── documentations/               # Comprehensive documentation
├── Containerfile                 # Podman/Docker build configuration
├── podman-start.sh               # Local development script
├── podman-stop.sh                # Cleanup script
├── requirements.txt              # Python dependencies
├── sample.env.txt                # Environment variables template
└── README.md                     # This file
```

## Technical Details

### Audio Processing Pipeline

1. **Twilio Input**: u-law 8kHz audio from phone calls
2. **Resampling**: Convert to Linear16 48kHz for Deepgram
3. **Deepgram Processing**: STT -> LLM reasoning -> TTS
4. **Output**: Convert back to u-law 8kHz for Twilio

### AI Agent Configuration

- **STT Model**: `flux-general-en` (real-time speech recognition)
- **LLM Model**: `gemini-2.5-flash` (reasoning and responses)
- **TTS Model**: `aura-2-odysseus-en` (natural voice synthesis)
- **Language**: English (`en`)

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/voice` | POST | Twilio webhook (call initiation) |
| `/twilio` | WS | WebSocket for audio streaming |
| `/orders` | GET | TV dashboard (large display) |
| `/staff` | GET | Staff console interface |
| `/orders.json` | GET | Orders data (JSON API) |

## Environment Configuration

Create `.env` file with required variables:

```bash
# Server Configuration
VOICE_HOST=your-domain.com

# Deepgram API
DEEPGRAM_API_KEY=your_deepgram_key

# Twilio Voice (calls)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_E164=+1234567890
TWILIO_TO_E164=+1234567890

# Twilio SMS (notifications)
MSG_TWILIO_ACCOUNT_SID=your_msg_account_sid
MSG_TWILIO_AUTH_TOKEN=your_msg_auth_token
MSG_TWILIO_FROM_E164=+1234567890

# Agent Configuration
AGENT_LANGUAGE=en
AGENT_TTS_MODEL=aura-2-odysseus-en
AGENT_STT_MODEL=flux-general-en
```

## Monitoring & Debugging

```bash
# View application logs
podman logs -f dg-drinks

# View specific log levels
podman logs dg-drinks | grep ERROR
```

## Troubleshooting

**Call not connecting?**
- Check if ngrok is running: `curl https://your-ngrok-url.ngrok-free.app/voice`
- Verify Twilio webhook URL is correct and uses HTTPS
- Check application logs: `podman logs -f dg-drinks`

**No audio on call?**
- Ensure WebSocket URL uses `wss://` (not `ws://`)
- Check Deepgram API key is valid
- Verify `VOICE_HOST` matches your ngrok URL exactly

**SMS not sending?**
- Verify Twilio SMS credentials in `.env`
- Check phone number has SMS capability
- Review Twilio logs in console

```bash
# Restart application
./podman-stop.sh && ./podman-start.sh

# Test endpoints
curl http://localhost:8000/orders.json
```
