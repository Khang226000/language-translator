import tkinter as tk  
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image  
from googletrans import Translator, LANGUAGES 
from tkinter import messagebox
import pyperclip as pc 
import os
import sys
import speech_recognition as spr 
import webbrowser
import cv2
import threading
import pyaudio
import easyocr
import platform
from datetime import datetime
from tkinter import filedialog
import numpy as np
from database import get_user_info, delete_history_item, get_history
from gtts import gTTS
from playsound import playsound
import tempfile
import pygame
from database import create_tables, save_history, add_login_from_column, check_tables

profile_window = None
reader_general = None
reader_japanese = None
reader_korean = None
reader_cyrillic = None

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr
pygame.mixer.init()
LANGUAGE_CODES = {v.title(): k for k, v in LANGUAGES.items()}
LANGUAGE_CODES["Auto Detect"] = "auto"
TTS_CODES = {
    "English": "en",
    "Vietnamese": "vi",
    "Japanese": "ja",
    "Korean": "ko",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-cn",
    "Thai": "th",
    "Russian": "ru",
    "Italian": "it"
}
SPEECH_CODES = {
    "Auto Detect": "en-US",
    "English": "en-US",
    "Vietnamese": "vi-VN",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "French": "fr-FR",
    "German": "de-DE",
    "Spanish": "es-ES",
    "Chinese": "zh-CN",
    "Thai": "th-TH",
    "Russian": "ru-RU",
    "Italian": "it-IT"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BG_MAIN   = "#EAF4FF"   
BG_HEADER = "#A7D3FF"   
BG_PANEL  = "#FFFFFF"   
BTN_MAIN  = "#4DA3FF"   
BTN_SOFT  = "#A7D3FF"   
BG_HEADER = BTN_MAIN
BTN_HOVER = "#3399FF"
TEXT_DARK = "#1F2937"


# ---------------------------------------------------Language Translator--------------------------------------------------------------
''' This python file consist of all functionalities required for the language translator application to work  '''

# UI is developed using Tkinter library
create_tables()
check_tables()
add_login_from_column()

root = tk.Tk()

def init_ocr():
    global reader_general, reader_japanese, reader_korean, reader_cyrillic

    with HiddenPrints(): 
        reader_general = easyocr.Reader(['en','vi','fr','de','es','it'])
        reader_japanese = easyocr.Reader(['en','ja'])
        reader_korean = easyocr.Reader(['en','ko'])
        reader_cyrillic = easyocr.Reader(['en','ru'])

# chạy nền
threading.Thread(target=init_ocr, daemon=True).start()
root.title('Langauge Translator')
root.geometry('1060x660')
root.maxsize(1060, 660)
root.minsize(1060, 660)
root.configure(bg=BG_MAIN)
# ===== STYLE COMBOBOX =====
style = ttk.Style()
style.theme_use("default")

style.configure(
    "TCombobox",
    fieldbackground=BG_PANEL,
    background=BTN_SOFT,
    foreground=TEXT_DARK,
    padding=6
)
# ===== HEADER =====
header = Frame(root, bg=BG_HEADER, height=90)
header.pack(fill=X)
# ===== AVATAR USER (TOP RIGHT) =====
try:
    user_img = Image.open(
        os.path.join(BASE_DIR, "resources", "icons", "dangnhap.png")
    )

    user_img = user_img.resize((55, 55), Image.Resampling.LANCZOS)
    user_avatar = ImageTk.PhotoImage(user_img)

    avatar_label = Label(
        header,
        image=user_avatar,
        bg=BG_HEADER,
        bd=0,
        cursor="hand2"
    )
    avatar_label.image = user_avatar

    # đặt góc phải
    avatar_label.place(relx=0.97, rely=0.5, anchor="e")

    # click mở profile
    def open_profile(event=None):
        global profile_window

    # Nếu đã mở rồi thì focus lại
        if profile_window is not None and profile_window.winfo_exists():
            profile_window.deiconify()
            refresh_history()   
            profile_window.lift()
            profile_window.focus_force()
            return

        profile_window = create_profile_window()

    avatar_label.bind("<Button-1>", open_profile)

except Exception as e:
    print("Lỗi load avatar:", e)

title_frame = Frame(header, bg=BG_HEADER)
title_frame.pack(pady=15)

try:
    logo_img = Image.open(
        os.path.join(BASE_DIR, "resources", "icons", "translation.png")
    )

    logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
    logo_icon = ImageTk.PhotoImage(logo_img)

    logo_label = Label(
        title_frame,
        image=logo_icon,
        bg=BG_HEADER,
        bd=0
    )
    logo_label.image = logo_icon
    logo_label.pack(side=LEFT, padx=(0, 10))

except Exception as e:
    print("Lỗi load logo:", e)
    
title_label = Label(
    title_frame,
    text="LANGUAGE TRANSLATOR",
    bg=BG_HEADER,
    fg="white",
    font=("Segoe UI", 26, "bold")
)
title_label.pack(side=LEFT)


# ===== MIC CANVAS (HIỆU ỨNG SÓNG) =====
mic_canvas = Canvas(
    root,
    width=220,
    height=220,
    bg="#6EC6FF",
    highlightthickness=0
)
mic_canvas.place(x=820, y=300)
mic_canvas.place_forget()

listening = False
audio_level = 0.0
voice_running = False


def draw_mic_wave(level):
    mic_canvas.delete("all")

    cx, cy = 110, 110
    base_radius = 50
    wave_radius = base_radius + int(level * 40)

    # sóng ngoài
    mic_canvas.create_oval(
        cx - wave_radius, cy - wave_radius,
        cx + wave_radius, cy + wave_radius,
        fill="#4AA3FF", outline=""
    )

    # mic chính
    mic_canvas.create_oval(
        cx - base_radius, cy - base_radius,
        cx + base_radius, cy + base_radius,
        fill="#1E90FF", outline=""
    )

    mic_canvas.create_text(cx, cy, text="🎤", font=("Arial", 36), fill="white")

def update_mic_ui():
    if listening:
        draw_mic_wave(audio_level)
        root.after(40, update_mic_ui) 

def mic_wave_listener():
    global listening, audio_level

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    while listening:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)

            samples = np.frombuffer(data, dtype=np.int16)

            if len(samples) == 0:
                audio_level = 0
                continue

            rms = np.sqrt(np.mean(samples.astype(np.float32) ** 2))

            if np.isnan(rms):
                rms = 0

            audio_level = min(rms / 3000, 1.0)

        except Exception:
            audio_level = 0

    stream.stop_stream()
    stream.close()
    p.terminate()
    
