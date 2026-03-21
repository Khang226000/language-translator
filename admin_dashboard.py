import tkinter as tk
from tkinter import *
from tkinter import ttk
from database import connect, get_user_info
import sys
import os
from datetime import datetime
import subprocess
import csv
from tkinter import filedialog, messagebox
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table

def style_button(btn, color, hover_color):
    btn.config(
        bg=color,
        fg="white",
        activebackground=hover_color,
        activeforeground="white",
        bd=0,
        relief="flat",
        font=("Segoe UI", 11, "bold"),
        padx=18,
        pady=8,
        cursor="hand2"
    )

    def on_enter(e):
        btn['bg'] = hover_color

    def on_leave(e):
        btn['bg'] = color

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
# ===== STYLE =====
BG_MAIN   = "#EEF5FF"
BG_HEADER = "#3B82F6"
BG_CARD   = "#FFFFFF"
TEXT_DARK = "#111827"

root = tk.Tk()
root.title("ADMIN")
root.geometry("1100x700")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

# ===== USER =====
user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
user_data = get_user_info(user_id)

if user_data:
    name, email, phone, role, login_from = user_data
else:
    name, email, phone, role = ("Admin", "", "", "admin")

# ===== HEADER =====
header = Frame(root, bg=BG_HEADER, height=90)
header.pack(fill=X)

Label(header,
      text="ADMIN DASHBOARD",
      font=("Segoe UI", 24, "bold"),
      bg=BG_HEADER,
      fg="white").pack(pady=20)

# ===== BUTTON USER MODE (TO + ĐẸP) =====
def open_user_app():
    root.destroy()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen([sys.executable,
                      os.path.join(BASE_DIR, "language_translator.py"),
                      str(user_id)])

btn_user = Button(root,
    text="🚀 Dùng như User",
    command=open_user_app
)

style_button(btn_user, "#22C55E", "#16A34A")

btn_user.place(x=880, y=25)
def on_enter(e):
    btn_user['bg'] = "#16A34A"

def on_leave(e):
    btn_user['bg'] = "#22C55E"

btn_user.bind("<Enter>", on_enter)
btn_user.bind("<Leave>", on_leave)
style = ttk.Style()
style.theme_use("default")

# ===== TAB STYLE =====
style.configure("TNotebook",
                background=BG_MAIN,
                borderwidth=0)

style.configure("TNotebook.Tab",
                font=("Segoe UI", 12, "bold"),
                padding=[20, 10],   # 👈 làm tab to ra
                background="#DDEBFF",
                foreground="#1F2937")

# Tab khi được chọn
style.map("TNotebook.Tab",
          background=[("selected", "#3B82F6")],
          foreground=[("selected", "white")])

# ===== NOTEBOOK =====
notebook = ttk.Notebook(root)
notebook.place(x=20, y=110, width=1060, height=560)


# ================= DASHBOARD PRO =================
tab1 = Frame(notebook, bg=BG_MAIN)
notebook.add(tab1, text="🏠 Dashboard")

def create_stat_card(parent, title, value, x):
    card = Frame(parent, bg=BG_CARD, bd=1, relief="solid")
    card.place(x=x, y=30, width=230, height=120)

    Label(card, text=title,
          font=("Segoe UI", 11),
          bg=BG_CARD).pack(pady=5)

    lbl = Label(card, text=value,
                font=("Segoe UI", 20, "bold"),
                fg="#2563EB",
                bg=BG_CARD)
    lbl.pack()

    return lbl

# ===== 4 CARD =====
lbl_users = create_stat_card(tab1, "👤 Tổng Users", "0", 30)
lbl_trans = create_stat_card(tab1, "🌐 Tổng Translations", "0", 280)
lbl_today = create_stat_card(tab1, "📅 Hôm nay", "0", 530)
lbl_new_users = create_stat_card(tab1, "🆕 User mới", "0", 780)

btn_refresh = Button(root,
    text="🔄 Refresh",
    command=lambda: [load_stats(), load_activity(), load_users()]
)

style_button(btn_refresh, "#F59E0B", "#D97706")

btn_refresh.place(x=880, y=115)


def on_enter_refresh(e):
    btn_refresh['bg'] = "#D97706"

def on_leave_refresh(e):
    btn_refresh['bg'] = "#F59E0B"

btn_refresh.bind("<Enter>", on_enter_refresh)
btn_refresh.bind("<Leave>", on_leave_refresh)
# ===== RECENT ACTIVITY =====
activity_card = Frame(tab1, bg=BG_CARD, bd=1, relief="solid")
activity_card.place(x=30, y=180, width=600, height=250)

Label(activity_card,
      text="📜 Hoạt động gần đây",
      font=("Segoe UI", 12, "bold"),
      bg=BG_CARD).pack(pady=10)

activity_box = Listbox(activity_card, font=("Segoe UI", 10))
activity_box.pack(fill=BOTH, expand=True, padx=10, pady=5)

