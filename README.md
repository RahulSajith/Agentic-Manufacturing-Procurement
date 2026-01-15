# 🤖 Agentic Manufacturing Procurement System

An autonomous **Computer Use Agent (CUA)** built to demonstrate reliable, closed-loop automation for industrial procurement. 

## 🚀 The Challenge
Manufacturing procurement often involves manual navigation of vendor portals, which is slow and prone to human error. This project automates that workflow while maintaining "Safety-First" industrial standards.

## 🛠️ Tech Stack
- **Engine:** Python
- **LLM:** `Qwen3:8b` (Running locally via Ollama)
- **Automation:** Playwright (Chromium)
- **Validation:** Pydantic

## ✨ Key Features
- **Closed-Loop Verification:** The agent doesn't just click; it re-scans the UI after every action to verify the state change (e.g., confirming a "Quote Sent" message).
- **Human-in-the-Loop (HITL):** Integrated approval gate prevents the AI from taking financial actions without human confirmation.
- **Local Inference:** Runs entirely on local hardware, ensuring proprietary manufacturing data never leaves the internal network.
- **Audit Trails:** Generates structured logs in `/logs` for every agentic decision and action.

## 🚦 How to Run
1. Ensure **Ollama** is running with `ollama run qwen3:8b`.
2. Install dependencies: `pip install playwright pydantic ollama`.
3. Initialize Playwright: `playwright install chromium`.
4. Run the agent: `python src/agent.py`.