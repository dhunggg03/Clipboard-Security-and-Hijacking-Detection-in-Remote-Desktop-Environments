import time
import pyperclip
from regex_patterns import analyze_text

class ClipboardListener:
    def __init__(self, log_callback=None, on_alert=None):
        self.log_callback = log_callback
        self.on_alert = on_alert
        self.running = True

    def start(self):
        last_text = pyperclip.paste()
        if self.log_callback:
            self.log_callback("[INFO] Monitoring Clipboard events in real-time...")
        
        while self.running:
            try:
                current_text = pyperclip.paste()
                if current_text != last_text:
                    data_type = analyze_text(current_text)
                    if data_type:
                        if self.on_alert:
                            self.on_alert(data_type, last_text, current_text)
                    else:
                        if self.log_callback:
                            self.log_callback(f"[INFO] Clipboard updated.")
                    last_text = current_text
            except Exception as e:
                print(f"[DEBUG ERROR] {e}")
            time.sleep(0.5)

    def stop(self):
        self.running = False