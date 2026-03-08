import json
from openai import OpenAI
from schema import Entity, Claim, Evidence
import time

client = OpenAI()

PROMPT = """
You are an expert at extracting structured knowledge from email communications.

From the following email, extract:

1. Entities: People, organizations, projects, locations, etc. Each entity should have:
   - id: unique identifier (e.g., email address for people)
   - type: person, organization, project, etc.
   - name: display name
   - aliases: list of alternative names

2. Claims: Factual statements or relationships. Each claim should have:
   - subject: entity id
   - relation: type of relationship (e.g., works_for, sent_email_to, discusses)
   - object: entity id or value
   - confidence: 0-1 score
   - evidence: excerpt from email, source_id, start/end offsets, timestamp

Output only valid JSON with keys "entities" and "claims". No extra text.

Email:
{email_text}
"""

def extract_structured(email_data, max_retries=3):
    email_text = f"Subject: {email_data['subject']}\nFrom: {email_data['from']}\nTo: {email_data['to']}\nDate: {email_data['date']}\nBody: {email_data['body']}"

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": PROMPT.format(email_text=email_text)},
                    {"role": "user", "content": "Extract entities and claims."}
                ],
                temperature=0.1
            )

            data = json.loads(response.choices[0].message.content.strip())

            # Validate
            entities = [Entity(**e) for e in data.get('entities', [])]
            claims = []
            for c in data.get('claims', []):
                #evidence details
                ev_list = []
                for ev in c.get('evidence', []):
                    ev['source_id'] = email_data['id']
                    ev['timestamp'] = email_data['date']
                    ev_list.append(Evidence(**ev))
                c['evidence'] = ev_list
                claims.append(Claim(**c))

            return entities, claims

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(1)

    return [], []