# Tittle bar icon image used in Tkinter GUI
title_bar_icon = PhotoImage(
    file=os.path.join(BASE_DIR, "resources", "icons", "translation.png")
)
root.iconphoto(False,title_bar_icon)
cl =''
output=''
current_user_id = None
scrollable_frame = None
if len(sys.argv) > 1:
    current_user_id = int(sys.argv[1])
user_data = get_user_info(current_user_id)

if user_data:
    current_role = user_data[3]   # role
else:
    current_role = "user"



# For Clearing Textbox Data
def clear():
    t1.delete(1.0, 'end')
    t2.delete(1.0, 'end')
# dịch tự động  
translator = Translator()
typing_timer = None
def auto_translate(event=None):

    global typing_timer

    if typing_timer:
        root.after_cancel(typing_timer)

    typing_timer = root.after(120, do_translate)
def do_translate():

    text = t1.get("1.0", "end-1c")

    if text.strip() == "":
        t2.delete("1.0", "end")
        return

    from_lang = auto_detect.get()
    to_lang = choose_langauge.get()

    src = LANGUAGE_CODES.get(from_lang, "auto")
    dest = LANGUAGE_CODES.get(to_lang, "en")

    def translate_thread():

        try:
            result = translator.translate(text, src=src, dest=dest)

            global output
            output = result.text
            save_history(
            current_user_id,
            text,
            output,
            from_lang,
            to_lang
            )
        
            root.after(0, update_output, result.text)
            root.after(0, refresh_history)
        except Exception as e:
            print("Translate error:", e)

    threading.Thread(target=translate_thread, daemon=True).start()
def update_output(text):

    t2.delete("1.0", "end")
    t2.insert("end", text)

    
def refresh_history():
    global scrollable_frame
    
    if scrollable_frame is None:
        return

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    history = get_history(current_user_id)

    for h in history:
        source, translated, from_lang, to_lang, time, hid = h

        item = Frame(scrollable_frame, bg="#F5F9FF", bd=1, relief="solid")
        item.pack(fill="x", pady=8, padx=10)

        top = Frame(item, bg="#F5F9FF")
        top.pack(fill="x", padx=5, pady=2)

        Label(top, text=f"{from_lang} → {to_lang}",
              font=("Segoe UI", 9, "bold"),
              bg="#F5F9FF").pack(side="left")

        Label(top, text=time,
              font=("Segoe UI", 8),
              fg="gray",
              bg="#F5F9FF").pack(side="right")

        Label(
            item,
            text=source,
            anchor="w",
            justify="left",
            wraplength=600,  # 👉 tăng theo width mới
            bg="#F5F9FF"
        ).pack(fill="x", padx=5)

        Label(
        item,
        text="→ " + translated,
        fg="#1E90FF",
        justify="left",
        wraplength=600,
        bg="#F5F9FF"
    ).pack(fill="x", padx=5, pady=(0,5))

        # ===== DELETE =====
        def delete_item(id=hid):
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa?")
            if confirm:
                delete_history_item(id)
                refresh_history()

        # ===== SAVE =====
        def save_item(text_source=source, text_trans=translated):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text file", "*.txt")]
            )
            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"{text_source}\n→ {text_trans}")

            messagebox.showinfo("OK", "Đã lưu!")

        # ===== FRAME BUTTON =====
        btn_frame = Frame(item, bg="#F5F9FF")
        btn_frame.pack(fill="x", padx=5, pady=5)

        Button(
            btn_frame,
            text="Lưu",
            bg="#4DA3FF",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=save_item
        ).pack(side="left", padx=5)

        Button(
            btn_frame,
            text="Xóa",
            bg="#FF4D4D",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=delete_item
        ).pack(side="right", padx=5)

        # hover
        def on_enter(e, frame=item):
            frame.config(bg="#EAF4FF")

        def on_leave(e, frame=item):
            frame.config(bg="#F5F9FF")

        item.bind("<Enter>", on_enter)
        item.bind("<Leave>", on_leave)
