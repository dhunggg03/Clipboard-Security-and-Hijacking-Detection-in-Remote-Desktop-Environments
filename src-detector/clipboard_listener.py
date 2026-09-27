import win32clipboard
import win32gui
from integrity_checker import IntegrityChecker

class ClipboardListener:
    def __init__(self, callback_alert):
        self.checker = IntegrityChecker()
        self.callback_alert = callback_alert
        self.hwnd = None

    def create_listener_window(self):
        def wnd_proc(hwnd, msg, wparam, lparam):
            if msg == 0x031D:  # WM_CLIPBOARDUPDATE
                self.on_clipboard_change()
                return 0
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = wnd_proc
        wc.lpszClassName = "ClipboardListenerClass"
        hinst = win32gui.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        
        self.hwnd = win32gui.CreateWindow(
            class_atom, "ClipboardListenerWindow", 0, 0, 0, 0, 0, 0, 0, hinst, None
        )
        win32gui.AddClipboardFormatListener(self.hwnd)

    def on_clipboard_change(self):
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                
                status, data_type, orig_text = self.checker.process_new_clipboard(data)
                if status == "HIJACK_DETECTED":
                    self.restore_clipboard(orig_text)
                    self.callback_alert(data_type, orig_text, data)
            else:
                win32clipboard.CloseClipboard()
        except Exception:
            pass

    def restore_clipboard(self, clean_text: str):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(clean_text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        except Exception:
            pass

    def start(self):
        self.create_listener_window()
        win32gui.PumpMessages()