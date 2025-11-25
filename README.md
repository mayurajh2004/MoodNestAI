# MoodNestAI

**MoodNestAI** is an AI-powered mental wellness companion designed to support users in tracking, analyzing, and improving their emotional well-being. The system leverages multi-agent AI architecture, combining intake, analysis, and recommendation agents to provide personalized guidance and coping strategies.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview
MoodNestAI focuses on helping users improve their mental wellness through:

- **Emotion Intake** – Users provide input on their mood and experiences.
- **Analysis** – AI agents analyze patterns, detect emotional states, and evaluate well-being.
- **Recommendations** – Personalized coping strategies and suggestions are generated to improve mood.

By using a multi-agent approach, MoodNestAI ensures modularity, scalability, and efficient handling of user interactions.

---

## Architecture

![Architecture](assets/architecture.png)

**High-Level Flow:**

1. **User Interaction** – Users interact via Streamlit UI.
2. **Orchestration** – FastAPI orchestrator routes requests to agents.
3. **Agents** –  
   - `Intake Agent` – collects user input  
   - `Analyzer Agent` – interprets emotional patterns  
   - `Recommender Agent` – generates personalized advice  
4. **Memory** – Stores user sessions and past interactions for context-aware recommendations.

---

## Features
- Multi-agent AI system for personalized mental wellness guidance
- Streamlit web interface for easy interaction
- FastAPI orchestrator for real-time request handling
- Memory module for storing user history
- Modular architecture for easy extension

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/mayurajh2004/MoodNestAI.git
cd MoodNestAI
```

2. **Set up Python environment**

Create and activate a virtual environment (examples):

Windows (PowerShell):

```powershell
python -m venv venv
venv\\Scripts\\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Run the Streamlit UI:

```bash
streamlit run streamlit_app.py
```

Run the FastAPI orchestrator (example using `uvicorn`):

```bash
uvicorn orchestrator_app:app --reload --port 8000
# or if your app is run differently, adjust the command accordingly
```

Open your browser at `http://localhost:8501` for the Streamlit UI or `http://127.0.0.1:8000/docs` for the FastAPI docs (if available).

## repository tree

```text
MoodNestAI/
├─ README.md
├─ KAGGLE_WRITEUP.md
├─ requirements.txt
├─ streamlit_app.py
├─ orchestrator_app.py
├─ agents/
│  ├─ __init__.py
│  ├─ a2a_message.py
│  ├─ intake_agent.py
│  ├─ analyzer_agent.py
│  ├─ recommender_agent.py
│  └─ tools.py
├─ memory/
│  ├─ memory.py
│  └─ init_db.py
├─ docker/
│  ├─ Dockerfile
│  └─ gcp_deploy.md
├─ tests/
│  └─ test_agents.py
└─ assets/
   ├─ architecture.png
   └─ thumbnail.png
```



