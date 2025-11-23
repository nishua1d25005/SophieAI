# 🧠 SophieAI  
### A Voice-Activated Desktop Assistant Built in Python

SophieAI is a fully custom personal AI assistant designed to run locally on Windows with optional cloud intelligence via the OpenAI API.

It combines **speech recognition, AI logic, system automation, memory, web search, summarization, and Excel automation** into one unified assistant.

---

## ✨ **Key Features**

### 🔊 **Wake-Word Activation**
Uses `openwakeword` to continuously listen for a trigger phrase.

### 🎤 **Speech Recognition (English + Hindi)**
Powered by Google's ASR with automatic language detection.

### 🗣️ **Text-to-Speech Engine**
Natural voice output using `pyttsx3`.

### 🧠 **GPT Integration**
Fallback to GPT-3.5 for complex queries.

### 📝 **Memory System**
Stores:
- user’s last topic  
- conversation history  
- context for follow-up questions  

Saved in `memory.json`.

### 🌐 **Web Search + Auto Summarizer**
Uses:
- `googlesearch` to fetch results  
- `BeautifulSoup` to summarize the page  

### 📊 **Excel Automation**
You can give commands like:

> "Add two new rows in report.xlsx"

SophieAI auto-generates Python code using GPT and executes it safely with `exec()` sandbox.

### 💻 **System Commands**
- Open Notepad  
- Launch Chrome  
- Shutdown / Restart PC  
- Open files  
- And more…

---

## 🛠️ **Tech Stack**

| Category | Tools |
|---------|-------|
| Language | Python |
| AI / NLP | SpeechRecognition, openwakeword, pyttsx3, googletrans |
| Web | BeautifulSoup, requests, googlesearch |
| Excel | openpyxl |
| OS | Windows automations |
| Cloud | OpenAI API |

---

## 📂 **Project Structure**

