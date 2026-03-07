from email.mime import message
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
window.configure( bg=BG_COLOR,highlightbackground=BORDER_COLOR,highlightthickness=3)

chat_area = scrolledtext.ScrolledText(window,bg=CHAT_COLOR,
                                      fg=TEXT_COLOR,font=("Arial", 12),
                                      highlightbackground=BORDER_COLOR,highlightthickness=2,
                                      padx=10,pady=10)
chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
chat_area.config(state='disabled')


bottom_frame = tk.Frame(window, bg=BG_COLOR,highlightbackground=BORDER_COLOR,highlightthickness=2)
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
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                chat_area.config(state='normal')
                chat_area.insert(tk.END, message + "\n")
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