SUSPICIOUS_PHRASES =[
    "ignore previous",
    "ignore all previous",
    "ignore the above",
    "disregard previous",
    "system prompt",
    "you are now",
    "reveal your instructions",
    "act as",
    "jailbreak",
]

def is_suspicious(text:str)->bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in SUSPICIOUS_PHRASES)
