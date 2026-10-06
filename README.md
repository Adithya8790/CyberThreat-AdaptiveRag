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
