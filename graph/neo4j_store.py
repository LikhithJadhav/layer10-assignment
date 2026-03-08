from neo4j import GraphDatabase
from schema import Entity, Claim

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

def create_entity(tx, entity: Entity):
    tx.run(
        """
        MERGE (e:Entity {id: $id})
        SET e.name = $name, e.type = $type
        """,
        id=entity.id, name=entity.name, type=entity.type
    )

def create_claim(tx, claim: Claim):
    tx.run(
        """
        MATCH (s:Entity {id: $s})
        MATCH (o:Entity {id: $o})
        CREATE (c:Claim {relation: $r, confidence: $conf})
        MERGE (s)-[:SUBJECT]->(c)
        MERGE (c)-[:OBJECT]->(o)
        """,
        s=claim.subject, o=claim.object, r=claim.relation, conf=claim.confidence
    )

    for ev in claim.evidence:
        tx.run(
            """
            MATCH (c:Claim {relation: $r, confidence: $conf})
            CREATE (e:Evidence {source_id: $sid, excerpt: $ex, timestamp: $ts})
            MERGE (c)-[:SUPPORTED_BY]->(e)
            """,
            r=claim.relation, conf=claim.confidence, sid=ev.source_id, ex=ev.excerpt, ts=ev.timestamp
        )

def store_entities(entities: List[Entity]):
    with driver.session() as session:
        for e in entities:
            session.execute_write(create_entity, e)

def store_claims(claims: List[Claim]):
    with driver.session() as session:
        for c in claims:
            session.execute_write(create_claim, c)