def open_full_history():
    full_win = Toplevel(root)
    full_win.title("Toàn bộ lịch sử")
    full_win.geometry("900x650")  # 👉 to hơn
    full_win.configure(bg="#EAF4FF")

    # ===== HEADER =====
    Label(
        full_win,
        text="📜 TOÀN BỘ LỊCH SỬ",
        font=("Segoe UI", 16, "bold"),
        bg="#4DA3FF",
        fg="white",
        pady=10
    ).pack(fill=X)

    # ===== FRAME CHÍNH =====
    main_frame = Frame(full_win, bg="#EAF4FF")
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    canvas = Canvas(main_frame, bg="#EAF4FF", highlightthickness=0)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)

    scroll_frame = Frame(canvas, bg="#EAF4FF")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ===== SCROLL CHUỘT =====
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # ===== LOAD DATA =====
    history = get_history(current_user_id)

    for h in history:
        source, translated, from_lang, to_lang, time, hid = h

        # ===== CARD =====
        item = Frame(
            scroll_frame,
            bg="white",
            bd=1,
            relief="solid"
        )
        item.pack(fill="x", pady=8, padx=5, ipady=5)

        # ===== TOP =====
        top = Frame(item, bg="white")
        top.pack(fill="x", padx=10, pady=5)

        Label(
            top,
            text=f"{from_lang} → {to_lang}",
            font=("Segoe UI", 10, "bold"),
            bg="white"
        ).pack(side="left")

        Label(
            top,
            text=time,
            font=("Segoe UI", 9),
            fg="gray",
            bg="white"
        ).pack(side="right")

        # ===== SOURCE =====
        Label(
            item,
            text=source,
            anchor="w",
            justify="left",
            wraplength=780,  # 👉 trải dài
            bg="white",
            font=("Segoe UI", 10)
        ).pack(fill="x", padx=10)

        # ===== RESULT =====
        Label(
            item,
            text="→ " + translated,
            fg="#1E90FF",
            anchor="w",
            justify="left",
            wraplength=780,
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(fill="x", padx=10, pady=(5, 5))

        # ===== BUTTON =====
        btn_frame = Frame(item, bg="white")
        btn_frame.pack(fill="x", padx=10, pady=5)

        # ===== SAVE =====
        def save_item(text_source=source, text_trans=translated):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text file", "*.txt")]
            )
            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"{text_source}\n→ {text_trans}")

            messagebox.showinfo("OK", "Đã lưu!")

        # ===== DELETE =====
        def delete_item(id=hid, frame=item):
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa?")
            if confirm:
                delete_history_item(id)
                frame.destroy()  # 👉 xóa ngay trên UI

        Button(
            btn_frame,
            text="💾 Lưu",
            bg="#4DA3FF",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=save_item
        ).pack(side="left", padx=5)

        Button(
            btn_frame,
            text="🗑 Xóa",
            bg="#FF4D4D",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=delete_item
        ).pack(side="right", padx=5)

        # ===== HOVER =====
        def on_enter(e, f=item):
            f.config(bg="#EAF4FF")

        def on_leave(e, f=item):
            f.config(bg="white")

        item.bind("<Enter>", on_enter)
        item.bind("<Leave>", on_leave)
def swap_languages():
    # Lấy ngôn ngữ hiện tại
    from_lang = auto_detect.get()
    to_lang = choose_langauge.get()

    # Đổi combobox
    auto_detect.set(to_lang)
    choose_langauge.set(from_lang)

    # Lấy text
    text_left = t1.get("1.0", "end-1c")
    text_right = t2.get("1.0", "end-1c")

    # Đổi nội dung text
    t1.delete("1.0", "end")
    t2.delete("1.0", "end")

    t1.insert("end", text_right)
    t2.insert("end", text_left)

# For Copying Textbox Data after Translation
def copy():
    pc.copy(str(output))

def texttospeech():

    text = t2.get("1.0", "end-1c")

    if text.strip() == "":
        messagebox.showerror(
            "Language Translator",
            "No text to read"
        )
        return

    lang = choose_langauge.get()

    tts_lang = TTS_CODES.get(lang, "en")

    speak(text, tts_lang)
# For converting Speech to Text [ Please Note : Only English is currently supported as from-language in Speech to Text Translation ]
def speak(text, lang="en"):

    def run():
        try:

            temp_path = os.path.join(tempfile.gettempdir(), "tts_audio.mp3")

            tts = gTTS(text=text, lang=lang)
            tts.save(temp_path)

            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.unload()

        except Exception as e:
            print("TTS error:", e)

    threading.Thread(target=run, daemon=True).start()
voice_popup = None

def show_voice_popup():
    global voice_popup

    voice_popup = Toplevel(root)
    voice_popup.overrideredirect(True)  # bỏ viền
    voice_popup.configure(bg="#1E90FF")

    # vị trí giữa màn hình
    x = root.winfo_x() + 350
    y = root.winfo_y() + 250
    voice_popup.geometry(f"320x120+{x}+{y}")

    frame = Frame(voice_popup, bg="#1E90FF")
    frame.pack(fill=BOTH, expand=True)

    Label(
        frame,
        text="🎤 Đang nhận giọng nói...",
        font=("Segoe UI", 14, "bold"),
        fg="white",
        bg="#1E90FF"
    ).pack(pady=(15,5))

    Label(
        frame,
        text="Hãy nói vào micro",
        font=("Segoe UI", 10),
        fg="white",
        bg="#1E90FF"
    ).pack()

def hide_voice_popup():
    global voice_popup
    if voice_popup:
        voice_popup.destroy()
        voice_popup = None
