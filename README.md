# Embedding Integrity & Fail-Fast Security for LLMs

This project explores **parameter-level security in Large Language Models (LLMs)** by detecting and blocking silent tampering of embedding matrices using **cryptographic integrity verification, audit logging, and fail-fast enforcement**.

Most GenAI systems focus on prompts, RAG, or fine-tuning.  
This project instead asks a lower-level but critical question:

> **How do we ensure that LLM embeddings have not been silently modified before a model is deployed or loaded?**

---

## 🚨 Problem Statement

Embedding matrices are the first learned parameters in an LLM.  
Even a small, targeted modification to a single token embedding can subtly alter model behavior.

While embeddings are typically stored in cloud-based artifact stores, **storage security alone does not guarantee parameter integrity**.  
Without explicit verification, silent embedding tampering can go undetected.

---

## 🎯 Project Goal

To design a **simple, explainable, and production-oriented mechanism** that:

- Treats base embeddings as **immutable trusted artifacts**
- Detects **single-token embedding tampering**
- Identifies **exactly which token was modified**
- Logs violations for audit and forensics
- Prevents corrupted embeddings from being used (**fail-fast**)

---

## 🧠 High-Level Design
Trusted Base Embeddings
↓
Cryptographic Hash Registration
↓
Candidate Embedding Artifact
↓
Token-Level Integrity Verification
↓
Audit Logging + Fail-Fast Blocking


Integrity checks are performed **at model load or deployment time**, not during inference.

---

## 🧱 Project Structure

embeddings-integrity/
│
├── embeddings/
│ ├── embedding_store.py # Embedding creation, load, save, update
│ ├── integrity.py # Hash-based integrity verification
│ ├── audit.py # Audit logging for violations
│ └── init.py
│
├── experiments/
│ ├── tamper_demo.py # Simulates single-token embedding tampering
│ ├── integrity_check_demo.py # Verifies integrity and enforces fail-fast
│ └── init.py
│
├── README.md
├── .gitignore
└── requirements.txt


---

## ⚙️ How It Works (Step-by-Step)

### 1️⃣ Base Embedding Creation
- A custom embedding matrix is created for a fixed vocabulary
- The base embedding artifact is treated as **immutable**
- Stored using `safetensors` for safety and consistency

### 2️⃣ Tampering Simulation
- A single token embedding (e.g., `"python"`) is modified
- All other embeddings remain unchanged
- A **new, versioned artifact** is created instead of overwriting the base

### 3️⃣ Integrity Registration
- Cryptographic hashes (SHA-256) are computed **per token embedding**
- These hashes represent the **trusted reference**

### 4️⃣ Integrity Verification
- Before loading embeddings, hashes are recomputed
- Token-level comparison detects even single-value changes
- Exact tampered tokens are identified

### 5️⃣ Audit & Fail-Fast Enforcement
- Any integrity violation is logged with timestamp and token name
- Execution is aborted immediately to prevent unsafe usage

---

## 🔐 Why Cryptographic Hashing?

- Detects even **single-bit changes**
- Fixed-size fingerprints (secure and efficient)
- Token-level granularity enables forensic analysis
- Independent of model architecture

Hashing is performed **once per artifact lifecycle**, not during inference.

---

## 📊 Example Audit Log

```json
{
  "timestamp": "2026-01-04 16:25:12",
  "embedding_file": "tampered_embeddings_1767543240.safetensors",
  "violated_tokens": ["python"]
}

How to Run
Clean previous artifacts
del embeddings/base_embeddings.safetensors
del embeddings/tampered_embeddings_*.safetensors
del embeddings/audit_log.json

Run tampering demo
python -m experiments.tamper_demo

Run integrity verification
python -m experiments.integrity_check_demo



📌 Disclaimer

This project is an educational and exploratory implementation designed to illustrate integrity concepts.
Large-scale production systems may use optimizations such as chunk-based hashing, Merkle trees, or signed manifests.

