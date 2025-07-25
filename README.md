# Visexa Pilot

### Deployed on Streamlit : https://hkq8y6bhxj6lrevvlxauq4.streamlit.app/

Visexa Pilot is your **AI-powered personal co-worker** built using [LangGraph](https://www.langchain.com/langgraph), [LangChain](https://www.langchain.com/), and [Streamlit](https://streamlit.io/).  
It acts as a multi-tool agent capable of browsing, analyzing data, writing code, and iterating on tasks until your **success criteria** are met.

---

## ✨ Features
- **LangGraph-powered Multi-Agent Workflow**: Executes tasks step-by-step with evaluation loops.
- **Built-in Tools**:  
  - Google search (via Serper API)  
  - Wikipedia queries  
  - Python REPL execution  
  - File management  
  - Push notifications via Pushover  
  - Playwright-based browser automation (headless mode)
- **Self-Evaluating Agent**: Evaluates its own answers against user-defined success criteria.
- **Streamlit UI**: A beautiful and professional chat-like interface for interaction.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/visexa-pilot.git
cd visexa-pilot
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Environment Variables
Create a `.env` file in the project root and add:
```
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langchain_key
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user
PLAYWRIGHT_HEADLESS=true
```

---

## 🖥️ Running the App

Run the Streamlit app locally:
```bash
streamlit run streamlit_app.py
```

The app will launch in your default browser at `http://localhost:8501`.

---

## ☁️ Deploying on Streamlit Cloud
1. Push your project to GitHub.  
2. Go to [streamlit.io](https://streamlit.io/cloud) and deploy your repo.  
3. In **App Settings → Secrets**, add the environment variables mentioned above.  
4. Ensure you have a `packages.txt` with `playwright` listed and `requirements.txt` with the Python dependencies.  
5. Add a `.streamlit/config.toml` with:
   ```toml
   [server]
   headless = true

   [build]
   commands = ["playwright install chromium"]
   ```

---

## 🧩 Project Structure
```
visexa-pilot/
│
├── streamlit_app.py         # Streamlit UI
├── sidekick.py              # Main Sidekick agent logic
├── sidekick_tools.py        # Toolkits for the agent
├── requirements.txt         # Dependencies
├── packages.txt             # System-level packages
└── README.md                # Project Documentation
```

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **Streamlit** – UI framework
- **LangGraph & LangChain** – Agent orchestration
- **OpenAI GPT Models**
- **Playwright** – Browser automation
- **Pushover** – Push notifications

---

## 📜 License
This project is licensed under the MIT License. You are free to modify and distribute it.

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork this repo, submit PRs, or open issues.

---

## ✍️ Author
**Visexa Labs : Sukhdeep Singh**  
*Your AI Co-Worker for Smarter Workflows*
