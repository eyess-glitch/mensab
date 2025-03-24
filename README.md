# Voice-Controlled AI Assistant (Mensab)

A modular voice assistant system that combines wake-word detection, speech-to-text conversion, and local LLM processing to execute tasks through natural language commands.


## 1. Technical Specifications

- **Wake Word Engine**: Porcupine 
- **STT Model**: Faster-Whisper (`turbo` variant)
- **LLM Backend**: Ollama (default: `qwen2.5-coder:7b`)
- **Audio Processing**: 16kHz, 16-bit mono PCM
- **VAD Sensitivity**: Aggressive (WebRTC Vad mode 1)

## 2. Getting Started

### Prerequisites
- Python 3.8+
- PyAudio
- Porcupine wake word engine (with valid access key)
- Ollama service running locally
- Faster-Whisper dependencies

### Installation
```bash
git clone https://github.com/yourusername/mensab-voice-assistant.git
cd mensab-voice-assistant
pip install -r requirements.txt

## 3. Usage
python run_system.py
