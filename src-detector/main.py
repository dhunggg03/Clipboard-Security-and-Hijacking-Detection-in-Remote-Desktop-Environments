import threading
import customtkinter as ctk
from clipboard_listener import ClipboardListener

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RDP Clipboard Security Detector")
        self.geometry("550x320")

        self.label = ctk.CTkLabel(self, text="🛡️ Clipboard Guard is Active", font=("Arial", 18, "bold"))
        self.label.pack(pady=15)

        self.textbox = ctk.CTkTextbox(self, width=500, height=220)
        self.textbox.pack(pady=5)
        self.textbox.insert("end", "[INFO] Monitoring Clipboard events in real-time...\n")

        self.listener = ClipboardListener(self.on_hijack_alert)
        threading.Thread(target=self.listener.start, daemon=True).start()

    def on_hijack_alert(self, data_type, original_text, malicious_text):
        message = (
            f"\n[🚨 ALERT] CLIPBOARD HIJACK BLOCKED!\n"
            f"- Data Type: {data_type}\n"
            f"- Restored Original: {original_text}\n"
            f"- Blocked Malicious: {malicious_text}\n"
        )
        self.textbox.insert("end", message)
        self.textbox.see("end")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    app = App()
    app.mainloop()