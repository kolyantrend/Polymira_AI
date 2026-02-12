# 🔮 Polymira AI — Prediction Market Oracle

![Polymira Banner](https://pub-7341693284a64271b79b1b4630d3e1eb.r2.dev/polymira%20(20).jpeg)

Polymira is an autonomous AI agent built for the **Colosseum Agent Hackathon 2026**.  
It operates as an intelligent layer on top of **Polymarket**, combining real-time market data with **Gemini 2.0 Flash** reasoning to detect mispriced prediction markets and surface high-probability insights.

Polymira runs continuously, researches independently, and publishes actionable forecasts without human intervention.

---

## 🚀 Key Features

- 🤖 **Autonomous Agent (24/7)** - Continuous monitoring and analysis via systemd service
- 🔍 **Deep Research Engine** - Gemini 2.0 Flash + Google Search Grounding
- 📊 **700+ Events** - Across 12 Polymarket categories
- 🎯 **Edge Detection** - AI probability vs market odds analysis
- 💎 **Solana Integration** - Phantom Wallet (Desktop & Mobile)
- 📱 **Mobile Deep Linking** - Seamless wallet connection on mobile devices
- 🏆 **Reputation System** - Leaderboard tracking (buyers, likers, sharers)
- 🐦 **Social Sharing** - Twitter/X integration with verification
- 🔐 **Secure Payments** - 0.01 SOL per prediction unlock (Devnet)
- 🎨 **Modern UI** - Tailwind CSS + Three.js animations
- ⚡ **Real-time Updates** - Live feed with pagination
- 🔒 **Rate Limiting** - Built-in security features

---

## 🧠 Agentic Decision Logic

```
Edge = True_Probability (AI) − Market_Probability (Polymarket)
```

If `Edge > 10%`, Polymira automatically publishes a prediction card and updates the database.

---

## ⚡ Live Demo (Solana Devnet)

### Polymira is an AI-powered forecasting system that operates 24/7, providing automated market analysis. It automatically searches for forecasts, analyzes them, and generates results, as well as updates them on Github.

1. Visit [https://forecasts.polymira.org/](https://forecasts.polymira.org/)
2. Switch network in Phantom wallet (Settings → Developer settings → Solana Devnet)
3. Get SOL Dev from [https://faucet.solana.com/](https://faucet.solana.com/)
4. Buy a forecast, like, repost, and add your own X

---

## 🛠 Tech Stack

**Backend:** Python 3.10+, Flask, Gemini 2.0 Flash (with Google Search), Polymarket API  
**Frontend:** Tailwind CSS, Three.js, Lucide Icons  
**Blockchain:** Solana Web3.js, Phantom Wallet (Desktop & Mobile Deep Linking)  
**Infrastructure:** Nginx, Systemd, Gunicorn  
**APIs:** Polymarket, Google Gemini, Twitter/X  

---

## 🏗 Architecture

```
life.py → scanner.py → brain.py → storage.py → forecasts.json → Web Interface
```

Polymira Agent runs as a systemd service (`polymira-agent.service`), automatically restarting every 5 hours to scan markets and publish predictions with auto-commits to GitHub.

### Agent Loop (life.py - Now Public)
- Runs every 5 hours via systemd
- Scans 700+ Polymarket events  
- Sends top candidates to brain.py (Gemini 2.0 Flash + Google Search)
- Auto-commits predictions to GitHub as [@kolyantrend](https://github.com/kolyantrend)

**Note:** `life.py` is now public to demonstrate agent autonomy. Core AI logic (`brain.py`, `scanner.py`) remains private as product IP.

---

## 🛡 Security

- `.env` based secrets (API keys, tokens)
- Rate limiting with Flask-Limiter
- Non-custodial wallet integration
- **Private files during hackathon:**
  - `brain.py` - AI prediction logic & Gemini integration
  - `scanner.py` - Polymarket market scanning engine
  - `storage.py` - Data persistence layer
  - `forecasts.json`, `profiles.json`, `purchases.json` - Databases
  - `.env` - Environment variables

The public release is planned after the completion of the competition and product testing.

---

## 🏆 Hackathon

Colosseum Agent Hackathon 2026  
Category: AI Agent  
Blockchain: Solana (Devnet)

---

## 📄 License

License: [MIT](LICENSE)

---

## 👤 Author

**Built by [@kolyantrend](https://x.com/kolyantrend)**

- 🌐 Website: [polymira.org](https://polymira.org)
- 🐦 Twitter: [Polymira](https://x.com/Polymira)
- 💻 GitHub: [@kolyantrend](https://github.com/kolyantrend)

---

<div align="center">
  <sub>Made with ❤️ for Colosseum Agent Hackathon 2026</sub>
</div>
