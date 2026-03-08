from collections import defaultdict
from schema import Claim

def deduplicate_claims(claims: List[Claim]) -> List[dict]:
    table = defaultdict(list)
    for c in claims:
        key = (c.subject, c.relation, c.object)
        table[key].append(c)

    merged = []
    for k, clist in table.items():
        # Merge evidence
        all_evidence = []
        total_conf = 0
        for c in clist:
            all_evidence.extend(c.evidence)  # evidence is list
            total_conf += c.confidence
        avg_conf = total_conf / len(clist)
        merged.append({
            "subject": k[0],
            "relation": k[1],
            "object": k[2],
            "confidence": avg_conf,
            "evidence": all_evidence
        })
    return merged