def smart_voice_translate():
    global listening, voice_running

    if voice_running:
        return
    root.focus_force()
    root.update()

    voice_running = True
    listening = True

    root.after(0, show_voice_popup)
    mic_canvas.place(x=820, y=300)
    root.update()
    def run():

        global listening, voice_running

        recog = spr.Recognizer()

        from_lang = auto_detect.get()
        to_lang = choose_langauge.get()

        
        if from_lang == "Auto Detect":
            speech_code = "vi-VN"
        else:
            speech_code = SPEECH_CODES.get(from_lang, "vi-VN")

        to_code = LANGUAGE_CODES.get(to_lang, "en")



        try:

            with spr.Microphone() as source:

                print("🎤 Listening...")
                print("Using microphone...")

                recog.adjust_for_ambient_noise(source, duration=1.5)

                recog.dynamic_energy_threshold = True
                recog.energy_threshold = 200   

                recog.pause_threshold = 1.2    
                recog.non_speaking_duration = 0.6
                root.update()
                audio = recog.listen(
                    source,
                    
                    timeout=10,           
                    phrase_time_limit=None
                )

            
            root.after(0, mic_canvas.place_forget)
                

            result_holder = {}

            def recognize_task():
                try:
                    result_holder["text"] = recog.recognize_google(
                        audio,
                        language=speech_code
                    )
                except Exception as e:
                    result_holder["error"] = str(e)

            t = threading.Thread(target=recognize_task)
            t.start()
            t.join(timeout=7)   # ⏱ tối đa 7 giây

            
            if t.is_alive():
                root.after(0, lambda: messagebox.showerror("Timeout", "Nhận diện quá lâu!"))
                root.after(0, hide_voice_popup)
                voice_running = False
                return

            
            if "error" in result_holder:
                root.after(0, lambda: messagebox.showerror("Lỗi", result_holder["error"]))
                root.after(0, hide_voice_popup)
                voice_running = False
                return

            text = result_holder.get("text", "")

            print("Recognized:", text)

            # dịch
            result = translator.translate(
                text,
                src="auto",
                dest=to_code
            )

            translated = result.text
            save_history(
            current_user_id,
            text,
            translated,
            from_lang,
            to_lang
            )
            root.after(0, refresh_history)
            def update_gui():

                t1.delete("1.0", "end")
                t1.insert("end", text)

                t2.delete("1.0", "end")
                t2.insert("end", translated)

            root.after(0, update_gui)
            root.after(0, hide_voice_popup)

            # đọc bản dịch
            tts_lang = TTS_CODES.get(to_lang, "en")
            speak(translated, tts_lang)

        except Exception as e:
            listening = False
            root.after(0, mic_canvas.place_forget)
            root.after(0, hide_voice_popup)   
            print("Voice error:", e)

        voice_running = False

    threading.Thread(target=run, daemon=True).start()
import cv2

