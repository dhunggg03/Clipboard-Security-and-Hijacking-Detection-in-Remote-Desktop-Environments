import time
import pyperclip
from pynput import keyboard

from regex_patterns import analyze_text
from integrity_checker import IntegrityChecker

COPY_ATTRIBUTION_WINDOW = 1.0  # seconds


class _CopyKeyTracker:
    """Watches for a local Ctrl+C so clipboard changes can be told apart
    from unexplained (possibly remote) changes."""

    def __init__(self):
        self._last_ctrl_c_time = 0.0
        self._ctrl_down = False
        self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()

    def _on_press(self, key):
        try:
            if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
                self._ctrl_down = True
            elif self._ctrl_down and hasattr(key, "char") and key.char == "\x03":
                self._last_ctrl_c_time = time.time()
        except Exception:
            pass

    def _on_release(self, key):
        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            self._ctrl_down = False

    def was_recent_copy(self) -> bool:
        return (time.time() - self._last_ctrl_c_time) <= COPY_ATTRIBUTION_WINDOW


class ClipboardListener:
    def __init__(self, log_callback=None, on_alert=None):
        self.log_callback = log_callback
        self.on_alert = on_alert
        self.running = True
        self.checker = IntegrityChecker()
        self._key_tracker = _CopyKeyTracker()

    def _log(self, message: str):
        if self.log_callback:
            self.log_callback(message)

    def start(self):
        self._key_tracker.start()
        try:
            
            seed_text = pyperclip.paste()
            self.checker.process_new_clipboard(
                seed_text, analyze_text(seed_text), locally_copied=True
            )
            self._log("[INFO] Monitoring clipboard events in real-time...")

            while self.running:
                try:
                    current_text = pyperclip.paste()
                except Exception as e:
                    self._log(f"[DEBUG ERROR] {e}")
                    time.sleep(0.5)
                    continue

                data_type = analyze_text(current_text)
                locally_copied = self._key_tracker.was_recent_copy()

                status, label, kept_text = self.checker.process_new_clipboard(
                    current_text, data_type, locally_copied
                )

                if status == "HIJACK_DETECTED":
                    pyperclip.copy(kept_text)  
                    if self.on_alert:
                        self.on_alert(label, kept_text, current_text)
                elif status == "NEW_COPY":
                    if data_type:
                        self._log(f"[INFO] Sensitive data copied ({data_type}).")
                    else:
                        self._log("[INFO] Clipboard updated.")

                time.sleep(0.5)
        finally:
            self._key_tracker.stop()

    def stop(self):
        self.running = False