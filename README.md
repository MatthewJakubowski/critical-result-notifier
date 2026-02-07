<div align="center">
  <img src="https://raw.githubusercontent.com/MatthewJakubowski/Universal-Lab-Converter/main/going_dark_cover.jpg" width="100%" alt="System Status: Going Dark. Deep Work Protocol.">
</div>


# ⚡ Critical Result Closed-Loop Notifier

<div align="center">

![Status](https://img.shields.io/badge/Status-Educational_Prototype-F7DF1E?style=for-the-badge&logo=statuspage&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Compliance](https://img.shields.io/badge/ISO_15189-Concept-005C84?style=for-the-badge&logo=nhs&logoColor=white)

<br />

**A resilient, automated system for communicating "Panic Values" in clinical laboratories.** *Ensures no critical patient result is lost in the noise.*

[Explore Code](https://github.com/MatthewJakubowski/critical-result-notifier) · [Report Bug](https://github.com/MatthewJakubowski/critical-result-notifier/issues)

</div>

---

> [!IMPORTANT]
> **NOT A MEDICAL DEVICE**: This software is a **Proof of Concept (PoC)** designed strictly for educational purposes and architectural demonstration. It is **NOT** a certified medical device (MDR/FDA) and **must not** be used for patient diagnosis or clinical decision-making.

> [!CAUTION]
> **LEGAL & SAFETY DISCLAIMER – READ BEFORE USE**
>
> This software is provided strictly for **EDUCATIONAL** and **ARCHITECTURAL DEMONSTRATION** purposes only.
>
> 1. **NO CLINICAL USE:** This software is **NOT** a certified medical device under MDR (EU), FDA (USA), or any other regulatory framework. It must **NEVER** be used for actual patient diagnosis, monitoring, or treatment.
> 2. **NO WARRANTY:** THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
> 3. **LIABILITY WAIVER:** IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, MEDICAL ERRORS, LOSS OF LIFE, OR OTHER LIABILITY.
> 4. **COMPLIANCE:** Any implementation of this logic in a real-world scenario requires independent validation, clinical trials, and strict compliance with local regulations (HIPAA, GDPR/RODO, ISO 15189).


## 🤖 Vibe Coding & Credits
​This project was architected and generated via Vibe Coding sessions in close cooperation with my favorite assistant and travel companion, Google Gemini AI.
It represents an exploration of AI-Assisted Engineering, demonstrating how modern LLMs can help structure robust, safety-critical architectural patterns.

## 🧬 The Problem
In high-throughput medical laboratories, reporting **Critical Values** (results indicating immediate life-threatening states) is often a bottleneck. Manual phone calls are prone to:
* ⏳ **Latency:** Technicians waiting on hold.
* ❌ **"Fire and Forget":** Leaving voicemails that are never checked.
* 📉 **Human Error:** Miscommunication of patient data.

## 💡 The Solution: Closed-Loop Architecture
This system implements a **Persistent State Machine** that guarantees delivery through a confirmation loop.

### How it works (The Logic Flow)

```mermaid
sequenceDiagram
    participant LIS as Lab Interface (Mock)
    participant Core as System Core (Python)
    participant DB as SQLite (State)
    participant Doc as Physician (Twilio)
    
    LIS->>Core: 🩸 Critical Value Detected (K+ > 6.2)
    Core->>DB: Create Incident (Status: NEW)
    Core->>Doc: 📞 CALL: "Critical result for Order #123"
    
    alt Physician Answers & Presses 1
        Doc-->>Core: DTMF "1" (Ack)
        Core->>DB: Update Status: ACKNOWLEDGED
        Core->>LIS: Log "Delivered to Human"
    else No Answer / Hangup
        Core->>DB: Update Retry Count (+1)
        Core->>Core: Wait 60s -> Retry Call
    else Max Retries Exceeded (3x)
        Core->>DB: Update Status: ESCALATING
        Core->>Doc: 🚨 CALL MANAGER (Escalation)
    end

  ```
---

## 🛠 Tech Stack & Engineering Decisions

| Component | Technology | Why? |
| :--- | :--- | :--- |
| **Language** | Python 3.12 | Type hinting, AsyncIO support, and vast library ecosystem. |
| **Container** | Docker | "Build once, run anywhere" reliability, isolating dependencies. |
| **Database** | SQLite (WAL) | Serverless, atomic transactions, perfect for embedded logic. |
| **Telephony** | Twilio Voice | Programmable voice API for TwiML (XML) interaction. |
| **API** | FastAPI | High-performance webhook handler for call callbacks. |

## 📂 Project Structure
```text
critical-result-notifier/
├── config/
│   └── settings.yaml      # Thresholds & Retries configuration
├── src/
│   ├── core/              # Business Logic (State Machine)
│   ├── main.py            # Application Entry Point
│   └── server.py          # Webhook Listener (FastAPI)
├── Dockerfile             # Container definition
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```
## 🚀 Deployment (Quick Start)
**​Prerequisites**: Docker & Twilio Account.
1. **Clone the repository**
   ```bash
   git clone [https://github.com/MatthewJakubowski/critical-result-notifier.git](https://github.com/MatthewJakubowski/critical-result-notifier.git)
   cd critical-result-notifier
   ```
2. **Configure Environment**
   ```bash
    cp .env.example .env # Edit .env with your Twilio SID/Token
   ```
3. **Ignition (Docker)**
   ```bash
   docker-compose up --build -d
   ```
4. **Verify Status**
   The system will begin the heartbeat loop. Check logs via:
   ```bash
   docker logs -f critical-alert-worker
   ```

<br />
​<div align="center">
<p>Authored by <b>Mateusz Jakubowski</b></p>
<p><i>Engineering Safe Systems for Healthcare.</i></p>
<p>Copyright © 2026. All Rights Reserved.</p>
</div>
