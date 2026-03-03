# IntelliCredit Engine

**AI-Powered Corporate Credit Decisioning & CAM Automation System**

IntelliCredit Engine is a modular AI-driven corporate credit decisioning system that automates multi-source document analysis, structured risk extraction, and explainable underwriting to generate professional Credit Appraisal Memos (CAM).

Designed for financial institutions and credit teams, the engine transforms unstructured corporate documents into structured intelligence and transparent lending recommendations.

---

## 🚀 Overview

Corporate credit appraisal often requires stitching together:

- Annual reports  
- Financial statements  
- GST filings  
- Bank statements  
- Legal notices  
- Regulatory disclosures  
- Due diligence notes  

IntelliCredit Engine automates this workflow using:

- Retrieval-Augmented Generation (RAG)
- Structured financial signal extraction
- Deterministic, explainable risk scoring
- Confidence-calibrated decision logic
- Automated CAM document generation

---

## 🏗️ Architecture


Document Upload
↓
Multi-Format Ingestion + OCR
↓
Vector Embedding (FAISS)
↓
Similarity-Based Retrieval
↓
Structured Risk Extraction
↓
Deterministic Credit Scoring
↓
Confidence Calibration
↓
Credit Appraisal Memo (DOCX)


---

## 🔍 Core Features

### 1️⃣ Multi-Format Ingestion
- PDF (native + scanned via OCR)
- PPTX
- Excel
- CSV
- Section-aware chunking
- Metadata enrichment (page number, document type, etc.)

### 2️⃣ Intelligent Retrieval
- FAISS-based similarity search
- Similarity score normalization
- Metadata-aware chunk processing
- Multi-document reasoning support

### 3️⃣ Structured Risk Extraction
Extracts financial and risk indicators such as:
- Revenue trends
- Debt obligations
- Litigation exposure
- Regulatory flags
- Sector headwinds
- Management instability

Outputs validated structured JSON for downstream scoring.

### 4️⃣ Deterministic Risk Scoring
Transparent scoring model based on:
- Financial strength
- Litigation risk
- Sector risk
- Operational risk
- Management risk

Outputs:
- Final Risk Score (0–100)
- Risk Category (Low / Moderate / High / Reject)
- Suggested Loan Limit
- Suggested Interest Rate

### 5️⃣ Confidence Calibration
Decision confidence calculated using:
- Similarity score weighting
- Document coverage ratio
- Extraction completeness

### 6️⃣ CAM Generation
Automatically generates structured Credit Appraisal Memos including:
- Executive Summary
- Company Overview
- Five Cs of Credit
- Risk Assessment
- Final Recommendation
- Evidence Appendix with citations

---

## 🛠️ Tech Stack

**Backend**
- Python
- FastAPI
- FAISS
- Pydantic
- Local LLM (LLaMA-based)
- Tesseract OCR

**Frontend**
- React
- Modular UI architecture

---

## 📦 Project Structure


intellicredit-engine/
│
├── backend/
│ ├── ingestion/
│ ├── retrieval/
│ ├── rag/
│ ├── credit_engine/
│ │ ├── extractor.py
│ │ ├── scoring.py
│ │ ├── cam_generator.py
│ │ └── utils.py
│ └── api/
│
├── frontend/
└── README.md


---

## 🎯 Design Principles

- Explainability over black-box predictions  
- Deterministic scoring logic  
- Metadata-aware evidence citation  
- Modular architecture  
- Production-ready deployment structure  

---

## 📌 Future Enhancements

- Hybrid search (BM25 + vector)
- Portfolio-level risk aggregation
- Stress scenario simulation
- Sector-specific scoring templates
- SaaS deployment layer

---

## 📄 License

This repository is intended for demonstration and research purposes.