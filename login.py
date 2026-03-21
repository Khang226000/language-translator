import tkinter as tk
from tkinter import *
from tkinter import messagebox
import threading
from PIL import Image, ImageTk
import os
from facebook_login import login_facebook
from google_login import login_google, get_user_info
from database import register_user, login_user, check_user_exists

def round_rect(canvas, x1, y1, x2, y2, r=25, **kwargs):
    return canvas.create_polygon(
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
        x1, y1,
        smooth=True, splinesteps=36, **kwargs
    )
# ---------- COLORS ----------
BG = "#42A5F5"        
HEADER = "#42A5F5"    
PRIMARY = "#42A5F5"   
CARD = "#FFFFFF"
LINE = "#90CAF9"      

root = tk.Tk()
root.title("Login")
root.geometry("420x720")
root.configure(bg=BG)
root.resizable(False, False)

current_user_id = None
# Canvas để vẽ card trắng bo góc
canvas = Canvas(root, bg=BG, highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

# ---------- HEADER ----------
header = Frame(root, bg=HEADER, height=160)
header.pack(fill="x")

# ---------- CARD ----------

# Nền xanh nhạt
root.configure(bg=BG)


# ---------- LOGO ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    logo_path = os.path.join(BASE_DIR, "resources", "icons", "dangnhap.png")
    print("PATH:", logo_path)  # debug

    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((100, 100))

    logo_tk = ImageTk.PhotoImage(logo_img)

    logo_label = Label(root, image=logo_tk, bg=HEADER, bd=0)
    logo_label.image = logo_tk

    logo_label.place(x=170, y=40)

except Exception as e:
    print("Lỗi load logo:", e)
# Card trắng (khung trong)
CARD_TOP = 140
CARD_HEIGHT = 500

round_rect(canvas, 30, CARD_TOP, 390, CARD_TOP + CARD_HEIGHT, r=30, fill=CARD)

# Frame chứa nội dung
card = Frame(root, bg=CARD)
card.place(x=40, y=CARD_TOP + 20, width=340, height=CARD_HEIGHT - 40)


# ---------- LOGIN ----------
def login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    if not username or not password:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tài khoản và mật khẩu")
        return

    status_label.config(text="Đang đăng nhập...")

    def run_login():
        user = login_user(username, password)

        if user:
            global current_user_id
            current_user_id = user[0]

            from database import get_user_info
            user_data = get_user_info(current_user_id)

            if not user_data:
                root.after(0, lambda: messagebox.showerror("Lỗi", "Không lấy được dữ liệu user"))
                return

            role = user_data[3]  # role nằm ở cột thứ 4

            def success():
                messagebox.showinfo("Đăng nhập", "Đăng nhập thành công!")
                root.destroy()

                import subprocess, sys

                # ===== PHÂN LUỒNG ADMIN / USER =====
                if role == "admin":
                    subprocess.Popen([
                        sys.executable,
                        "language-translator/admin_dashboard.py",
                        str(current_user_id)
                    ])
                else:
                    subprocess.Popen([
                        sys.executable,
                        "language-translator/language_translator.py",
                        str(current_user_id)
                    ])

            root.after(0, success)

        else:
            root.after(0, lambda: messagebox.showerror(
                "Lỗi",
                "Sai tài khoản, mật khẩu hoặc tài khoản không tồn tại"
            ))

    threading.Thread(target=run_login, daemon=True).start()

# ---------- GOOGLE LOGIN ----------
def google_login_handler():
    def run_google():
        try:
            creds = login_google()
            user = get_user_info(creds)

            name = user["name"]
            email = user["email"]

            register_user(name, email, "", "google_login")

            db_user = login_user(email, "google_login")
            if not db_user:
                register_user(name, email, "", "google_login", "google")
                db_user = login_user(email, "google_login")

            if db_user:
                global current_user_id
                current_user_id = db_user[0]

                def success():
                    messagebox.showinfo("OK", "Login Google thành công!")
                    root.destroy()

                    import subprocess, sys
                    subprocess.Popen([sys.executable, "language-translator/language_translator.py"])

                root.after(0, success)

        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Google Error", str(e)))

    threading.Thread(target=run_google, daemon=True).start()

# ---------- REGISTER ----------
def register():
    win = Toplevel(root)
    win.title("Register")
    win.geometry("420x720")
    win.configure(bg=BG)
    win.resizable(False, False)

    # HEADER
    header = Frame(win, bg=HEADER, height=160)
    header.pack(fill="x")
    # ---------- LOGO REGISTER ----------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    try:
        logo_path = os.path.join(BASE_DIR, "resources", "icons", "dangnhap.png")

        logo_img = Image.open(logo_path).convert("RGBA")
        logo_img = logo_img.resize((100, 100))

        logo_tk = ImageTk.PhotoImage(logo_img)

        logo_label = Label(header, image=logo_tk, bg=HEADER, bd=0)
        logo_label.image = logo_tk

    # căn giữa + xích lên giống login
        logo_label.place(relx=0.5, y=10, anchor="n")

    except Exception as e:
        print("Lỗi logo register:", e)

    # CARD
    # CANVAS nền để vẽ bo góc
    canvas = Canvas(win, bg=BG, highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # Vẽ card bo góc
    CARD_TOP = 140
    CARD_HEIGHT = 550
    round_rect(canvas, 30, CARD_TOP, 390, CARD_TOP + CARD_HEIGHT, r=30, fill=CARD)

    # Frame chứa nội dung (đặt đè lên)
    # Nền xanh nhạt
    win.configure(bg=BG)

    # Frame nội dung
    card = Frame(win, bg=CARD)
    card.place(x=40, y=CARD_TOP + 20, width=340, height=CARD_HEIGHT - 40)

    Label(
        card,
        text="SIGN UP",
        font=("Segoe UI", 18, "bold"),
        fg=PRIMARY,
        bg=CARD
    ).pack(pady=20)

    # USERNAME
    Label(card, text="Username", bg=CARD, fg="#666", font=("Segoe UI", 9)).pack(anchor="w", padx=30)
    entry_name = Entry(card, bd=0, font=("Segoe UI", 12))
    entry_name.pack(fill="x", padx=30, pady=(5,15))
    Frame(card, height=2, bg=LINE).pack(fill="x", padx=30)

    # EMAIL
    Label(card, text="Email", bg=CARD, fg="#666", font=("Segoe UI", 9)).pack(anchor="w", padx=30, pady=(10,0))
    entry_email = Entry(card, bd=0, font=("Segoe UI", 12))
    entry_email.pack(fill="x", padx=30, pady=(5,15))
    Frame(card, height=2, bg=LINE).pack(fill="x", padx=30)

    # PHONE
    Label(card, text="Phone", bg=CARD, fg="#666", font=("Segoe UI", 9)).pack(anchor="w", padx=30, pady=(10,0))
    entry_phone = Entry(card, bd=0, font=("Segoe UI", 12))
    entry_phone.pack(fill="x", padx=30, pady=(5,15))
    Frame(card, height=2, bg=LINE).pack(fill="x", padx=30)

    # PASSWORD
    Label(card, text="Password", bg=CARD, fg="#666", font=("Segoe UI", 9)).pack(anchor="w", padx=30, pady=(10,0))
    entry_pass = Entry(card, show="*", bd=0, font=("Segoe UI", 12))
    entry_pass.pack(fill="x", padx=30, pady=(5,15))
    Frame(card, height=2, bg=LINE).pack(fill="x", padx=30)

    # REGISTER BUTTON
    def do_register():
        print("CLICK REGISTER")
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        phone = entry_phone.get().strip()
        password = entry_pass.get().strip()

        
        if not name or not email or not phone or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        
        if "@" not in email or "." not in email:
            messagebox.showwarning("Lỗi email", "Email không hợp lệ!")
            return

        
        if not phone.isdigit():
            messagebox.showwarning("Lỗi", "Số điện thoại phải là số!")
            return

        
        if len(password) < 6:
            messagebox.showwarning("Lỗi", "Mật khẩu phải ≥ 6 ký tự!")
            return
        
        existing_user = check_user_exists(name, email, phone)
        print("DB:", existing_user)  

        if existing_user is not None:
            
            try:
                if existing_user[1] == name:
                    messagebox.showerror("Lỗi", "Username đã tồn tại!")
                elif existing_user[2] == email:
                    messagebox.showerror("Lỗi", "Email đã tồn tại!")
                elif existing_user[3] == phone:
                    messagebox.showerror("Lỗi", "Số điện thoại đã tồn tại!")
                else:
                    messagebox.showerror("Lỗi", "Thông tin đã tồn tại!")
            except:
                messagebox.showerror("Lỗi", "Dữ liệu đã tồn tại!")
            return
        
        ok = register_user(name, email, phone, password)

        if ok:
            messagebox.showinfo("Thành Công", "Tạo tài khoản thành công!")
            win.destroy()
        else:
            messagebox.showerror("Error", "Đăng ký thất bại!")

    btn_canvas = Canvas(card, width=220, height=50, bg=CARD, highlightthickness=0, cursor="hand2")
    btn_canvas.pack(pady=25)

    round_rect(btn_canvas, 0, 0, 220, 50, r=25, fill="#64B5F6")

    btn_canvas.create_text(110, 25, text="SIGN UP", fill="white",
                       font=("Segoe UI", 11, "bold"))
    
    btn_canvas.bind("<Button-1>", lambda e: do_register())
    
    back_label = Label(
    card,
    text="Already have an account? Login",
    fg="#42A5F5",
    bg=CARD,
    cursor="hand2",
    font=("Segoe UI", 10, "underline")
)
    back_label.pack(pady=(10, 0))
    back_label.bind("<Button-1>", lambda e: win.destroy())
    

    def on_enter(e):
        back_label.config(fg="#1B4F72")

    def on_leave(e):
        back_label.config(fg="#42A5F5")

    back_label.bind("<Enter>", on_enter)
    back_label.bind("<Leave>", on_leave)

# ---------- UI INSIDE CARD ----------
Label(
    card,
    text="LOGIN",
    font=("Segoe UI", 18, "bold"),
    fg=PRIMARY,
    bg=CARD
).pack(pady=20)

# USERNAME
Label(card, text="Username", bg=CARD, fg="#888").pack(anchor="w", padx=30)
entry_user = Entry(card, bd=0, font=("Segoe UI", 11))
entry_user.pack(fill="x", padx=30)
Frame(card, height=1, bg=LINE).pack(fill="x", padx=30, pady=5)

# PASSWORD
Label(card, text="Password", bg=CARD, fg="#888").pack(anchor="w", padx=30, pady=(10,0))
entry_pass = Entry(card, show="*", bd=0, font=("Segoe UI", 11))
entry_pass.pack(fill="x", padx=30)
Frame(card, height=1, bg=LINE).pack(fill="x", padx=30, pady=5)


# LOGIN BUTTON
btn_canvas = Canvas(card, width=220, height=50, bg=CARD, highlightthickness=0, cursor="hand2")
btn_canvas.pack(pady=25)

round_rect(btn_canvas, 0, 0, 220, 50, r=25, fill="#64B5F6")

btn_canvas.create_text(110, 25, text="LOGIN", fill="white",
                       font=("Segoe UI", 11, "bold"))

btn_canvas.bind("<Button-1>", lambda e: login())

# REGISTER
signup_label = Label(
    card,
    text="Don't have an account? Sign up",
    fg="#42A5F5",
    bg=CARD,
    cursor="hand2",
    font=("Segoe UI", 10, "underline")
)
signup_label.pack()

# Gán sự kiện click
signup_label.bind("<Button-1>", lambda e: register())
def on_enter(e):
    signup_label.config(fg="#1B4F72")

def on_leave(e):
    signup_label.config(fg=PRIMARY)

signup_label.bind("<Enter>", on_enter)
signup_label.bind("<Leave>", on_leave)
Label(card, text="", bg=CARD).pack()

# ---------- GOOGLE BUTTON ----------
google_btn = Canvas(card, width=260, height=45, bg=CARD, highlightthickness=0, cursor="hand2")
google_btn.pack(pady=5)

round_rect(google_btn, 0, 0, 260, 45, r=22, fill="#DB4437")

google_btn.create_text(
    130, 22,
    text="Đăng nhập với Google",
    fill="white",
    font=("Segoe UI", 10, "bold")
)

google_btn.bind("<Button-1>", lambda e: google_login_handler())


# ---------- FACEBOOK BUTTON ----------
fb_btn = Canvas(card, width=260, height=45, bg=CARD, highlightthickness=0, cursor="hand2")
fb_btn.pack(pady=5)

round_rect(fb_btn, 0, 0, 260, 45, r=22, fill="#1877F2")

fb_btn.create_text(
    130, 22,
    text="Đăng nhập với Facebook",
    fill="white",
    font=("Segoe UI", 10, "bold")
)

fb_btn.bind("<Button-1>", lambda e: login_facebook())

status_label = Label(card, text="", bg=CARD)
status_label.pack(pady=5)


root.mainloop()