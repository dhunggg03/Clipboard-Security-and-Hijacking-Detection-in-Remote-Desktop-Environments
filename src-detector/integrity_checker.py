import hashlib
from regex_patterns import analyze_text

class IntegrityChecker:
    def __init__(self):
        self.last_clean_hash = None
        self.last_clean_text = ""
        self.last_data_type = "Normal"

    def calculate_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def process_new_clipboard(self, new_text: str):
        new_hash = self.calculate_hash(new_text)
        new_data_type = analyze_text(new_text)

        if new_hash == self.last_clean_hash:
            return "UNCHANGED", self.last_data_type, new_text

        if self.last_data_type != "Normal" and new_hash != self.last_clean_hash:
            return "HIJACK_DETECTED", self.last_data_type, self.last_clean_text

        self.last_clean_hash = new_hash
        self.last_clean_text = new_text
        self.last_data_type = new_data_type
        return "NEW_COPY", new_data_type, new_text