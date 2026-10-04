import threading
import customtkinter as ctk
from clipboard_listener import ClipboardListener


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RDP Clipboard Security Detector")
        self.geometry("550x320")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.label = ctk.CTkLabel(
            self, text="🛡️ Clipboard Guard is Active", font=("Arial", 18, "bold")
        )
        self.label.pack(pady=15)

        self.textbox = ctk.CTkTextbox(self, width=500, height=220)
        self.textbox.pack(pady=5)
        self.textbox.insert("end", "[INFO] Starting clipboard guard...\n")

        self.listener = ClipboardListener(log_callback=self._on_log, on_alert=self._on_hijack_alert)
        self._thread = threading.Thread(target=self.listener.start, daemon=True)
        self._thread.start()

    def _on_log(self, message: str):
        self.after(0, self._append, message)

    def _on_hijack_alert(self, data_type, original_text, malicious_text):
        message = (
            f"\n[🚨 ALERT] CLIPBOARD HIJACK BLOCKED!\n"
            f"- Data Type: {data_type}\n"
            f"- Restored Original: {original_text}\n"
            f"- Blocked Malicious: {malicious_text}\n"
        )
        self.after(0, self._append, message)

    def _append(self, message: str):
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")

    def on_close(self):
        self.listener.stop()
        self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    app = App()
    app.mainloop()