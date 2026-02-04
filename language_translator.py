import tkinter as tk  
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image  
from googletrans import Translator  
from tkinter import messagebox
import pyperclip as pc 
from gtts import gTTS  
import os
import speech_recognition as spr 
import webbrowser
import threading
import pyaudio
import numpy as np

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
root = tk.Tk()
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

title_label = Label(
    header,
    text="LANGUAGE TRANSLATOR",
    bg=BG_HEADER,
    fg="white",
    font=("Segoe UI", 30, "bold")
)
title_label.pack(pady=20)

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
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = np.sqrt(np.mean(np.square(np.frombuffer(data, dtype=np.int16))))
        audio_level = min(rms / 3000, 1.0)

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

# For Performing Main Translation Function
def translate():
    language_1 = t1.get("1.0", "end-1c")
    global cl
    cl = choose_langauge.get()

    if language_1 == '':
        messagebox.showerror('Language Translator', 'Please fill the Text Box for Translation')
    else:
         t2.delete(1.0, 'end')
         translator = Translator()
         global output
         output = translator.translate(language_1, dest=cl)
         output = output.text
         t2.insert('end', output)

# For Clearing Textbox Data
def clear():
    t1.delete(1.0, 'end')
    t2.delete(1.0, 'end')
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

# For Converting Translated Text to Speech
def texttospeech():
 global cl
 cl = choose_langauge.get()
 if os.path.exists("text_to_speech.mp3"):
  os.remove("text_to_speech.mp3")
 mytext =output
 language='en'
 if cl == 'English':
     language = 'en'
 elif cl == 'Afrikaans':
     language = 'af'
 elif cl == 'Albanian':
     language = 'sq'
 elif cl == 'Arabic':
     language = 'ar'
 elif cl == 'Armenian':
     language = 'hy'
 elif cl == 'Azerbaijani':
     language = 'az'
 elif cl == 'Basque':
     language = 'eu'
 elif cl == 'Belarusian':
     language = 'be'
 elif cl == 'Bengali':
     language = 'bn'
 elif cl == 'Bosnian':
     language = 'bs'
 elif cl == 'Bulgarian':
     language = 'bg'
 elif cl == 'Catalan':
     language = 'ca'
 elif cl == 'Cebuano':
     language = 'ceb'
 elif cl == 'Chinese':
     language = 'zh'
 elif cl == 'Corsican':
     language = 'co'
 elif cl == 'Croatian':
     language = 'hr'
 elif cl == 'Czech':
     language = 'cs'
 elif cl == 'Danish':
     language = 'da'
 elif cl == 'Dutch':
     language = 'nl'
 elif cl == 'English':
     language = 'en'
 elif cl == 'Esperanto':
     language = 'eo'
 elif cl == 'Estonian':
     language = 'et'
 elif cl == 'Finnish':
     language = 'fi'
 elif cl == 'French':
     language = 'fr'
 elif cl == 'Frisian':
     language = 'fy'
 elif cl == 'Galician':
     language = 'gl'
 elif cl == 'Georgian':
     language = 'ka'
 elif cl == 'German':
     language = 'de'
 elif cl == 'Greek':
     language = 'el'
 elif cl == 'Gujarati':
     language = 'gu'
 elif cl == 'Haitian Creole':
     language = 'ht'
 elif cl == 'Hausa':
     language = 'ha'
 elif cl == 'Hawaiian':
     language = 'haw'
 elif cl == 'Hebrew':
     language = 'he'
 elif cl == 'Hindi':
     language = 'hi'
 elif cl == 'Hmong':
     language = 'hmn'
 elif cl == 'Hungarian':
     language = 'hu'
 elif cl == 'Icelandic':
     language = 'is'
 elif cl == 'Igbo':
     language = 'ig'
 elif cl == 'Indonesian':
     language = 'id'
 elif cl == 'Irish':
     language = 'ga'
 elif cl == 'Italian':
     language = 'it'
 elif cl == 'Japanese':
     language = 'ja'
 elif cl == 'Javanese':
     language = 'jv'
 elif cl == 'Kannada':
     language = 'kn'
 elif cl == 'Kazakh':
     language = 'kk'
 elif cl == 'Khmer':
     language = 'km'
 elif cl == 'Kinyarwanda':
     language = 'rw'
 elif cl == 'Korean':
     language = 'ko'
 elif cl == 'Kurdish':
     language = 'ku'
 elif cl == 'Kyrgyz':
     language = 'ky'
 elif cl == 'Lao':
     language = 'lo'
 elif cl == 'Latin':
     language = 'la'
 elif cl == 'Latvian':
     language = 'lv'
 elif cl == 'Lithuanian':
     language = 'lt'
 elif cl == 'Luxembourgish':
     language = 'lb'
 elif cl == 'Macedonian':
     language = 'mk'
 elif cl == 'Malagasy':
     language = 'mg'
 elif cl == 'Malay':
     language = 'ms'
 elif cl == 'Malayalam':
     language = 'ml'
 elif cl == 'Maltese':
     language = 'mt'
 elif cl == 'Maori':
     language = 'mi'
 elif cl == 'Marathi':
     language = 'mr'
 elif cl == 'Mongolian':
     language = 'mn'
 elif cl == 'Myanmar':
     language = 'my'
 elif cl == 'Nepali':
     language = 'ne'
 elif cl == 'Norwegian':
     language = 'no'
 elif cl == 'Odia':
     language = 'or'
 elif cl == 'Pashto':
     language = 'ps'
 elif cl == 'Persian':
     language = 'fa'
 elif cl == 'Polish':
     language = 'pl'
 elif cl == 'Portuguese':
     language = 'pt'
 elif cl == 'Punjabi':
     language = 'pa'
 elif cl == 'Romanian':
     language = 'ro'
 elif cl == 'Russian':
     language = 'ru'
 elif cl == 'Samoan':
     language = 'sm'
 elif cl == 'Scots Gaelic':
     language = 'gd'
 elif cl == 'Serbian':
     language = 'sr'
 elif cl == 'Sesotho':
     language = 'st'
 elif cl == 'Shona':
     language = 'sn'
 elif cl == 'Sindhi':
     language = 'sd'
 elif cl == 'Sinhala':
     language = 'si'
 elif cl == 'Slovak':
     language = 'sk'
 elif cl == 'Slovenian':
     language = 'sl'
 elif cl == 'Somali':
     language = 'so'
 elif cl == 'Spanish':
     language = 'es'
 elif cl == 'Sundanese':
     language = 'su'
 elif cl == 'Swahili':
     language = 'sw'
 elif cl == 'Swedish':
     language = 'sv'
 elif cl == 'Tajik':
     language = 'tg'
 elif cl == 'Tamil':
     language = 'ta'
 elif cl == 'Tatar':
     language = 'tt'
 elif cl == 'Telugu':
     language = 'te'
 elif cl == 'Thai':
     language = 'th'
 elif cl == 'Turkish':
     language = 'tr'
 elif cl == 'Turkmen':
     language = 'tk'
 elif cl == 'Ukrainian':
     language = 'uk'
 elif cl == 'Urdu':
     language = 'ur'
 elif cl == 'Uyghur':
     language = 'ug'
 elif cl == 'Uzbek':
     language = 'uz'
 elif cl == 'Vietnamese':
     language = 'vi'
 elif cl == 'Welsh':
     language = 'cy'
 elif cl == 'Xhosa':
     language = 'xh'
 elif cl == 'Yiddish':
     language = 'yi'
 elif cl == 'Yoruba':
     language = 'yo'
 elif cl == 'Zulu':
     language = 'zu'
 else:
     language == 'en'
 try:
     myobj = gTTS(text=mytext, lang=language, slow=False)
     myobj.save("text_to_speech.mp3")
     os.system("text_to_speech.mp3")

 except ValueError as e:
     messagebox.showerror('Language Translator', cl+' is currently not supported for Read Aloud (Text to Speech)')
     print(f"An error occurred: {e}")
     # Handle the error or perform any necessary cleanup actions
 except AssertionError as e:
     # Handle the "No text to speak" error
     messagebox.showerror('Language Translator','Please enter the data to be translated before using Read Aloud')
     print("Error:", e)

