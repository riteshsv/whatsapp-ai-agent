# WhatsApp-ai-agent 🤖💬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)

A production-ready FastAPI middleware engine that connects Meta's **WhatsApp Business Cloud API** with **OpenAI** to deliver context-aware AI support and automation.

---

## 📸 Overview & Flow
┌─────────────────┐       ┌────────────────────────┐       ┌─────────────────┐
│ Customer Phone  │ ────> │ WhatsApp Business Cloud│ ────> │ FastAPI Server  │
│  (WhatsApp App) │ <──── │       API Webhook      │ <──── │ + OpenAI Engine │
└─────────────────┘       └────────────────────────┘       └─────────────────┘

---

## ✨ Features

- ⚡ **FastAPI Webhook Server:** Validates Meta webhook verification requests and processes incoming text messages asynchronously.
- 🧠 **AI-Powered Responses:** Integrates with OpenAI's GPT models to handle incoming queries.
- 🔒 **Secure Configuration:** Environment-variable-based credential management (`.env`).
- 🧪 **Mock Demo Data:** Includes standard Meta webhook JSON payloads for rapid local testing.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** installed.
- A **Meta for Developers** account with the WhatsApp product added.
- An **OpenAI API Key**.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/WhatsApp-ai-agent.git](https://github.com/your-username/WhatsApp-ai-agent.git)
   cd WhatsApp-ai-agent