def translate_image_ai():


    file_path = filedialog.askopenfilename(
        title="Chọn ảnh",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )

    if not file_path:
        return

    try:
        # ===== DEBUG PATH =====
        print(" File:", file_path)

        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", "Không tìm thấy file")
            return

        
        file_bytes = np.fromfile(file_path, dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            messagebox.showerror("Lỗi", "Không đọc được ảnh (OpenCV fail)")
            return

        print(" Ảnh load OK")

        # ===== OCR =====
        results = reader_general.readtext(img)

        if not results:
            print(" thử Japanese")
            results = reader_japanese.readtext(img)

        if not results:
            print(" thử Korean")
            results = reader_korean.readtext(img)

        if not results:
            print(" thử Russian")
            results = reader_cyrillic.readtext(img)

        if not results:
            messagebox.showwarning("Thông báo", "Không tìm thấy chữ trong ảnh")
            return

        # ===== LẤY TEXT =====
        text = " ".join([res[1] for res in results])

        print(" OCR:", text)

        t1.delete("1.0", "end")
        t1.insert("end", text)

        do_translate()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi AI OCR:\n{e}")
# combobox for from-language selection
a = tk.StringVar()
auto_detect = ttk.Combobox(root, width=20,textvariable=a, state='readonly', font=('Corbel', 20, 'bold'), )

auto_detect['values'] = ['Auto Detect'] + list(LANGUAGE_CODES.keys())

auto_detect.place(x=50, y=140)
auto_detect.current(0)
l = tk.StringVar()

# combobox for to-language selection
choose_langauge = ttk.Combobox(root, width=20, textvariable=l, state='readonly', font=('Corbel', 20, 'bold'))
choose_langauge['values'] = list(LANGUAGE_CODES.keys())

choose_langauge.place(x=600, y=140)
choose_langauge.current(0)
auto_detect.bind("<<ComboboxSelected>>", auto_translate)
choose_langauge.bind("<<ComboboxSelected>>", auto_translate)

# ===== ICON ĐẢO NGƯỢC NGÔN NGỮ =====
swap_icon_img = Image.open(
    os.path.join(BASE_DIR, "resources", "icons", "daonguoc.png")
)
swap_icon_img = swap_icon_img.resize((50, 50), Image.Resampling.LANCZOS)
swap_icon = ImageTk.PhotoImage(swap_icon_img)

def rounded_button(parent, text, image, command, width=140, height=45, radius=20):

    canvas = Canvas(
        parent,
        width=width,
        height=height,
        bg=BG_MAIN,
        highlightthickness=0,
        cursor="hand2"
    )

    def create_rounded_rect(x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    # tạo rect
    rect = create_rounded_rect(0, 0, width, height, radius, fill=BTN_SOFT, outline="")

    # icon
    icon_x = 20   
    text_x = icon_x + 22  

    icon_id = canvas.create_image(icon_x, height//2, image=image)

    text_id = canvas.create_text(
        text_x,
        height//2,
        text=text,
        anchor="w",   
        fill=TEXT_DARK,
        font=('Corbel', 16, 'bold')
    )

    # hover 
    def on_enter(e):
        canvas.itemconfig(rect, fill=BTN_MAIN)
        canvas.itemconfig(text_id, fill="white")

    def on_leave(e):
        canvas.itemconfig(rect, fill=BTN_SOFT)
        canvas.itemconfig(text_id, fill=TEXT_DARK)

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    def handle_click(e):
        root.focus_force()
        root.update()
        command()

    canvas.bind("<Button-1>", handle_click)

    canvas.image = image
    return canvas
# ===== BUTTON ĐẢO NGƯỢC NGÔN NGỮ =====
swap_button = Button(
    root,
    image=swap_icon,
    relief=FLAT,
    borderwidth=0,
    cursor="hand2",
    command=swap_languages,
    bg=BG_MAIN,
    activebackground=BG_MAIN
)

swap_button.image = swap_icon
# Đặt ở GIỮA 2 combobox
swap_button.place(x=500, y=135)
# Load and resize the icon images for buttons
translate_text_icon_img = Image.open(
    os.path.join(BASE_DIR, "resources", "icons", "hinhanh.png")
)
resized_translate_text_icon = translate_text_icon_img.resize((32, 32), Image.Resampling.LANCZOS)
translate_text_icon = ImageTk.PhotoImage(resized_translate_text_icon)

clear_text_icon_img = Image.open(
    os.path.join(BASE_DIR, "resources", "icons", "eraser.png")
)
resized_clear_text_icon = clear_text_icon_img.resize(
    (32, 32), Image.Resampling.LANCZOS
)
clear_text_icon = ImageTk.PhotoImage(resized_clear_text_icon)


copy_text_icon_img = Image.open(
    os.path.join(BASE_DIR, "resources", "icons", "copy.png")
)
resized_copy_text_icon = copy_text_icon_img.resize(
    (32, 32), Image.Resampling.LANCZOS
)
copy_text_icon = ImageTk.PhotoImage(resized_copy_text_icon)


read_aloud_icon_img = Image.open(
    os.path.join(BASE_DIR, "resources", "icons", "text_to_speech.png")
)
resized_read_aloud_icon = read_aloud_icon_img.resize(
    (32, 32), Image.Resampling.LANCZOS
)
read_aloud_icon = ImageTk.PhotoImage(resized_read_aloud_icon)


voice_input_icon_img = Image.open(
    os.path.join(BASE_DIR, "resources", "icons", "voice_recognition.png")
)
resized_voice_input_icon = voice_input_icon_img.resize(
    (32, 32), Image.Resampling.LANCZOS
)
voice_input_icon = ImageTk.PhotoImage(resized_voice_input_icon)
mic_img = Image.open(
    os.path.join(BASE_DIR, "resources", "icons", "mic.png")
)

mic_img = mic_img.resize((120, 120), Image.Resampling.LANCZOS)
mic_icon = ImageTk.PhotoImage(mic_img)



# Text Widget settings used in Tkinter GUI
t1 = Text(
    root,
    width=45,
    height=13,
    font=('Calibri', 16),
    bg=BG_PANEL,
    fg=TEXT_DARK,
    relief=FLAT,
    highlightthickness=2,
    highlightbackground="#CFE4FF",
    highlightcolor=BTN_MAIN
)
t1.place(x=20, y=200)
t1.bind("<KeyRelease>", auto_translate)
t2 = Text(
    root,
    width=45,
    height=13,
    font=('Calibri', 16),
    bg=BG_PANEL,
    fg=TEXT_DARK,
    relief=FLAT,
    highlightthickness=2,
    highlightbackground="#CFE4FF",
    highlightcolor=BTN_MAIN
)
t2.place(x=550, y=200)
# ===== BUTTON FRAME =====
button_frame = Frame(root, bg=BG_MAIN)
button_frame.place(x=40, y=560)


image_translate_btn = rounded_button(
    root, " Image Translate ", translate_text_icon, translate_image_ai, 200, 50
)
image_translate_btn.place(x=20, y=565)

clear_button = rounded_button(
    root, " Clear ", clear_text_icon, clear, 140, 50
)
clear_button.place(x=240, y=565)

copy_button = rounded_button(
    root, " Copy ", copy_text_icon, copy, 140, 50
)
copy_button.place(x=400, y=565)

read_aloud = rounded_button(
    root, " Read Aloud ", read_aloud_icon, texttospeech, 170, 50
)
read_aloud.place(x=560, y=565)

voice_translate_btn = rounded_button(
    root, " Voice Translate ", voice_input_icon, smart_voice_translate, 220, 50
)
voice_translate_btn.place(x=750, y=565)

def open_feedback_window():
    feedback_win = Toplevel(root)
    feedback_win.title("Góp ý / Báo lỗi")
    feedback_win.geometry("400x350")
    feedback_win.configure(bg="#EAF4FF")
    feedback_win.resizable(False, False)

    Label(
        feedback_win,
        text="💬 Góp ý hoặc báo lỗi",
        font=("Segoe UI", 14, "bold"),
        bg="#EAF4FF"
    ).pack(pady=10)

    text_box = Text(
        feedback_win,
        height=10,
        width=40,
        font=("Segoe UI", 10)
    )
    text_box.pack(padx=20, pady=10)

    def submit_feedback():
        content = text_box.get("1.0", "end-1c").strip()

        if not content:
            messagebox.showwarning("Thiếu nội dung", "Vui lòng nhập góp ý!")
            return

        try:
            from database import save_feedback
            save_feedback(current_user_id, content)
        except:
            print("Chưa có bảng feedback")

        messagebox.showinfo("Cảm ơn", "Đã gửi góp ý!")
        feedback_win.destroy()

    Button(
        feedback_win,
        text="📤 Gửi",
        bg="#4DA3FF",
        fg="white",
        command=submit_feedback
    ).pack(pady=10)
def open_restore_window():
    restore_win = Toplevel(root)
    restore_win.title("Khôi phục dữ liệu")
    restore_win.geometry("420x300")
    restore_win.configure(bg="#EAF4FF")
    restore_win.resizable(False, False)

    # ===== HEADER =====
    Label(
        restore_win,
        text="🔄 Khôi phục dữ liệu offline",
        font=("Segoe UI", 14, "bold"),
        bg="#4DA3FF",
        fg="white"
    ).pack(fill=X, pady=5)

    # ===== NỘI DUNG =====
    content_frame = Frame(restore_win, bg="#EAF4FF")
    content_frame.pack(padx=20, pady=15, fill=BOTH, expand=True)

    message = (
        "Dữ liệu offline hiện đã được tải và lưu đầy đủ trên máy của bạn.\n\n"
        "Nếu bạn vẫn không thể tra từ offline được, hãy nhấn nút [Khôi phục] bên dưới.\n\n"
        "Chú ý: Trong quá trình khôi phục, dữ liệu cũ sẽ bị xoá và phần mềm sẽ tự động "
        "tải dữ liệu mới ngay khi quay về trang chủ."
    )

    Label(
        content_frame,
        text=message,
        font=("Segoe UI", 10),
        bg="#EAF4FF",
        justify="left",
        wraplength=360
    ).pack()

    # ===== BUTTON =====
    btn_frame = Frame(content_frame, bg="#EAF4FF")
    btn_frame.pack(pady=20, fill=X)

    def do_restore():
        try:
            # 👉 XÓA dữ liệu cũ (ví dụ history)
            from database import connect
            conn = connect()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM history")
            conn.commit()
            conn.close()

            messagebox.showinfo("Thành công", "Đã khôi phục dữ liệu offline!")

            restore_win.destroy()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khôi phục:\n{e}")

    Button(
        btn_frame,
        text="Hủy bỏ",
        bg="#CCCCCC",
        fg="black",
        command=restore_win.destroy
    ).pack(side=RIGHT, padx=5, ipadx=10, ipady=5)

    Button(
        btn_frame,
        text="Khôi phục",
        bg="#4DA3FF",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=do_restore
    ).pack(side=RIGHT, padx=5, ipadx=10, ipady=5)
def open_privacy_policy():
    policy_win = Toplevel(root)
    policy_win.title("Chính sách bảo mật")
    policy_win.geometry("450x500")
    policy_win.configure(bg="#EAF4FF")
    policy_win.resizable(False, False)

    # ===== HEADER =====
    Label(
        policy_win,
        text="🔒 CHÍNH SÁCH BẢO MẬT",
        font=("Segoe UI", 14, "bold"),
        bg="#4DA3FF",
        fg="white"
    ).pack(fill=X)

    # ===== CONTENT FRAME =====
    frame = Frame(policy_win, bg="#EAF4FF")
    frame.pack(fill=BOTH, expand=True, padx=15, pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    text = Text(
        frame,
        wrap=WORD,
        yscrollcommand=scrollbar.set,
        font=("Segoe UI", 10),
        bg="white",
        relief=FLAT
    )
    text.pack(fill=BOTH, expand=True)

    scrollbar.config(command=text.yview)

    # ===== NỘI DUNG =====
    policy_text = """
1. Thu thập dữ liệu
Ứng dụng chỉ lưu các thông tin cần thiết như:
- Tên, email, số điện thoại
- Lịch sử dịch (để cải thiện trải nghiệm)

2. Mục đích sử dụng
Dữ liệu được sử dụng để:
- Lưu lịch sử dịch
- Cá nhân hóa trải nghiệm người dùng
- Cải thiện chất lượng dịch

3. Bảo mật
Chúng tôi cam kết:
- Không chia sẻ dữ liệu cho bên thứ ba
- Mã hóa mật khẩu người dùng
- Bảo vệ dữ liệu trên thiết bị của bạn

4. Đăng nhập bên thứ ba
Khi đăng nhập bằng Google/Facebook:
- Chỉ lấy thông tin cơ bản (tên, email)
- Không truy cập dữ liệu cá nhân khác

5. Quyền của người dùng
Bạn có quyền:
- Xem thông tin cá nhân
- Gửi góp ý / báo lỗi

6. Liên hệ
Mọi thắc mắc xin liên hệ:
support@meddu.app
"""

    text.insert("1.0", policy_text)
    text.config(state="disabled")

    # ===== BUTTON =====
    Button(
        policy_win,
        text="Đóng",
        bg="#4DA3FF",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=policy_win.destroy
    ).pack(pady=10)

def open_rating_window():
    rating_win = Toplevel(root)
    rating_win.title("Đánh giá ứng dụng")
    rating_win.geometry("400x350")
    rating_win.configure(bg="#EAF4FF")
    rating_win.resizable(False, False)

    # ===== HEADER =====
    Label(
        rating_win,
        text="⭐ Đánh giá ứng dụng",
        font=("Segoe UI", 14, "bold"),
        bg="#4DA3FF",
        fg="white"
    ).pack(fill=X, pady=5)

    # ===== CHỌN SAO =====
    rating_value = tk.IntVar(value=5)

    star_frame = Frame(rating_win, bg="#EAF4FF")
    star_frame.pack(pady=15)

    def set_rating(val):
        rating_value.set(val)
        update_stars()

    stars = []

    def update_stars():
        for i, lbl in enumerate(stars):
            if i < rating_value.get():
                lbl.config(text="★", fg="gold")
            else:
                lbl.config(text="☆", fg="gray")

    for i in range(5):
        lbl = Label(
            star_frame,
            text="☆",
            font=("Segoe UI", 24),
            bg="#EAF4FF",
            cursor="hand2"
        )
        lbl.pack(side=LEFT, padx=5)
        lbl.bind("<Button-1>", lambda e, v=i+1: set_rating(v))
        stars.append(lbl)

    update_stars()

    # ===== NHẬN XÉT =====
    text_box = Text(
        rating_win,
        height=6,
        font=("Segoe UI", 10)
    )
    text_box.pack(padx=20, pady=10, fill=X)

    # ===== SUBMIT =====
    def submit_rating():
        content = text_box.get("1.0", "end-1c").strip()
        rating = rating_value.get()

        try:
            from database import save_rating
            save_rating(current_user_id, rating, content)
        except:
            print("Chưa có bảng rating")

        messagebox.showinfo("Cảm ơn", f"Bạn đã đánh giá {rating}⭐")
        rating_win.destroy()

    Button(
        rating_win,
        text="Gửi đánh giá",
        bg="#4DA3FF",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=submit_rating
    ).pack(pady=10)

def open_share_window():
    share_win = Toplevel(root)
    share_win.title("Chia sẻ ứng dụng")
    share_win.geometry("400x300")
    share_win.configure(bg="#EAF4FF")
    share_win.resizable(False, False)

    Label(
        share_win,
        text="📤 Chia sẻ với bạn bè",
        font=("Segoe UI", 14, "bold"),
        bg="#EAF4FF"
    ).pack(pady=10)

    share_text = "Mình đang dùng app dịch rất xịn! Bạn thử nhé"

    text_box = Text(
        share_win,
        height=5,
        width=40,
        font=("Segoe UI", 10)
    )
    text_box.pack(padx=20, pady=10)
    text_box.insert("1.0", share_text)

    # ===== COPY =====
    def copy_text():
        import pyperclip
        pyperclip.copy(share_text)
        messagebox.showinfo("Đã copy", "Đã copy nội dung!")

    # ===== EMAIL =====
    def send_email():
        import webbrowser
        subject = "Giới thiệu ứng dụng dịch"
        body = share_text
        url = f"mailto:?subject={subject}&body={body}"
        webbrowser.open(url)

    btn_frame = Frame(share_win, bg="#EAF4FF")
    btn_frame.pack(pady=10)

    Button(
        btn_frame,
        text="📋 Copy",
        bg="#4DA3FF",
        fg="white",
        width=10,
        command=copy_text
    ).grid(row=0, column=0, padx=10)

    Button(
        btn_frame,
        text="📧 Email",
        bg="#34C759",
        fg="white",
        width=10,
        command=send_email
    ).grid(row=0, column=1, padx=10)

def create_profile_window():
    global scrollable_frame
    profile = Toplevel(root)
    profile.protocol("WM_DELETE_WINDOW", profile.withdraw)
    profile.title("User Profile")
    profile.geometry("700x700")
    profile.configure(bg=BG_MAIN)
    profile.resizable(False, False)
    
    # ===== HEADER =====
    header = Frame(profile, bg=BTN_MAIN, height=80)
    header.pack(fill=X)
    
    Label(
        header,
        text="TÀI KHOẢN",
        font=("Segoe UI", 18, "bold"),
        bg=BTN_MAIN,
        fg="white"
    ).pack(pady=20)

    # ===== ICON BÁNH RĂNG =====
    try:
        gear = Image.open(os.path.join(BASE_DIR, "resources", "icons", "banhrang.png"))
        gear = gear.resize((45, 45))  
        gear_icon = ImageTk.PhotoImage(gear)

        btn_setting = Label(
            header,
            image=gear_icon,
            bg=BTN_MAIN,
            cursor="hand2"
        )
        btn_setting.image = gear_icon
        btn_setting.place(relx=0.93, rely=0.5, anchor="center")

        # ===== POPUP SETTINGS (NEW) =====
        def open_setting(event=None):
            setting_win = Toplevel(profile)
            setting_win.title("Cài đặt")
            setting_win.geometry("340x470")
            setting_win.configure(bg=BG_MAIN)
            setting_win.resizable(False, False)

            header = Frame(setting_win, bg=BTN_MAIN, height=60)
            header.pack(fill=X)

            Label(
            header,
            text="⚙ CÀI ĐẶT",
            font=("Segoe UI", 14, "bold"),
            bg=BTN_MAIN,
            fg="white"
            ).pack(pady=15)

            def create_btn(text, cmd):
                frame = Frame(setting_win, bg=BG_MAIN)
                frame.pack(padx=20, pady=6, fill="x")

                btn = Frame(
                    frame,
                    bg="white",
                    highlightthickness=1,
                    highlightbackground="#D0E6FF",
                    bd=0
                )
                btn.pack(fill="x")

                lbl = Label(
                    btn,
                    text=text,
                    font=("Segoe UI", 11, "bold"),
                    bg="white",
                    fg="#1F2937",
                    anchor="w",
                    padx=18,
                    pady=14,
                    cursor="hand2"
                )
                lbl.pack(fill="x")

    # ===== HOVER =====
                def on_enter(e):
                    if "Đăng xuất" in text:
                        btn.config(bg="#FFEEEE")
                        lbl.config(bg="#FFEEEE", fg="#FF4D4D")
                    else:
                        btn.config(bg="#EAF4FF")
                        lbl.config(bg="#EAF4FF")

                def on_leave(e):
                    btn.config(bg="white")
                    lbl.config(bg="white")

    # ===== CLICK (NHẤN XUỐNG) =====
                def on_click(e):
                    btn.config(bg="#4DA3FF")
                    lbl.config(bg="#4DA3FF", fg="white")

                def on_release(e):
                    btn.config(bg="#EAF4FF")
                    lbl.config(bg="#EAF4FF", fg="#1F2937")
                    cmd()

    # bind sự kiện
                lbl.bind("<Enter>", on_enter)
                lbl.bind("<Leave>", on_leave)
                lbl.bind("<ButtonPress-1>", on_click)
                lbl.bind("<ButtonRelease-1>", on_release)

                return frame

            # ===== BUTTONS =====
            create_btn("💬 Báo lỗi hoặc Góp ý", open_feedback_window)
            create_btn("🔄 Khôi phục dữ liệu offline", open_restore_window)
            create_btn("🔒 Chính sách bảo mật", open_privacy_policy)
            create_btn("⭐ Đánh giá ứng dụng", open_rating_window)
            create_btn("📤 Chia sẻ đến bạn bè", open_share_window)
            
            def save_history_to_file():
                history = get_history(current_user_id)

                if not history:
                    messagebox.showwarning("Trống", "Không có lịch sử để lưu!")
                    return

                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text file", "*.txt")],
                    title="Lưu lịch sử"
                )

                if not file_path:
                    return

                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        for h in history:
                            source, translated, from_lang, to_lang, time, hid = h
                            f.write(f"[{time}] {from_lang} -> {to_lang}\n")
                            f.write(f"  {source}\n")
                            f.write(f"  -> {translated}\n\n")

                    messagebox.showinfo("Thành công", "Đã lưu lịch sử!")
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))
            # ===== LOGOUT =====
            def logout():
                confirm = messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?")
                if confirm:
                    setting_win.destroy()
                    profile.destroy()
                    root.destroy()

                    import subprocess, sys
                    subprocess.Popen([sys.executable, "login.py"])

            create_btn("🚪 Đăng xuất", logout)
        btn_setting.bind("<Button-1>", open_setting)

    except:
        Label(
            header,
            text="⚙",
            font=("Segoe UI", 20),  
            bg=BTN_MAIN,
            fg="white",
            cursor="hand2"
        ).place(relx=0.96, rely=0.5, anchor="center")
    refresh_history()
    
    # ===== CARD =====
    card = Frame(profile, bg="white")
    card.place(x=20, y=100, width=660, height=600)

    # ===== AVATAR =====
    try:
        img = Image.open(os.path.join(BASE_DIR, "resources", "icons", "dangnhap.png"))
        img = img.resize((70, 70))
        avatar = ImageTk.PhotoImage(img)

        Label(card, image=avatar, bg="white").pack(pady=10)
        card.avatar = avatar
    except:
        pass

    # ===== DATA DB =====
    user_data = get_user_info(current_user_id)

    if user_data:
        name, email, phone, role, login_from = user_data
    else:
        name, email, phone, role, login_from = ("Unknown", "", "", "user", "system")

    login_map = {
        "google": "Google",
        "facebook": "Facebook",
        "system": "Hệ thống"
    }
    login_text = login_map.get(login_from, "Hệ thống")

    # ===== INFO =====
    info_frame = Frame(card, bg="white")
    info_frame.pack(pady=5, padx=20, fill="x")

    def row(r, title, value):
        Label(
        info_frame,
        text=title,
        font=("Segoe UI", 11, "bold"),
        bg="white",
        fg="#1F2937"
    ).grid(row=r, column=0, sticky="w", pady=6)

        Label(
        info_frame,
        text=value,
        font=("Segoe UI", 13, "bold"),  
        fg="#111827",
        bg="white"
    ).grid(row=r, column=1, sticky="w", padx=12)

    row(0, "Tên:", name)
    row(1, "Email:", email)
    row(2, "SĐT:", phone)
    row(3, "Vai trò:", role)
    row(4, "Đăng nhập:", login_text)

    # ===== HISTORY =====
    top_history = Frame(card, bg="white")
    top_history.pack(fill="x", padx=20, pady=(10, 0))

    Label(
    top_history,
    text="Lịch sử dịch",
    font=("Segoe UI", 12, "bold"),
    bg="white"
).pack(side="left")

    Button(
    top_history,
    text="Xem tất cả",
    bg="#4DA3FF",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=open_full_history
).pack(side="right")    
    

    history_frame = Frame(card, bg="white")
    history_frame.pack(padx=15, pady=5, fill="both", expand=True)
    history_frame.config(height=250)

    canvas = Canvas(history_frame, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(history_frame, orient="vertical", command=canvas.yview)

    global scrollable_frame
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    refresh_history()
    return profile
root.mainloop()
