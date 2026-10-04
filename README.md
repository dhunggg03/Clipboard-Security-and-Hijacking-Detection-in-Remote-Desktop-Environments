# Remote Clipboard Security & Hijacking Detector

An in-memory monitoring and security tool designed to detect and prevent
clipboard sniffing and hijacking attacks in Remote Desktop Protocol (RDP) and
virtualized environments.

**Scope:** Windows only. The PoC attacker uses `win32clipboard`
(`pywin32`), and local-copy attribution uses a global keyboard hook
(`pynput`). Linux/macOS support is not implemented — see Future Work.

## 📌 Problem Context

While Clipboard Redirection in RDP/VirtualBox enables convenient
cross-machine data sharing, it introduces a major security risk. Attackers
or malicious background processes on a remote machine can leverage system
APIs to silently sniff sensitive data (crypto wallet addresses, resident
numbers, card details) or hijack copied contents in real-time. Standard
antivirus solutions often miss these fileless/in-memory techniques because
they rely on legitimate OS functionality.

This isn't a hypothetical risk — a documented flaw (CVE-2016-3066) in
spice-gtk caused RDP/VM clients to auto-sync the local clipboard to the
remote guest instantly, even without window focus, and academic research has
shown clipboard hijacking executed remotely over RDP/virtualization sessions
with no malware installed on the victim's machine at all.

## 🛠️ Key Features

- **Real-Time Clipboard Listener** — polls clipboard content via `pyperclip`
  and classifies every change.
- **Sensitive Data Pattern Matching (Regex)** — identifies BTC/ETH wallet
  addresses, credit card numbers, and Korean Resident Registration Numbers
  (RRN).
- **SHA-256 Integrity Tracking** — hashes each accepted clipboard value to
  detect whether the current content matches the last known-clean copy.
- **Local-Copy Attribution** — a background key listener (`pynput`) tracks
  real Ctrl+C events. A clipboard change is only flagged as a hijack when
  the previous value was sensitive **and** the change was not preceded by a
  local Ctrl+C within a 1-second window — this is what tells a legitimate
  new copy apart from an unexplained (e.g. remote/background) swap.
- **Automatic Restoration** — on a detected hijack, the clean value is
  written back to the clipboard immediately via `pyperclip.copy()`, not just
  logged.

## 📂 Repository Structure

```
requirements.txt
src-detector/              Main defense tool, runs on the Host
├── main.py                 CustomTkinter GUI entry point
├── clipboard_listener.py   Polling loop + Ctrl+C attribution tracker
├── regex_patterns.py       Sensitive-data pattern definitions
└── integrity_checker.py    SHA-256 hashing + hijack decision logic
poc-attack/                 Proof of Concept attacker
└── remote_hijack.py         Simulated clipboard-swap attack (Windows win32clipboard)
```

## 🧰 Tech Stack

| Component              | Library          |
|-------------------------|-------------------|
| Clipboard read/write     | `pyperclip`       |
| GUI                      | `customtkinter`   |
| Local copy detection     | `pynput`          |
| PoC attacker clipboard   | `pywin32` (`win32clipboard`) |
| Integrity check          | `hashlib` (SHA-256, stdlib) |

## ⚠️ Responsible Use Notice

`poc-attack/remote_hijack.py` simulates a clipboard-hijacking attacker for
demonstration and testing purposes only. Run it only against your own local
machine or an isolated lab VM you control. Do not run it against any system
you don't own or have explicit permission to test.

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the defense tool (Terminal 1):
   ```bash
   cd src-detector
   python main.py
   ```
3. In an isolated lab VM only, run the simulated attacker (Terminal 2):
   ```bash
   cd poc-attack
   python remote_hijack.py
   ```
4. Copy a BTC address (e.g. `1BoatSLRHtKNngkdXEeobR76b53LETtpyT`), then wait —
   the attacker will swap it, and the detector should alert and restore the
   original within about a second.

## 🧪 Evaluation

- **False positives** — copy normal content (URLs, code, prose) with the
  detector running; confirm no alerts fire.
- **True positives** — run `remote_hijack.py` against the Host while
  `main.py` is active; confirm the swap is detected, alerted, and the
  original value is restored on paste.
- **Detection latency** — time the gap between the simulated swap and the
  alert firing, across several runs, to report a representative number.
- **Attribution accuracy** — confirm that copying a new sensitive value
  yourself (a real Ctrl+C) is *not* flagged as a hijack, only unexplained
  changes are.

## 🔭 Future Work

- Hook the RDP virtual channel directly (e.g. via FreeRDP's `cliprdr`
  channel) for a genuine "this came through the RDP redirection channel"
  signal, instead of inferring it from the absence of a local Ctrl+C.
- Extend detection to cross-device cloud clipboard sync (Cloud Clipboard /
  Universal Clipboard) as a related but separate threat surface.
- Cross-platform support (Linux/macOS clipboard + keyboard hooking).

## License

MIT (suggested — change if your course requires otherwise).