# For converting Speech to Text [ Please Note : Only English is currently supported as from-language in Speech to Text Translation ]
def speechtotext():
    global listening, audio_thread

    try:
        recog = spr.Recognizer()

        # ===== BẬT MIC =====
        listening = True
        mic_canvas.place(x=820, y=300)

        audio_thread = threading.Thread(
            target=mic_wave_listener,
            daemon=True
        )
        audio_thread.start()

        update_mic_ui()   

        with spr.Microphone() as source:
            recog.adjust_for_ambient_noise(source, duration=0.8)
            audio = recog.listen(source)

        # ===== TẮT MIC =====
        listening = False
        mic_canvas.place_forget()

        text = recog.recognize_google(audio, language="en-US")
        t1.insert("end", text + "\n")

    except spr.UnknownValueError:
        listening = False
        mic_canvas.place_forget()
        messagebox.showerror("Voice Input", "❌ Cannot recognize your voice")

    except spr.RequestError:
        listening = False
        mic_canvas.place_forget()
        messagebox.showerror("Voice Input", "❌ Speech service error")



# combobox for from-language selection
a = tk.StringVar()
auto_detect = ttk.Combobox(root, width=20,textvariable=a, state='readonly', font=('Corbel', 20, 'bold'), )

auto_detect['values'] = (
    'Auto Detect',
    'Afrikaans',
    'Albanian',
    'Arabic',
    'Armenian',
    'Azerbaijani',
    'Basque',
    'Belarusian',
    'Bengali',
    'Bosnian',
    'Bulgarian',
    'Catalan',
    'Cebuano',
    'Chichewa',
    'Chinese',
    'Corsican',
    'Croatian',
    'Czech',
    'Danish',
    'Dutch',
    'English',
    'Esperanto',
    'Estonian',
    'Filipino',
    'Finnish',
    'French',
    'Frisian',
    'Galician',
    'Georgian',
    'German',
    'Greek',
    'Gujarati',
    'Haitian Creole',
    'Hausa',
    'Hawaiian',
    'Hebrew',
    'Hindi',
    'Hmong',
    'Hungarian',
    'Icelandic',
    'Igbo',
    'Indonesian',
    'Irish',
    'Italian',
    'Japanese',
    'Javanese',
    'Kannada',
    'Kazakh',
    'Khmer',
    'Kinyarwanda',
    'Korean',
    'Kurdish',
    'Kyrgyz',
    'Lao',
    'Latin',
    'Latvian',
    'Lithuanian',
    'Luxembourgish',
    'Macedonian',
    'Malagasy',
    'Malay',
    'Malayalam',
    'Maltese',
    'Maori',
    'Marathi',
    'Mongolian',
    'Myanmar',
    'Nepali',
    'Norwegian'
    'Odia',
    'Pashto',
    'Persian',
    'Polish',
    'Portuguese',
    'Punjabi',
    'Romanian',
    'Russian',
    'Samoan',
    'Scots Gaelic',
    'Serbian',
    'Sesotho',
    'Shona',
    'Sindhi',
    'Sinhala',
    'Slovak',
    'Slovenian',
    'Somali',
    'Spanish',
    'Sundanese',
    'Swahili',
    'Swedish',
    'Tajik',
    'Tamil',
    'Tatar',
    'Telugu',
    'Thai',
    'Turkish',
    'Turkmen',
    'Ukrainian',
    'Urdu',
    'Uyghur',
    'Uzbek',
    'Vietnamese',
    'Welsh',
    'Xhosa'
    'Yiddish',
    'Yoruba',
    'Zulu',
)

