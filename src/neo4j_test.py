from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "CyberThreatKG"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

def get_attack_context(tx, attack_name):
    query = """
    MATCH (a:Attack {name: $attack_name})
          -[:MAPS_TO]->
          (t:Technique)
    OPTIONAL MATCH (t)-[:BELONGS_TO]->(tactic:Tactic)
    RETURN a.name AS attack,
           t.id AS technique_id,
           t.name AS technique,
           tactic.name AS tactic
    """

    result = tx.run(query, attack_name=attack_name)

    return [record.data() for record in result]


with driver.session() as session:
    attack = "PortScan"

    results = session.execute_read(
        get_attack_context,
        attack
    )

    print("\n==============================")
    print("     THREAT CONTEXT")
    print("==============================")

    for result in results:
        print("Attack       :", result["attack"])
        print("Technique ID :", result["technique_id"])
        print("Technique    :", result["technique"])
        print("Tactic       :", result["tactic"])

driver.close()