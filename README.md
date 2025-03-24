# 🎙️ Voice-to-Command AI Assistant  

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/LLM-Ollama-orange?logo=ollama" alt="Ollama">
  <img src="https://img.shields.io/badge/ASR-Whisper-lightgrey?logo=openai" alt="Whisper">
  <img src="https://img.shields.io/badge/Wakeword-Porcupine-yellow" alt="Porcupine">
</p>

A voice-controlled assistant that **transcribes speech to text** and **executes terminal commands** via LLM. Built for local automation with natural interaction.

---

## ✨ Features  
- 🎤 **Wake-word detection** 
- 🔍 **Speech-to-Text** using `faster-whisper`  
- 💻 **Bash script generation** via `Ollama`  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed
- [Porcupine Access Key](https://console.picovoice.ai/) (free tier available)

### Installation
```bash
# Clone the repo
git clone https://github.com/your-username/voice-command-assistant.git
cd voice-command-assistant

# Install dependencies
pip install -r requirements.txt

# Download models
ollama pull qwen2.5-coder:7b
