import hashlib
import difflib

def normalize(text):
    # Remove extra whitespace
    return ' '.join(text.lower().split())

def artifact_hash(text):
    return hashlib.sha256(normalize(text).encode()).hexdigest()

def is_duplicate(text1, text2, threshold=0.9):

    return difflib.SequenceMatcher(None, normalize(text1), normalize(text2)).ratio() > threshold

def deduplicate_artifacts(emails):
    seen_hashes = set()
    unique = []
    for email in emails:
        h = artifact_hash(email['body'])
        if h not in seen_hashes:
            seen_hashes.add(h)
            unique.append(email)
        else:
            # duplicate check
            pass
    return unique