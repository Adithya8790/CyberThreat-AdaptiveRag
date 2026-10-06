from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "CyberThreatKG"


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


def retrieve_threat_context(attack_name):

    query = """
    MATCH (a:Attack {name: $attack_name})
          -[:MAPS_TO]->
          (t:Technique)

    OPTIONAL MATCH (t)-[:BELONGS_TO]->(tactic:Tactic)

    OPTIONAL MATCH (t)-[:MITIGATED_BY]->(m:Mitigation)

    RETURN
        a.name AS attack,
        t.id AS technique_id,
        t.name AS technique,
        tactic.name AS tactic,
        m.name AS mitigation
    """

    with driver.session() as session:

        result = session.run(
            query,
            attack_name=attack_name
        )

        return [record.data() for record in result]


if __name__ == "__main__":

    attack = "DoS Hulk"

    context = retrieve_threat_context(attack)

    print("\n==============================")
    print("       GRAPHRAG RETRIEVAL")
    print("==============================")

    for item in context:

        print("Attack       :", item["attack"])
        print("Technique ID :", item["technique_id"])
        print("Technique    :", item["technique"])
        print("Tactic       :", item["tactic"])
        print("Mitigation   :", item["mitigation"])


driver.close()