auto_detect.place(x=50, y=140)
auto_detect.current(0)
l = tk.StringVar()

# combobox for to-language selection
choose_langauge = ttk.Combobox(root, width=20, textvariable=l, state='readonly', font=('Corbel', 20, 'bold'))
choose_langauge['values'] = (
    'Afrikaans',
    'Albanian',
    'Arabic',
    'Armenian',
    'Azerbaijani',
    'Basque',
    'Belarusian',
    'Bengali',
    'Bosnian',
    'Bulgarian',
    'Catalan',
    'Cebuano',
    'Chichewa',
    'Chinese',
    'Corsican',
    'Croatian',
    'Czech',
    'Danish',
    'Dutch',
    'English',
    'Esperanto',
    'Estonian',
    'Filipino',
    'Finnish',
    'French',
    'Frisian',
    'Galician',
    'Georgian',
    'German',
    'Greek',
    'Gujarati',
    'Haitian Creole',
    'Hausa',
    'Hawaiian',
    'Hebrew',
    'Hindi',
    'Hmong',
    'Hungarian',
    'Icelandic',
    'Igbo',
    'Indonesian',
    'Irish',
    'Italian',
    'Japanese',
    'Javanese',
    'Kannada',
    'Kazakh',
    'Khmer',
    'Kinyarwanda',
    'Korean',
    'Kurdish',
    'Kyrgyz',
    'Lao',
    'Latin',
    'Latvian',
    'Lithuanian',
    'Luxembourgish',
    'Macedonian',
    'Malagasy',
    'Malay',
    'Malayalam',
    'Maltese',
    'Maori',
    'Marathi',
    'Mongolian',
    'Myanmar',
    'Nepali',
    'Norwegian'
    'Odia',
    'Pashto',
    'Persian',
    'Polish',
    'Portuguese',
    'Punjabi',
    'Romanian',
    'Russian',
    'Samoan',
    'Scots Gaelic',
    'Serbian',
    'Sesotho',
    'Shona',
    'Sindhi',
    'Sinhala',
    'Slovak',
    'Slovenian',
    'Somali',
    'Spanish',
    'Sundanese',
    'Swahili',
    'Swedish',
    'Tajik',
    'Tamil',
    'Tatar',
    'Telugu',
    'Thai',
    'Turkish',
    'Turkmen',
    'Ukrainian',
    'Urdu',
    'Uyghur',
    'Uzbek',
    'Vietnamese',
    'Welsh',
    'Xhosa'
    'Yiddish',
    'Yoruba',
    'Zulu',
)

