# Clipboard-Security-and-Hijacking-Detection-in-Remote-Desktop-Environments
A real-time in-memory monitoring tool to detect and prevent clipboard sniffing and hijacking attacks in RDP and virtualized environments


# Clipboard Security and Hijacking Detection in Remote Desktop Environments

An open-source clipboard broker that detects remote clipboard hijacking and
gates data leakage in RDP / VM clipboard-sharing sessions.

## Background

RDP and VM clipboard redirection share one clipboard per session and sync it
automatically and continuously — whatever you copy locally is transferred to
the remote host right away, filtered only by a blacklist of formats rather
than an explicit allowlist. That means clipboard content can be read or
overwritten by the other end of the session without the user ever pressing
paste.

## Related work

- **CVE-2016-3066** — spice-gtk (virt-viewer, virt-manager, GNOME Boxes)
  auto-synced the local clipboard to the remote guest instantly, even without
  window focus.
- Academic research has demonstrated clipboard hijacking executed remotely
  over RDP/virtualization sessions with no malware installed on the victim's
  machine.
- **Qubes OS** takes the opposite design stance: copying between VMs requires
  an explicit key combo, and the clipboard clears itself right after — this
  project's confirmation gate is inspired by that model.

## Threat model

- **Attacker:** a malicious or compromised remote host/guest on the other end
  of an RDP/VM session.
- **Capability:** read or overwrite the shared clipboard without the victim
  ever pasting.
- **Out of scope:** cross-device cloud clipboard sync (Cloud Clipboard /
  Universal Clipboard) and app-level clipboard snooping — left for future
  work.

## System architecture

| Component        | Role                                                                 |
|-------------------|-----------------------------------------------------------------------|
| Classifier        | Flags sensitive content — secrets, keys, high-entropy strings, wallet/account-shaped values |
| Sync gate         | Blocks silent auto-sync of flagged content across the RDP boundary; requires explicit confirmation |
| Hijack detector   | Flags a sensitive value being replaced by a different one within a short window, unprompted |
| Audit log         | Records what was flagged, blocked, or allowed, and when              |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# interactive: prompts before syncing anything flagged
python clipboard_broker.py

# unattended demo: simulates a hijack and a leak so you can see both
# detections fire without any manual input
python clipboard_broker.py --simulate
```

Detections and gate decisions are written to `clipboard_audit.log`.

## Evaluation

- **False positives** — run normal clipboard traffic (code, URLs, prose)
  through the classifier and confirm it stays quiet.
- **True positives** — the `--simulate` flag triggers a scripted address swap
  (hijack) and a scripted secret copy (leak); confirm both are caught.
- **Usability** — track how often the confirmation prompt interrupts normal,
  safe copy/paste.

## Implementation notes

This MVP watches the local clipboard and simulates the RDP sync boundary with
an in-terminal confirmation prompt, rather than hooking into a real RDP
client's clipboard channel. That's a reasonable, clearly-scoped limitation
for a course project — see Future Work.

## Future work

- Hook directly into a real RDP client's clipboard channel (e.g. FreeRDP)
  instead of simulating the sync boundary.
- Extend the same classifier/gate model to cross-device cloud clipboard sync.
- Publish the classifier as a standalone, reusable module.

## License

MIT (suggested — change if your course requires otherwise).
