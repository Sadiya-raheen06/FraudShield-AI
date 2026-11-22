import re
from urllib.parse import urlparse


# TRANSACTION FRAUD DETECTION
def analyse_transaction(amount, is_new_receiver=False,
                        unusual_activity=False):

    risk_score = 0
    reasons = []

    if amount >= 50000:
        risk_score += 35
        reasons.append("High transaction amount")

    if amount >= 20000:
        risk_score += 15
        reasons.append("Large payment")

    if is_new_receiver:
        risk_score += 25
        reasons.append("New or unverified receiver")

    if unusual_activity:
        risk_score += 30
        reasons.append("Unusual transaction activity")

    if risk_score >= 60:
        level = "HIGH RISK"
    elif risk_score >= 30:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return {
        "risk_score": min(risk_score, 100),
        "risk_level": level,
        "reasons": reasons
    }


# SMS FRAUD DETECTION
def scan_message(message):

    keywords = [
        "urgent", "otp", "verify your account",
        "click here", "blocked account",
        "update kyc", "claim your reward",
        "prize winner", "send password",
        "share otp", "account suspended"
    ]

    message_lower = message.lower()

    detected = [
        word for word in keywords
        if word in message_lower
    ]

    links = re.findall(
        r'https?://[^\s]+',
        message
    )

    risk_score = min(
        len(detected) * 20 + len(links) * 15,
        100
    )

    if risk_score >= 60:
        level = "HIGH RISK"
    elif risk_score >= 20:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "keywords": detected,
        "links": links
    }


# SUSPICIOUS WEBSITE DETECTION
def scan_website(url):

    suspicious_words = [
        "login", "verify", "banking",
        "freegift", "reward", "claim",
        "secure", "kyc"
    ]

    result = urlparse(url if "://" in url
                      else "https://" + url)

    domain = result.netloc.lower()

    score = 0
    reasons = []

    if result.scheme != "https":
        score += 25
        reasons.append("Website does not use HTTPS")

    if "@" in url:
        score += 40
        reasons.append("Suspicious URL structure")

    if len(domain) > 40:
        score += 15
        reasons.append("Unusually long domain")

    if any(word in domain for word in suspicious_words):
        score += 20
        reasons.append("Suspicious words in domain")

    if re.search(r'\d{5,}', domain):
        score += 20
        reasons.append("Unusual numbers in domain")

    if score >= 50:
        level = "HIGH RISK"
    elif score >= 20:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return {
        "risk_score": min(score, 100),
        "risk_level": level,
        "reasons": reasons
    }
