# Adaptive GraphRAG-Based Cyber Threat Intelligence Framework for Explainable Intrusion Detection

An AI-driven cybersecurity framework that combines **Machine Learning-based Intrusion Detection**, **Cyber Threat Intelligence**, **Neo4j Knowledge Graphs**, **Graph Retrieval-Augmented Generation (GraphRAG)**, and a **local Large Language Model (LLM)** to provide contextual and explainable analysis of suspicious network activity.

---

## 📌 Overview

Traditional Intrusion Detection Systems (IDS) primarily focus on identifying whether network traffic is malicious or benign. However, detecting an attack is only the first step of cybersecurity analysis.

Security analysts also need to understand:

- What type of attack occurred?
- Which MITRE ATT&CK technique is associated with it?
- Which tactical objective does the technique belong to?
- What evidence supports the classification?
- What mitigation strategy should be applied?
- Why was the network activity considered suspicious?

This project addresses these challenges by integrating a Machine Learning-based IDS with a **Cyber Threat Knowledge Graph** and **GraphRAG-based contextual retrieval**.

The system follows the pipeline:

```text
Network Traffic
      ↓
Data Preprocessing
      ↓
Machine Learning IDS
      ↓
Attack Detection
      ↓
Cyber Threat Knowledge Graph
      ↓
GraphRAG Retrieval
      ↓
Verified Threat Context
      ↓
Local LLM
      ↓
Explainable Cyber Threat Intelligence

# Adaptive GraphRAG-Based Cyber Threat Intelligence Framework for Explainable Intrusion Detection

An AI-assisted cybersecurity framework that combines Machine Learning-based Intrusion Detection Systems (IDS), a Cyber Threat Knowledge Graph, GraphRAG-based retrieval, and a local Large Language Model (LLM) to provide contextual, explainable, and hallucination-free cyber threat intelligence.

---

## 1. Project Overview & Architecture

Modern Intrusion Detection Systems (IDS) can classify network traffic as benign or malicious, but standard classification outputs lack the critical context that security analysts need to investigate an alert. 

This framework bridges the gap between raw machine learning detection and human-readable threat understanding. Instead of feeding raw alerts directly into an LLM (which introduces severe hallucination risks), this system utilizes a **Knowledge Graph** to retrieve verified facts first, passing them to a local LLM strictly as an explanation layer.

### Core Workflow Pipeline
1. **Network Data Input:** Network-flow records from the `CIC-IDS2017` dataset.
2. **Machine Learning IDS:** A Random Forest classifier evaluates the data and predicts traffic classes with a confidence score.
3. **GraphRAG Retrieval:** If an attack is detected, the system queries a Neo4j Cyber Threat Knowledge Graph to extract corresponding MITRE ATT&CK techniques, tactics, and verified mitigations.
4. **Local LLM Generation:** Llama 3.2 (3B) processes the verified graph context via Ollama to output an analyst-friendly threat summary.

---

## 2. Main Technologies Used

* **Language:** Python
* **Data Processing:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (Random Forest Classifier), Joblib
* **Knowledge Graph:** Neo4j, Cypher Query Language, Neo4j Python Driver
* **LLM Orchestration:** Ollama, Llama 3.2 (3B)

---

## 3. Project Structure

```text
AdaptiveRAG/
│
├── data/
│   ├── CIC-IDS2017/          # Raw dataset CSV files (Excluded from Git)
│   └── processed/
│       └── training_data.csv # Balanced 4-class training subset
│
├── models/
│   └── random_forest_ids.joblib
│
├── src/
│   ├── check_dataset.py      # Dataset health, shape, and label checking
│   ├── create_dataset.py     # Class selection, balancing, and preprocessing
│   ├── train_model.py        # Stratified splitting, model training, and saving
│   ├── predict.py            # Interactive prediction script
│   ├── neo4j_test.py         # Graph database connectivity validator
│   ├── graphrag.py           # Contextual relationship extraction engine
│   └── llm_report.py         # End-to-end GraphRAG + Ollama report generator
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 4. Dataset & Preprocessing