def load_activity():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT users.name, history.source_text, history.created_at
    FROM history
    JOIN users ON history.user_id = users.id
    ORDER BY history.created_at DESC
    LIMIT 5
    """)

    activity_box.delete(0, END)

    for row in cursor.fetchall():
        activity_box.insert(END, f"{row[0]}: {row[1]} ({row[2]})")

    conn.close()

load_activity()
# ===== ADMIN INFO (RIGHT - ĐẸP HƠN) =====
admin_card = Frame(tab1, bg=BG_CARD, bd=1, relief="solid")
admin_card.place(x=700, y=180, width=330, height=260)

Label(admin_card,
      text="👤 Thông tin Admin",
      font=("Segoe UI", 14, "bold"),
      bg=BG_CARD).pack(pady=10)

Label(admin_card,
      text=f"Username: {name}",
      font=("Segoe UI", 11),
      anchor="w",
      bg=BG_CARD).pack(fill="x", padx=20, pady=5)

Label(admin_card,
      text=f"Email: {email}",
      font=("Segoe UI", 11),
      anchor="w",
      bg=BG_CARD).pack(fill="x", padx=20, pady=5)

Label(admin_card,
      text=f"Vai trò: {role}",
      font=("Segoe UI", 11, "bold"),
      fg="#2563EB",
      anchor="w",
      bg=BG_CARD).pack(fill="x", padx=20, pady=5)

def load_stats():
    conn = connect()
    cursor = conn.cursor()

    # tổng user
    cursor.execute("SELECT COUNT(*) FROM users")
    lbl_users.config(text=cursor.fetchone()[0])

    # tổng lượt dịch
    cursor.execute("SELECT COUNT(*) FROM history")
    lbl_trans.config(text=cursor.fetchone()[0])

    # hôm nay
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT COUNT(*) FROM history
    WHERE DATE(created_at) = ?
    """, (today,))
    lbl_today.config(text=cursor.fetchone()[0])

    # user mới hôm nay
    cursor.execute("""
    SELECT COUNT(*) FROM users
    WHERE DATE(created_at) = ?
    """, (today,))
    lbl_new_users.config(text=cursor.fetchone()[0])

    conn.close()
load_stats()
load_activity()
# ================= USERS =================
tab2 = Frame(notebook, bg=BG_MAIN)
notebook.add(tab2, text="Users")

# SEARCH
search_frame = Frame(tab2, bg=BG_MAIN)
search_frame.pack(fill=X, padx=20, pady=10)

Label(search_frame, text="🔍 Tìm user:",
      font=("Segoe UI", 11),
      bg=BG_MAIN).pack(side=LEFT)

search_entry = Entry(search_frame, width=30)
search_entry.pack(side=LEFT, padx=10)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=30,
                fieldbackground="white",
                bordercolor="#D1D5DB",
                borderwidth=1)

style.configure("Treeview.Heading",
                font=("Segoe UI", 11, "bold"),
                background="#3B82F6",
                foreground="white",
                relief="flat")

style.map("Treeview",
          background=[("selected", "#BFDBFE")])

# TABLE
columns = ("ID", "Tên", "Email", "Role")
tree = ttk.Treeview(tab2,
                    columns=columns,
                    show="headings",
                    height=15,
                    style="Treeview")

tree.pack(fill=BOTH, expand=True, padx=20, pady=10)
tree.tag_configure('row', background='white')
tree.tag_configure('alt', background='#F9FAFB')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=180)

def load_users(keyword=""):
    for i in tree.get_children():
        tree.delete(i)

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT users.id, users.name, users.email, roles.name
    FROM users
    LEFT JOIN roles ON users.role_id = roles.id
    WHERE users.name LIKE ?
    """, (f"%{keyword}%",))

    rows = cursor.fetchall()

    for i, row in enumerate(rows):
        tag = 'alt' if i % 2 == 0 else 'row'
        tree.insert("", "end", values=row, tags=(tag,))

    conn.close()

Button(search_frame,
       text="Tìm",
       bg="#3B82F6",
       fg="white",
       command=lambda: load_users(search_entry.get())
       ).pack(side=LEFT)

load_users()

# ACTION
action = Frame(tab2, bg=BG_MAIN)
action.pack(pady=10)

def delete_user():
    selected = tree.selection()
    if not selected:
        return

    user_id = tree.item(selected[0])['values'][0]

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    load_users()

Button(action, text="❌ Xóa",
       bg="red", fg="white",
       width=12,
       command=delete_user).pack(side=LEFT, padx=10)

# ================= REPORT =================
tab3 = Frame(notebook, bg=BG_MAIN)
notebook.add(tab3, text="Reports")

def get_report_data():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT users.name, users.email, history.source_text,
           history.translated_text, history.created_at
    FROM history
    JOIN users ON history.user_id = users.id
    ORDER BY history.created_at DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def export_csv():
    data = get_report_data()
    file = filedialog.asksaveasfilename(defaultextension=".csv")
    if not file: return

    with open(file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Email", "Text", "Translated", "Time"])
        writer.writerows(data)

    messagebox.showinfo("OK", "CSV thành công!")

def export_excel():
    data = get_report_data()
    file = filedialog.asksaveasfilename(defaultextension=".xlsx")
    if not file: return

    wb = Workbook()
    ws = wb.active
    ws.append(["User", "Email", "Text", "Translated", "Time"])

    for r in data:
        ws.append(r)

    wb.save(file)
    messagebox.showinfo("OK", "Excel thành công!")

def export_pdf():
    data = get_report_data()
    file = filedialog.asksaveasfilename(defaultextension=".pdf")
    if not file: return

    doc = SimpleDocTemplate(file)
    table_data = [["User", "Email", "Text", "Translated", "Time"]]

    for r in data:
        table_data.append(list(map(str, r)))

    doc.build([Table(table_data)])
    messagebox.showinfo("OK", "PDF thành công!")

Label(tab3, text="📊 Xuất báo cáo",
      font=("Segoe UI", 16, "bold"),
      bg=BG_MAIN).pack(pady=30)

Button(tab3, text="📄 CSV", width=20, height=2,
       command=export_csv).pack(pady=10)

Button(tab3, text="📊 Excel", width=20, height=2,
       command=export_excel).pack(pady=10)

Button(tab3, text="🧾 PDF", width=20, height=2,
       command=export_pdf).pack(pady=10)

root.mainloop()