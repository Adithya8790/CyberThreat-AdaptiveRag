import requests
from neo4j import GraphDatabase


# ==============================
# CONFIGURATION
# ==============================

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "CyberThreatKG"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


# ==============================
# NEO4J
# ==============================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


def retrieve_threat_context(tx, attack_name):

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

    result = tx.run(
        query,
        attack_name=attack_name
    )

    return [record.data() for record in result]


# ==============================
# LLM REPORT GENERATION
# ==============================

def generate_report(context):

    prompt = f"""
You are a cybersecurity analyst assistant.

Generate a concise, evidence-grounded CTI report.

Use ONLY the information provided in the context below.
Do not invent CVEs, vulnerabilities, threat actors,
malware, evidence, or mitigations.

Threat Context:
{context}

Format your response as:

Detection:
Attack Type:
MITRE Technique:
Tactic:
Evidence:
Mitigation:
Analyst Summary:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    response.raise_for_status()

    return response.json()["response"]


# ==============================
# MAIN
# ==============================

attack = "DoS Hulk"

with driver.session() as session:

    context = session.execute_read(
        retrieve_threat_context,
        attack
    )

driver.close()


print("\n==============================")
print("       RETRIEVED CONTEXT")
print("==============================")

for item in context:

    print("Attack       :", item["attack"])
    print("Technique ID :", item["technique_id"])
    print("Technique    :", item["technique"])
    print("Tactic       :", item["tactic"])
    print("Mitigation   :", item["mitigation"])


print("\n==============================")
print("    EXPLAINABLE CTI REPORT")
print("==============================")

report = generate_report(context)

print(report)