choose_langauge.place(x=600, y=140)
choose_langauge.current(0)

# ===== ICON ĐẢO NGƯỢC NGÔN NGỮ =====
swap_icon_img = Image.open(
    os.path.join(BASE_DIR, "resources", "icons", "daonguoc.png")
)
swap_icon_img = swap_icon_img.resize((50, 50), Image.Resampling.LANCZOS)
swap_icon = ImageTk.PhotoImage(swap_icon_img)

def soft_button(**kwargs):
    return Button(
        root,
        bg=BTN_SOFT,
        fg=TEXT_DARK,
        activebackground=BTN_MAIN,
        activeforeground="white",
        relief=FLAT,
        cursor="hand2",
        **kwargs
    )

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
    os.path.join(BASE_DIR, "resources", "icons", "documents.png")
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

# Button settings used in Tkinter GUI
translate_button = Button(
    root,
    text=" Translate ",
    image=translate_text_icon,
    compound="right",
    font=('Corbel', 25, 'bold'),
    bg=BTN_MAIN,
    fg="black",                
    activebackground=BTN_HOVER,
    activeforeground="black",
    relief=FLAT,
    cursor="hand2",
    command=translate
)
translate_button.place(x=40, y=565)

clear_button = soft_button(
    text=" Clear ",
    image=clear_text_icon,
    compound="right",
    font=('Corbel', 18, 'bold'),
    command=clear
)

clear_button.place(x=270, y=565)

copy_button = soft_button(
    text=" Copy ",
    image=copy_text_icon,
    compound="right",
    font=('Corbel', 18, 'bold'),
    command=copy
)
copy_button.place(x=485, y=565)


read_aloud = soft_button(
    text=" Read Aloud ",
    image=read_aloud_icon,
    compound="right",
    font=('Corbel', 18, 'bold'),
    command=texttospeech
)
read_aloud.place(x=650, y=565)


voice_input = soft_button(
    text=" Voice Input ",
    image=voice_input_icon,
    compound="right",
    font=('Corbel', 18, 'bold'),
    command=speechtotext
)
voice_input.place(x=850, y=565)


root.mainloop()
