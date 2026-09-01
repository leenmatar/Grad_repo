def detect_priority(description):
    text = description.lower()
    score = 0

    # Critical urgency indicators
    if "system down" in text:
        score += 3

    if "server down" in text:
        score += 3

    # High urgency indicators
    if "urgent" in text:
        score += 2

    if "exam" in text:
        score += 2

    if "deadline" in text:
        score += 2

    # Access problems
    if "cannot access" in text:
        score += 1

    if "cannot login" in text:
        score += 1

    if "cannot log in" in text:
        score += 1

    # Other technical problems
    if "not working" in text:
        score += 1

    if "locked" in text:
        score += 1

    # Final priority
    if score >= 5:
        return "Critical"

    if score >= 3:
        return "High"

    if score >= 1:
        return "Medium"

    return "Low"
