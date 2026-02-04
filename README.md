<h1 align="center">🌍 Language Translator (Desktop Application)</h1>

<p align="center">
  Ứng dụng dịch ngôn ngữ desktop sử dụng Python & Google Translate API  
</p>

<p align="center">
  <img src="resources/icons/banner.png" alt="Language Translator Banner" width="80%">
</p>

---

## 📌 Giới thiệu

**Language Translator** là một ứng dụng desktop được phát triển bằng **Python (Tkinter)**, cho phép người dùng dịch văn bản giữa hơn **100 ngôn ngữ** một cách nhanh chóng và trực quan.

Ứng dụng tích hợp **Google Translate API** thông qua thư viện `googletrans`, hỗ trợ:
- Tự động nhận diện ngôn ngữ đầu vào
- Dịch văn bản theo thời gian thực
- Chuyển văn bản thành giọng nói
- Nhập văn bản bằng giọng nói
- Sao chép và xóa nội dung dễ dàng

Giao diện được thiết kế đơn giản, thân thiện, phù hợp cho học tập, demo đồ án và sử dụng hằng ngày.

---

## 🖥️ Giao diện ứng dụng

<p align="center">
  <img src="resources/screenshots/main_ui.png" alt="Application UI" width="85%">
</p>

---

## ⚙️ Chức năng chính

- 🌐 **Translate**: Dịch văn bản giữa hơn 100 ngôn ngữ
- 🧠 **Auto Detect**: Tự động nhận diện ngôn ngữ nguồn
- 🔁 **Swap Language**: Đảo ngược ngôn ngữ nguồn – đích
- 🔊 **Read Aloud**: Đọc to văn bản đã dịch (Text-to-Speech)
- 🎙️ **Voice Input**: Nhập văn bản bằng giọng nói (Speech-to-Text – tiếng Anh)
- 📋 **Copy**: Sao chép nội dung dịch vào clipboard
- 🧹 **Clear**: Xóa nhanh nội dung nhập và kết quả
- 🎨 **GUI trực quan**: Giao diện hiện đại, dễ sử dụng

---

## 🧠 Công nghệ & Thư viện sử dụng

| Công nghệ | Mô tả |
|---------|------|
| Python | Ngôn ngữ lập trình chính |
| Tkinter | Xây dựng giao diện đồ họa |
| googletrans | Kết nối Google Translate API |
| gTTS | Chuyển văn bản sang giọng nói |
| SpeechRecognition | Nhận diện giọng nói |
| PyAudio | Thu âm từ microphone |
| NumPy | Xử lý tín hiệu âm thanh |
| Pillow (PIL) | Xử lý hình ảnh |
| pyperclip | Sao chép văn bản |

---

## 📂 Cấu trúc thư mục
language-translator/
│
├── language_translator.py # File chính chạy ứng dụng
├── README.md # Tài liệu mô tả dự án
├── text_to_speech.mp3 # File âm thanh sinh ra (Read Aloud)
├── resources/
│ ├── icons/ # Icon giao diện
│ └── screenshots/ # Ảnh giao diện ứng dụng
