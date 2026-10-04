import hashlib

NORMAL = "Normal"


class IntegrityChecker:
    """
    Tracks the last known-clean clipboard value and decides whether a new
    clipboard value is a legitimate new copy or a hijack.

    A hijack is flagged when the *previous* clean value was sensitive and
    the clipboard changed WITHOUT being preceded by a local copy action
    (see clipboard_listener.py's key tracker) -- that's the signature of a
    remote/background swap rather than the user copying something new.
    """

    def __init__(self):
        self.last_clean_hash = None
        self.last_clean_text = ""
        self.last_data_type = NORMAL

    def calculate_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def process_new_clipboard(self, new_text: str, data_type: str, locally_copied: bool):
        """
        data_type:      result of analyze_text(new_text) -- a label string,
                         or None for non-sensitive content.
        locally_copied: True if this change was immediately preceded by a
                         local Ctrl+C.

        Returns (status, label, text_to_keep):
          "UNCHANGED"       -- identical to what's already on record
          "NEW_COPY"        -- a normal, attributed change -- accept it
          "HIJACK_DETECTED" -- previous clean copy was sensitive, content
                               changed, and no local copy action explains it
        """
        new_hash = self.calculate_hash(new_text)

        if new_hash == self.last_clean_hash:
            return "UNCHANGED", self.last_data_type, self.last_clean_text

        was_sensitive = self.last_data_type != NORMAL
        if was_sensitive and not locally_copied:
            
            return "HIJACK_DETECTED", self.last_data_type, self.last_clean_text

        label = data_type if data_type else NORMAL
        self.last_clean_hash = new_hash
        self.last_clean_text = new_text
        self.last_data_type = label
        return "NEW_COPY", label, new_text