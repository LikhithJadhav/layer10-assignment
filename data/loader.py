import os
import email
import pandas as pd
from email import policy
from email.parser import BytesParser

def load_enron_emails(data_dir="data/enron/maildir"):
    emails = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.'):
                continue  # skip some files
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'rb') as f:
                    msg = BytesParser(policy=policy.default).parse(f)
                    emails.append({
                        'id': filepath,
                        'subject': msg['subject'] or '',
                        'from': msg['from'] or '',
                        'to': msg['to'] or '',
                        'date': msg['date'] or '',
                        'body': msg.get_body(preferencelist=('plain',)).get_content() if msg.get_body() else ''
                    })
            except Exception as e:
                print(f"Error parsing {filepath}: {e}")
    return pd.DataFrame(emails)

if __name__ == "__main__":
    df = load_enron_emails()
    df.to_csv("data/enron_emails.csv", index=False)
    print(f"Loaded {len(df)} emails.")