from pydantic import BaseModel
from typing import List

class Evidence(BaseModel):
    source_id: str
    excerpt: str
    start: int
    end: int
    timestamp: str

class Entity(BaseModel):
    id: str
    type: str
    name: str
    aliases: List[str] = []

class Claim(BaseModel):
    subject: str
    relation: str
    object: str
    confidence: float
    evidence: List[Evidence]