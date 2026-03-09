import threading
import socket
import tkinter as tk
import os

BG_COLOR      = "#f6e6ff"
CHAT_COLOR    = "#fff0f5"
ENTRY_COLOR   = "#ccddfa"
BUTTON_COLOR  = "#d5f5e3"
TEXT_COLOR    = "#5524B9"
BORDER_COLOR  = "#ff4da6"
TITLE_BAR     = "#fb81be"
CLOSE_BUTTON  = "#e60073"
LINE_COLOR    = "#ffd6eb"

host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_FILES = [
    os.path.join(SCRIPT_DIR, "images", "gatito.gif"),
    os.path.join(SCRIPT_DIR, "images", "kitty.gif"),
    os.path.join(SCRIPT_DIR, "images", "kuromi.gif"),
    os.path.join(SCRIPT_DIR, "images", "mymelo.gif"),
    os.path.join(SCRIPT_DIR, "images", "osito.gif"),
]
ICON_SIZE = 28

window = tk.Tk()
window.withdraw()        

_chat_icon_refs = [None] * len(ICON_FILES)

def _load_chat_icon(index: int):
    if _chat_icon_refs[index] is not None:
        return _chat_icon_refs[index]
    try:
        raw = tk.PhotoImage(file=ICON_FILES[index], master=window)
        w, h = raw.width(), raw.height()
        sx = max(1, w // ICON_SIZE)
        sy = max(1, h // ICON_SIZE)
        img = raw.subsample(sx, sy)
        _chat_icon_refs[index] = img
        return img
    except Exception:
        return None

for i in range(len(ICON_FILES)):
    _load_chat_icon(i)

class NicknameDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Elige tu apodo e icono")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
        self.grab_set()

        self.result_nick = None
        self.result_icon = 0
        self._selected_icon = tk.IntVar(value=0)

        tk.Label(self, text="Apodo:", bg=BG_COLOR, fg=TEXT_COLOR,
                 font=("Arial", 12, "bold")).pack(pady=(18, 4))
        self._nick_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self._nick_var,
                         font=("Arial", 13), bg=ENTRY_COLOR, fg=TEXT_COLOR,
                         highlightbackground=BORDER_COLOR, highlightthickness=2,
                         width=22)
        entry.pack(padx=24)
        entry.focus()

        tk.Label(self, text="Elige un icono:", bg=BG_COLOR, fg=TEXT_COLOR,
                 font=("Arial", 12, "bold")).pack(pady=(14, 6))

        icon_row = tk.Frame(self, bg=BG_COLOR)
        icon_row.pack(padx=24, pady=(0, 6))

        # Load picker-sized copies (48 px) – still under the same master
        self._picker_imgs = []
        for i, path in enumerate(ICON_FILES):
            try:
                raw = tk.PhotoImage(file=path, master=window)
                w, h = raw.width(), raw.height()
                sx = max(1, w // 48)
                sy = max(1, h // 48)
                img = raw.subsample(sx, sy)
            except Exception:
                img = None
            self._picker_imgs.append(img)

            btn = tk.Radiobutton(
                icon_row,
                image=img,
                text=f"#{i+1}" if img is None else "",
                variable=self._selected_icon,
                value=i,
                bg=BG_COLOR,
                activebackground=LINE_COLOR,
                selectcolor=LINE_COLOR,
                indicatoron=False,
                relief="solid",
                bd=2,
                cursor="hand2",
                width=54, height=54,
            )
            btn.grid(row=0, column=i, padx=5)

        ok_btn = tk.Button(self, text="Entrar al chat ❤",
                           command=self._on_ok,
                           bg=BUTTON_COLOR, fg=TEXT_COLOR,
                           font=("Arial", 12, "bold"),
                           highlightbackground=BORDER_COLOR,
                           highlightthickness=2,
                           cursor="hand2")
        ok_btn.pack(pady=(8, 18), ipadx=8)

        self.bind("<Return>", lambda _: self._on_ok())
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        self.update_idletasks()
        dw = self.winfo_width(); dh = self.winfo_height()
        x = (self.winfo_screenwidth()  - dw) // 2
        y = (self.winfo_screenheight() - dh) // 2
        self.geometry(f"+{x}+{y}")

    def _on_ok(self):
        nick = self._nick_var.get().strip()
        if not nick:
            return
        self.result_nick = nick
        self.result_icon = self._selected_icon.get()
        self.destroy()

    def _on_cancel(self):
        self.destroy()


dlg = NicknameDialog(window)
window.wait_window(dlg)

nickname = dlg.result_nick or "Anonimo"
my_icon  = dlg.result_icon

window.title("Chat")
window.geometry("520x650")
window.x = 0
window.y = 0
window.configure(bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=3)
window.overrideredirect(True)
window.deiconify()

border_frame = tk.Frame(window, bg="#ff1493", padx=3, pady=3)
border_frame.pack(fill="both", expand=True)

main_frame = tk.Frame(border_frame, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)

title_bar = tk.Frame(main_frame, bg=TITLE_BAR, height=30)
title_bar.pack(fill=tk.X)
title_bar.pack_propagate(False)

tk.Label(title_bar, text="❤", bg=TITLE_BAR, fg="#a521f7", font=("Arial", 12)).pack(side=tk.LEFT, padx=(8, 2))
tk.Label(title_bar, text="❤", bg=TITLE_BAR, fg="#ff0080", font=("Arial", 12)).pack(side=tk.LEFT, padx=2)
tk.Label(title_bar, text="❤", bg=TITLE_BAR, fg="#ffffff", font=("Arial", 12)).pack(side=tk.LEFT, padx=2)
tk.Label(title_bar, text=" Chat", bg=TITLE_BAR, fg="white",
         font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=6)

def on_close():
    try:
        client.shutdown(socket.SHUT_RDWR)
        client.close()
    except Exception:
        pass
    window.destroy()

close_button = tk.Button(title_bar, text="✕", bg=CLOSE_BUTTON,
                         fg="white", bd=0, font=("Arial", 12, "bold"),
                         command=on_close, activebackground="#cc0066")
close_button.bind("<Enter>", lambda e: close_button.config(bg="#cc0066"))
close_button.bind("<Leave>", lambda e: close_button.config(bg=CLOSE_BUTTON))
close_button.pack(side=tk.RIGHT, padx=8, pady=3)

def start_move(event):
    window.x = event.x
    window.y = event.y

def move_window(event):
    x = event.x_root - window.x
    y = event.y_root - window.y
    window.geometry(f"+{x}+{y}")

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", move_window)
window.protocol("WM_DELETE_WINDOW", on_close)

chat_area = tk.Text(main_frame, bg=CHAT_COLOR, fg=TEXT_COLOR,
                    font=("Arial", 12),
                    highlightbackground=BORDER_COLOR, highlightthickness=2,
                    padx=10, pady=10, wrap="word")
chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
chat_area.config(state='disabled')
chat_area.tag_config("line", background=LINE_COLOR)

scrollbar = tk.Scrollbar(chat_area, command=chat_area.yview)
chat_area.configure(yscrollcommand=scrollbar.set)

bottom_frame = tk.Frame(main_frame, bg=BG_COLOR,
                        highlightbackground=BORDER_COLOR, highlightthickness=2)
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

msg_entry = tk.Entry(bottom_frame, font=("Arial", 14), bg=ENTRY_COLOR,
                     fg=TEXT_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=2)
msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
msg_entry.focus()

line_count = 0

def _insert_message(raw_message: str):
    global line_count
    icon_index = None
    text = raw_message

    if raw_message.startswith("[ICON:"):
        end = raw_message.find("]")
        if end != -1:
            try:
                icon_index = int(raw_message[6:end])
            except ValueError:
                pass
            text = raw_message[end + 1:]

    tag = "line" if line_count % 2 == 0 else ""
    chat_area.config(state='normal')

    if icon_index is not None:
        img = _load_chat_icon(icon_index)
        if img:
            chat_area.image_create(tk.END, image=img, padx=2, pady=2)
        chat_area.insert(tk.END, " " + text + "\n", tag)
    else:
        chat_area.insert(tk.END, text + "\n", tag)

    line_count += 1
    chat_area.see(tk.END)
    chat_area.config(state='disabled')


def write():
    message_text = msg_entry.get()
    if message_text.strip():
        message = f"[ICON:{my_icon}]{nickname}: {message_text}"
        client.send(message.encode('utf-8'))
    msg_entry.delete(0, tk.END)

msg_entry.bind("<Return>", lambda event: write())


def receive():
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message == 'NICK':
                client.send(f"{nickname}|{my_icon}".encode('utf-8'))
            else:
                window.after(0, _insert_message, message)
        except Exception:
            print("Ocurrio un error / conexion cerrada")
            try:
                window.after(0, window.destroy)
            except Exception:
                pass
            break


receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

send_button = tk.Button(bottom_frame, text="Enviar", command=write,
                        bg=BUTTON_COLOR, fg=TEXT_COLOR,
                        highlightbackground=BORDER_COLOR, highlightthickness=2,
                        font=("Arial", 12, "bold"))
send_button.pack(side=tk.RIGHT)

window.mainloop()