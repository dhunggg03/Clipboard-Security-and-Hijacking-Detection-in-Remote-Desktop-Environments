import re

PATTERNS = {
    "BTC_Address": re.compile(r"^(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-Z0-9]{38,59})$"),
    "ETH_Address": re.compile(r"^0x[a-fA-F0-9]{40}$"),
    "Credit_Card": re.compile(r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[047][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})$"),
    "KR_RRN": re.compile(r"^\d{6}-[1-4]\d{6}$")
}

def analyze_text(text: str) -> str:
    clean_text = text.strip()
    for name, pattern in PATTERNS.items():
        if pattern.search(clean_text):
            return name
    return None