The initial prototype uses the benchmark **CIC-IDS2017** dataset. Due to extreme class imbalances in raw traffic logs, the pipeline extracts a balanced downsampled subset containing **10,000 samples per class** across four core classes (Total: 40,000 rows, 79 features):
* `BENIGN`
* `DDoS`
* `DoS Hulk`
* `PortScan`

### Preprocessing Operations:
* Normalizes column names (e.g., strips accidental leading spaces such as `" Label"` to `"Label"`).
* Replaces or drops infinite (`inf`) and missing (`NaN`) numeric values.
* Generates a balanced, clean file at `data/processed/training_data.csv`.

---

## 5. Machine Learning IDS & Results

The detection layer uses a **Random Forest Classifier** configured with 100 estimators. Under a standard 80/20 stratified train/test split, the prototype yields an accuracy of **99.88%** with Precision, Recall, and F1-scores approximating 1.00.

> ⚠️ **Evaluation Warning:** This near-perfect accuracy reflects standard random partitioning on a single localized dataset. It should not be interpreted as absolute real-world performance. Production deployments require testing against time-based splits, withheld classes, and cross-dataset evaluations.

---

## 6. Cyber Threat Knowledge Graph & GraphRAG

Threat metadata is managed locally inside a **Neo4j database** mapping attack types to concrete security blueprints.

### Graph Architecture Example:
* `[Attack: DoS Hulk]` → `[MAPS_TO]` → `[Technique: T1498 (Network Denial of Service)]`
* `[Technique: T1498]` → `[BELONGS_TO]` → `[Tactic: Impact]`
* `[Technique: T1498]` → `[MITIGATED_BY]` → `[Mitigation: Rate limiting and traffic filtering]`

The **GraphRAG** layer queries this mapping deterministically, ensuring that facts passed to the LLM are exclusively derived from verified threat intelligence.

---

## 7. Installation & Setup

### Prerequisites
1. Install [Ollama](https://ollama.com) and download the model:
   ```bash
   ollama pull llama3.2:3b
   ```
2. Install and run a local instance of [Neo4j](https://neo4j.com) (Default URI: `bolt://localhost:7687`).

### Environment Setup
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd CyberThreat-AdaptiveRag
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 8. Execution Guide

Run the framework components sequentially:

1. **Prepare Dataset:** Download the raw CIC-IDS2017 files, place them in `data/CIC-IDS2017/`, and run:
   ```bash
   python src/create_dataset.py
   ```
2. **Train Model:** Train the Random Forest classifier:
   ```bash
   python src/train_model.py
   ```
3. **Interactive Prediction Test:** Run predictions manually on random dataset samples:
   ```bash
   python src/predict.py
   ```
4. **Validate Graph Setup:** Test connection to your active Neo4j database:
   ```bash
   python src/neo4j_test.py
   ```
5. **Generate Explainable Intelligence Report:** Execute the full GraphRAG pipeline with the local LLM:
   ```bash
   python src/llm_report.py
   ```

---

## 9. Future Scope & Roadmap

* **Hybrid Detection:** Integrate unsupervised anomaly detection (e.g., Isolation Forests, Autoencoders) to intercept zero-day or unknown attacks.
* **Advanced GraphRAG:** Introduce vector similarity lookups to ingest unstructured CTI reports, whitepapers, and CVE details alongside structured Neo4j graph nodes.
* **SOC Integration:** Transition from file-based execution to live packet network flow streams integrated into an interactive SOC analytical dashboard.
* **Analyst-in-the-Loop:** Establish feedback vectors to update model weights and adjust graph properties based on security analyst corrections.

---

## 10. Disclaimer

This framework is built exclusively for academic research, defensive security education, and explainable AI exploration. It is a prototype and should not be used as a production-grade enterprise security solution without comprehensive validation.

