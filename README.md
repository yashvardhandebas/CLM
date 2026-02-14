# CLM
Perfect. Here is a **clean, professional, copy-paste ready README** with:

* Clear structure
* Clean formatting
* Architecture diagrams (Markdown compatible)
* Recruiter-friendly language
* Not over-cluttered
* GitHub-ready

You can copy this whole thing directly into `README.md`.

---

# ⚖️ AI CLM Paralegal Assistant

An AI-powered **Contract Lifecycle Management (CLM)** system that simulates a paralegal-level contract intelligence assistant using multi-agent LLM architecture, RAG, OCR, legal reasoning, fraud detection, bias analysis, and explainable decision support.

---

## 🚀 Overview

Contracts are long, complex, and legally risky.
This system helps users:

* Upload **PDF (text or scanned)** contracts
* Extract key clauses automatically
* Detect legal risks
* Identify fraud indicators
* Analyze fairness and bias
* Map clauses to governing statutes
* Simulate breach scenarios
* Ask follow-up questions interactively
* Get a structured final recommendation

It is designed as a **decision-support system**, not legal advice.

---

# 🏗 System Architecture

## High-Level Flow

```
User Input (PDF / Text)
            ↓
OCR + Text Extraction
            ↓
RAG Indexing (Gemini Embeddings + ChromaDB)
            ↓
Multi-Agent Analysis Layer
            ↓
Final Recommendation Engine
            ↓
Interactive Q&A (Memory + RAG)
```

---

## Detailed Architecture

```
                 ┌────────────────────┐
                 │     Streamlit UI    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │     FastAPI API     │
                 └─────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 PDF/OCR Layer       RAG Engine         Session Memory
 (pdfplumber +       (ChromaDB +         (Context +
  Tesseract OCR)     Embeddings)         User Profile)
        │                  │                  │
        └──────────────┬───┴──────────────────┘
                       ▼
               Multi-Agent System
        (Risk, Bias, Fraud, Legal Mapping,
          Stress Test, Clause Extraction)
                       ▼
             Final Recommendation Engine
```

---

# 🧠 Core Features

---

## 📄 Universal PDF Support (Text + Scanned)

* Supports digital PDFs
* Uses **Tesseract OCR** for scanned documents
* Automatically detects extraction method
* Designed for real-world legal workflows

---

## 🔍 Clause Extraction Agent

Automatically identifies:

* Payment clauses
* Termination clauses
* Liability provisions
* Confidentiality terms
* Jurisdiction details

> “Finds important sections instantly.”

---

## ⚠️ Risk Analysis Agent

Detects:

* Unlimited liability
* One-sided termination
* Missing protections
* High financial exposure
* Structural weaknesses

> “Highlights where the contract may hurt you.”

---

## 📚 Legal Intelligence & Statute Mapper

* Identifies applicable laws
* Maps clauses to statutes
* Explains enforceability
* Flags legally weak provisions
* Explains when statutes may override clauses

> “Explains whether the contract would hold up in court.”

---

## 🚨 Fraud Risk Indicator Engine

Analyzes for:

* Fraudulent misrepresentation
* Deceptive terms
* Power imbalance exploitation
* Non-disclosure risks
* Hidden manipulation risks

> “Checks if someone could trick you using hidden wording.”

---

## ⚖️ Bias Meter (Fairness Analyzer)

Determines:

* Client-favored
* Vendor-favored
* Balanced

Provides reasoning and fairness insights.

> “Tells you if the contract is tilted toward one party.”

---

## 🧪 Loophole Detector / Stress Test

Simulates:

* Vendor breach scenario
* Client breach scenario

Evaluates:

* Who is protected
* Who is vulnerable
* Likely legal outcome

> “Imagines what happens if things go wrong.”

---

## 🧩 Compliance Gap Analyzer

Identifies:

* Missing dispute resolution clauses
* Lack of reciprocal rights
* Regulatory gaps
* Incomplete protections

> “Finds what’s missing, not just what’s written.”

---

## 🧠 RAG (Retrieval-Augmented Generation)

* Splits contracts into chunks
* Generates embeddings using Gemini
* Stores vectors in ChromaDB
* Retrieves only relevant sections during Q&A

Benefits:

* Reduces hallucination
* Handles long contracts
* Improves accuracy

---

## 🗂 Session Memory

* Remembers user identity (e.g., name)
* Maintains conversational context
* Supports interactive Q&A
* Session-based (no permanent storage)

---

## 🏁 Final Recommendation Engine

Aggregates outputs from all agents and produces:

* Overall Risk Level
* Legal Stability Assessment
* Fairness Evaluation
* Structured Final Recommendation:

  * Accept
  * Review Before Signing
  * Reject
* Clear reasoning and next steps

> Acts like a senior paralegal decision assistant.

---

# 🛠 Tech Stack

### Backend

* FastAPI
* Google Gemini API (`google.genai`)
* Pydantic

### AI Layer

* Gemini 2.5 Flash (LLM)
* text-embedding-004 (Embeddings)
* Multi-agent prompt architecture

### Vector Database

* ChromaDB

### OCR

* Tesseract OCR
* pytesseract
* pdf2image

### Frontend

* Streamlit

---

# 📦 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-clm-paralegal.git
cd ai-clm-paralegal
```

---

## 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn streamlit chromadb pytesseract pdf2image pillow requests python-dotenv
```

---

## 3️⃣ Install Tesseract (Required for OCR)

Download from:

[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Update path in:

```
utils/pdf_reader.py
```

---

## 4️⃣ Add Gemini API Key

Create `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

# ▶️ Running the Application

## Start Backend

```bash
uvicorn main:app --reload
```

## Start UI

```bash
streamlit run ui.py
```

Open:

```
http://localhost:8501
```

---

# 🧪 Usage Flow

1. Upload contract (PDF or text)
2. System performs multi-agent analysis
3. Review risk & fairness report
4. Ask follow-up questions
5. Get final recommendation

---

# 🎯 Design Philosophy

* Modular multi-agent architecture
* Explainable AI outputs
* Reduced hallucination via RAG
* Real-world document compatibility (OCR)
* Decision-support focused
* Not a replacement for lawyers

---

# 🔮 Future Improvements

* Clause redlining suggestions
* Version comparison engine
* Risk scoring algorithm
* Visual bias meter UI
* Exportable PDF reports
* Cloud deployment

---

# 📌 Disclaimer

This system provides AI-based decision support and educational insights.
It does not provide legal advice.

---

# 👨‍💻 Author

Yashvardhan Debas
AI & Legal-Tech Enthusiast

Built as an advanced multi-agent LLM system simulating a contract intelligence assistant.

---
