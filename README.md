# Compliantly – AI Brand Compliance Checker

Compliantly is a hybrid AI + rule-based brand compliance engine built in Python. It automatically evaluates marketing content against brand guidelines and produces a structured compliance report with scoring, violations, rewrite suggestions, and confidence estimation.

This project demonstrates applied LLM system design using GPT-5.2, deterministic validation pipelines, strict JSON schema enforcement, and modular backend architecture.

---

## Overview

Marketing teams rely on brand guidelines to maintain tone, voice, and consistency across content. Manual compliance reviews are slow, subjective, and error-prone.

Compliantly automates this process by:

* Parsing raw brand guidelines (text or PDF)
* Structuring them into machine-readable rules using GPT-5.2
* Running deterministic compliance checks
* Performing semantic brand alignment evaluation
* Producing a final compliance score and rewrite suggestion

The result is an explainable, hybrid compliance engine rather than a simple chatbot wrapper.

---

## Key Features

### 1. Hybrid Architecture

Compliantly combines:

* Deterministic rule-based checks (forbidden words, mandatory phrases, emoji usage, sentence length)
* GPT-powered semantic evaluation (tone alignment, voice consistency, contextual violations)
* Weighted score aggregation (40% deterministic, 60% semantic)

This design ensures both objectivity and contextual understanding.

---

### 2. Strict JSON Schema Enforcement

All GPT outputs are:

* Constrained to strict JSON-only responses
* Validated with Pydantic models
* Automatically retried on validation failure

This ensures reliability and production-grade robustness when interacting with LLMs.

---

### 3. Structured Compliance Report

The final output includes:

* Overall compliance score (0–100)
* Deterministic score
* Semantic score
* List of violations (typed and severity-based)
* Fully compliant suggested rewrite
* Confidence score (0.0–1.0)

This makes results explainable and actionable.

---

### 4. PDF and Text Support

Brand guidelines can be:

* Pasted as plain text
* Uploaded as PDF and automatically parsed

The system extracts and normalizes text before AI processing.

---

### 5. Desktop Application (Tkinter)

The application includes a simple but functional GUI:

* Brand guideline input panel
* Content input panel
* Compliance execution button
* Structured results display

The UI orchestrates the full compliance pipeline end-to-end.

---

## Architecture

```
compliantly/
│
├── config.py
├── schemas.py
├── pdf_parser.py
├── rule_engine.py
├── guideline_parser.py
├── semantic_engine.py
├── scoring.py
└── main.py
```

### Execution Flow

1. User provides guidelines (text or PDF).
2. Guidelines are parsed into structured rules using GPT-5.2.
3. Deterministic rule engine evaluates objective violations.
4. Semantic engine evaluates tone and contextual alignment.
5. Scores are aggregated.
6. A structured compliance report is displayed.

---

## Technical Highlights

This project demonstrates:

* LLM orchestration using GPT-5.2 (message-based API, no temperature)
* Strict JSON output enforcement
* Schema validation with Pydantic
* Retry logic for invalid LLM outputs
* Hybrid AI + deterministic system design
* Modular backend architecture
* Clean separation of concerns
* Weighted scoring aggregation
* GUI-based application orchestration

It is designed as an engineering project, not just an AI demo.

---

## GPT Integration Strategy

The system uses:

* Message-based API calls
* No temperature parameter
* Explicit JSON schema instructions
* Pydantic validation
* Controlled max_completion_tokens
* Structured payload injection

This reduces hallucination risk and ensures deterministic behavior in production-like conditions.

---

## Example Compliance Output (Conceptual)

```
Overall Score: 82
Deterministic Score: 90
Semantic Score: 78
Confidence: 0.87

Deterministic Violations:
- [HIGH] Forbidden word detected: "cheap"

Semantic Violations:
- tone_mismatch: The content is overly casual for a professional brand.
  Suggestion: Use more confident and structured language.

Suggested Rewrite:
[Rewritten compliant version]
```

---

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/compliantly.git
cd compliantly
```

2. Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Set your OpenAI API key:

```
export OPENAI_API_KEY="your_key_here"      # macOS/Linux
setx OPENAI_API_KEY "your_key_here"        # Windows
```

5. Run the application:

```
python main.py
```

---

## Future Improvements

* REST API version using FastAPI
* Multi-brand profile management
* Persistent structured guideline storage
* Audit logging
* CI/CD pipeline integration
* Web-based interface
* Batch document compliance checking
