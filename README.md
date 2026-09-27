# Remote Clipboard Security & Hijacking Detector

An in-memory monitoring and security tool designed to detect and prevent
clipboard sniffing and hijacking attacks in Remote Desktop Protocol (RDP) and
virtualized environments.

**Scope:** This detector targets Windows RDP clients
(`AddClipboardFormatListener` is a Win32-specific API). Linux/macOS clipboard
hooking would require a separate implementation and isn't covered here.

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

- **Real-Time Clipboard Listener** — monitors OS clipboard format events
  using Win32 APIs (`AddClipboardFormatListener`) without high CPU overhead.
- **Sensitive Data Pattern Matching (Regex)** — identifies sensitive formats
  such as crypto wallets (BTC, ETH), credit card numbers, and Resident
  Registration Numbers (RRN/ARC).
- **Integrity & Anomaly-Aware Hijack Detection** — computes SHA-256 hash
  signatures on copy events and flags changes that occur **without a
  corresponding local user copy action** (see note below), rather than
  claiming to identify the remote channel directly.
- **Instant Mitigation & Alerting** — displays real-time alerts and restores
  the clean clipboard state upon detecting suspicious swap behavior.

> **Design note on "remote" detection:** a generic clipboard-change event
> alone doesn't tell you *which side* of an RDP session changed the
> clipboard. This tool detects **unattributed changes** — clipboard content
> changing without a preceding local copy action (e.g. no Ctrl+C / explicit
> copy from a focused local window) — which is a reliable, honest signal for
> anomalous behavior regardless of whether the actual source is remote
> malware, a background process, or the RDP redirection channel itself. See
> **Future Work** for a more precise, channel-level approach.

## 📂 Repository Structure

```
requirements.txt        Python dependencies
src-detector/           Main defense tool running on Host
├── main.py             System tray & GUI entry point
├── clipboard_listener.py   Win32 API listener
├── regex_patterns.py       Pattern definitions for sensitive data
└── integrity_checker.py    Hash comparison & anomaly detection logic
poc-attack/             Proof of Concept scripts
└── remote_hijack.py    Simulated attacker script
```

## ⚠️ Responsible Use Notice

`poc-attack/remote_hijack.py` simulates a clipboard-hijacking attacker for
demonstration and testing purposes only. Run it only against your own local
machine or an isolated lab VM you control. Do not run it against any system
you don't own or have explicit permission to test.

## 🚀 Quick Start

1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the defense tool on the Host:
   ```bash
   python src-detector/main.py
   ```
3. (Optional, in an isolated lab VM only) Run the simulated attack to see
   detection in action:
   ```bash
   python poc-attack/remote_hijack.py
   ```

## 🧪 Evaluation

- **False positives** — copy normal content (URLs, code, prose) with the
  detector running; confirm no alerts fire.
- **True positives** — run `poc-attack/remote_hijack.py` against the Host
  while `main.py` is active; confirm the swap is detected and the
  alert/restore fires.
- **Detection latency** — measure the time between the simulated swap and
  the alert firing, to show the listener is event-driven and near-instant
  rather than eventually-consistent.

## 🔭 Future Work

- Hook the RDP virtual channel directly (e.g. via FreeRDP's client APIs for
  the `cliprdr` channel) to get a genuine signal for "this change came
  through the RDP redirection channel" rather than inferring it from the
  absence of a local copy action.
- Extend detection to cross-device cloud clipboard sync (Cloud Clipboard /
  Universal Clipboard) as a related but separate threat surface.
- Cross-platform support (Linux/macOS clipboard hooking).

## License

MIT 
