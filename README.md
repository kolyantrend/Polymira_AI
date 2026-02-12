# 🔮 Polymira AI — Prediction Market Oracle

![Polymira Banner](https://pub-7341693284a64271b79b1b4630d3e1eb.r2.dev/polymira%20(20).jpeg)

Polymira is an autonomous AI agent built for the **Colosseum Agent Hackathon 2026**.  
It operates as an intelligent layer on top of **Polymarket**, combining real-time market data with **Gemini 3.0 Flash Preview** reasoning to detect mispriced prediction markets and surface high-probability insights.

Polymira runs continuously, researches independently, and publishes actionable forecasts without human intervention.

---

## 🚀 Key Features

- 🤖 **Autonomous Agent (24/7)** - Continuous monitoring and analysis via systemd service
- 🔍 **Deep Research Engine V3** - Gemini 3.0 Flash Preview + Google Search Tooling
- 📊 **Real-time Scanning** - Smart filtering of Polymarket events (Politics, Crypto, Finance, Sports)
- 🎯 **Edge Detection** - AI probability vs market odds analysis (10% threshold)
- 💎 **Solana Integration** - Phantom Wallet support (Desktop & Mobile)
- 📱 **Mobile Deep Linking** - Seamless wallet connection on mobile devices
- 🏆 **Reputation System** - Leaderboard tracking (buyers, likers, sharers)
- 🐦 **Social Sharing** - Twitter/X integration with verification
- 🔐 **Secure Payments** - 0.01 SOL per prediction unlock (Devnet)
- 🎨 **Modern UI** - Tailwind CSS + Three.js animations
- ⚡ **Automated GitHub Sync** - Self-updating repository with latest findings
- 🔒 **Rate Limiting** - Built-in security with Flask-Limiter

---

## 🧠 Agentic Decision Logic

```
Edge = True_Probability (AI) − Market_Probability (Polymarket)
```

If `Edge > 10%`, Polymira automatically publishes a prediction card, updates the local database, and pushes changes to the GitHub repository.

---

## ⚡ Live Demo (Solana Devnet)

### Polymira is an AI-powered forecasting system that operates 24/7, providing automated market analysis. It automatically searches for forecasts, analyzes them using Google Search, and generates results.

1. Visit [https://forecasts.polymira.org/](https://forecasts.polymira.org/)
2. Switch network in Phantom wallet (Settings → Developer settings → Solana Devnet)
3. Get SOL Dev from [https://faucet.solana.com/](https://faucet.solana.com/)
4. Buy a forecast, like, repost, and add your own X

---

## 🛠 Tech Stack

**Backend:** Python 3.12, Flask, Gemini 3.0 Flash Preview (google-genai), Polymarket API  
**Frontend:** Tailwind CSS, Three.js, Lucide Icons  
**Blockchain:** Solana Web3.js, Phantom Wallet (Desktop & Mobile Deep Linking)  
**Infrastructure:** Nginx, Systemd, Gunicorn, Venv  
**APIs:** Polymarket Gamma API, Google Gemini, Twitter/X  

---

## 🏗 Architecture

```
life.py → scanner.py → brain.py (Gemini 3.0) → storage.py → forecasts.json → Web Interface
```

Polymira Agent runs as a systemd service (`polymira-agent.service`), automatically cycling every **5 hours** to scan markets and publish predictions with auto-commits to GitHub.

### Agent Loop (life.py)
- Runs every 300 minutes via systemd
- Scans Polymarket events with "Freshness First" logic
- Sends top candidates to `brain.py` for Google Search Grounding
- Auto-commits predictions to GitHub as [@kolyantrend](https://github.com/kolyantrend)

---

## 🛡 Security

- `.env` based secrets (API keys, tokens)
- Rate limiting with Flask-Limiter
- Non-custodial wallet integration
- **Private Core Files:**
  - `brain.py` - AI prediction logic & Google Search integration
  - `scanner.py` - Market scanning & filtering engine
  - `storage.py` - Data persistence layer
  - `.env` - Environment variables

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
