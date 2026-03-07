
import threading
import socket
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog

BG_COLOR = "#f6e6ff"
CHAT_COLOR = "#fff0f5"
ENTRY_COLOR = "#ccddfa"
BUTTON_COLOR = "#d5f5e3"
BUTTON_ACTIVE = "#b8f2d6"
TEXT_COLOR = "#5524B9"
BORDER_COLOR = "#ff4da6"
TITLE_BAR = "#fb81be"     
CLOSE_BUTTON = "#e60073"
LINE_COLOR = "#ffd6eb"

host = '127.0.0.1'
port = 55555


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

root = tk.Tk()
root.withdraw()

nickname = simpledialog.askstring("Nickname", "Escoge un apodo:", parent=root)

window = tk.Tk()
window.title("Chat")
window.geometry("520x650")
window.x = 0
window.y = 0
window.configure( bg=BG_COLOR,highlightbackground=BORDER_COLOR,highlightthickness=3)
window.overrideredirect(True)

border_frame = tk.Frame(window, bg="#ff1493", padx=3, pady=3)
border_frame.pack(fill="both", expand=True)

main_frame = tk.Frame(border_frame, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)

title_bar = tk.Frame(main_frame, bg=TITLE_BAR, height=30)
title_bar.pack(fill=tk.X)
title_bar.pack_propagate(False)
heart1 = tk.Label(title_bar, text="❤", bg=TITLE_BAR, fg="#a521f7", font=("Arial", 12))
heart1.pack(side=tk.LEFT, padx=(8,2))

heart2 = tk.Label(title_bar, text="❤", bg=TITLE_BAR, fg="#ff0080", font=("Arial", 12))
heart2.pack(side=tk.LEFT, padx=2)

heart3 = tk.Label(title_bar, text="❤", bg=TITLE_BAR, fg="#ffffff", font=("Arial", 12))
heart3.pack(side=tk.LEFT, padx=2)

title_label = tk.Label(title_bar,text=" Chat",
                       bg=TITLE_BAR,fg="white",
                       font=("Arial", 11, "bold"))

title_label.pack(side=tk.LEFT, padx=6)

close_button = tk.Button(title_bar,text="✕",bg=CLOSE_BUTTON,
                         fg="white",bd=0,font=("Arial", 12, "bold"),
                         command=window.destroy,activebackground="#cc0066")
close_button.bind("<Enter>", lambda e: close_button.config(bg="#cc0066"))
close_button.bind("<Leave>", lambda e: close_button.config(bg=CLOSE_BUTTON))

def start_move(event):
    window.x = event.x
    window.y = event.y

def move_window(event):
    x = event.x_root - window.x
    y = event.y_root - window.y
    window.geometry(f"+{x}+{y}")

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", move_window)


close_button.pack(side=tk.RIGHT, padx=8, pady=3)
chat_area = scrolledtext.ScrolledText(main_frame,bg=CHAT_COLOR,
                                      fg=TEXT_COLOR,font=("Arial", 12),
                                      highlightbackground=BORDER_COLOR,highlightthickness=2,
                                      padx=10,pady=10)
chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
chat_area.config(state='disabled')
chat_area.tag_config("line", background=LINE_COLOR)

bottom_frame = tk.Frame(main_frame,bg=BG_COLOR,highlightbackground=BORDER_COLOR,highlightthickness=2)
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

msg_entry = tk.Entry(bottom_frame,font=("Arial", 14),bg=ENTRY_COLOR,fg=TEXT_COLOR,
                     highlightbackground=BORDER_COLOR,highlightthickness=2)
msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
msg_entry.bind("<Return>", lambda event: write())
msg_entry.focus()

def write():  
    message_text = msg_entry.get()

    if message_text.strip() != "":
        message = f"{nickname}: {message_text}"
        client.send(message.encode('utf-8'))

    msg_entry.delete(0, tk.END)
line_count = 0

def receive():
    global line_count

    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == 'NICK':
                client.send(nickname.encode('utf-8'))

            else:
                chat_area.config(state='normal')

                if line_count % 2 == 0:
                    chat_area.insert(tk.END, message + "\n", "line")
                else:
                    chat_area.insert(tk.END, message + "\n")

                line_count += 1

                chat_area.see(tk.END)
                chat_area.config(state='disabled')

        except:
            print("Ocurrio un error")
            client.close()
            break

receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

send_button = tk.Button(bottom_frame,text="Enviar",command=write,
                        bg=BUTTON_COLOR,fg=TEXT_COLOR,highlightbackground=BORDER_COLOR,
                        highlightthickness=2,font=("Arial", 12, "bold")
)
send_button.pack(side=tk.RIGHT)


window.mainloop()