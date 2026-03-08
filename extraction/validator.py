from schema import Entity, Claim, Evidence
from typing import List

def validate_entities(entity_list: List[dict]) -> List[Entity]:
    valid = []
    for e in entity_list:
        try:
            entity = Entity(**e)
            if entity.id and entity.name:
                valid.append(entity)
        except Exception as ex:
            print(f"Invalid entity: {e}, error: {ex}")
    return valid

def validate_claims(claim_list: List[dict]) -> List[Claim]:
    valid = []
    for c in claim_list:
        try:
            claim = Claim(**c)
            if claim.subject and claim.object and claim.evidence:
                valid.append(claim)
        except Exception as ex:
            print(f"Invalid claim: {c}, error: {ex}")
    return valid

def repair_claims(claims: List[Claim]) -> List[Claim]:
    #ensure confidence is between 0 and 1
    for c in claims:
        c.confidence = max(0, min(1, c.confidence))
    return claims