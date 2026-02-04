<h1 align="center">🌍 Language Translator (Desktop Application)</h1>

<p align="center">
AI-powered language translation desktop app built with Python & Google Translate
</p>

<p align="center">
<img src="translator.png" alt="Language Translator UI" width="900"/>
</p>

---

## 📌 Project Overview

**Language Translator** is a **desktop application** developed using **Python (Tkinter)** that allows users to translate text between **multiple languages** using **Google Translate AI**.

The system provides a clean and intuitive **graphical user interface** with:
- Two language selection boxes
- Input and output text areas
- One-click translation
- Voice and audio support

This project focuses on **AI integration**, **GUI design**, and **user-friendly interaction**.

---

## 🤖 AI Integration (Google Translate)

This system integrates **Artificial Intelligence through Google Translate**:

- AI-powered **automatic language detection**
- High-quality multilingual translation
- Real-time translation via `googletrans` library

> Google Translate AI is used as the core translation engine of the system.

---

## 🖥️ User Interface Description

The application interface consists of:

- **Header section**  
  Displays the title *LANGUAGE TRANSLATOR* with a clean blue theme.

- **Language Selection**
  - Left combobox: Source language (Auto Detect supported)
  - Right combobox: Target language
  - Center swap button to reverse languages

- **Text Areas**
  - Left: Input text
  - Right: Translated output text

- **Action Buttons**
  - **Translate** (main button – emphasized)
  - Clear
  - Copy
  - Read Aloud
  - Voice Input

---

## ✨ Features

- 🌐 Translate text across **100+ languages**
- 🔍 Auto detect input language
- 🔊 Read translated text aloud (Text-to-Speech)
- 🎙️ Voice input using microphone (Speech-to-Text)
- 📋 Copy translated text to clipboard
- 🧹 Clear input/output text easily
- 🎨 Clean pastel-blue GUI (Tkinter)

---

## 🛠️ Technologies Used

- Python 3.10
- Tkinter (GUI)
- Google Translate AI (`googletrans`)
- gTTS (Text-to-Speech)
- SpeechRecognition (Voice Input)
- PyAudio
- Pyperclip
- Pillow (Image handling)

---

## ⚙️ Installation & Run

### 1️⃣ Clone repository
```bash
git clone https://github.com/Khang226000/language-translator.git
cd language-translator
