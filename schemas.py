from typing import List, Optional
from pydantic import BaseModel, Field, conlist, confloat


# ---------------------------
# Structured Guidelines
# ---------------------------

class StructuredGuidelines(BaseModel):
    tone: str = Field(..., description="Brand tone description")

    forbidden_words: List[str] = Field(
        default_factory=list,
        description="Words that must not appear in content"
    )

    mandatory_phrases: List[str] = Field(
        default_factory=list,
        description="Phrases that must appear in content"
    )

    no_emojis: bool = Field(
        default=False,
        description="Whether emojis are forbidden"
    )

    max_sentence_length: Optional[int] = Field(
        default=None,
        description="Maximum allowed words per sentence"
    )


# ---------------------------
# Deterministic Violations
# ---------------------------

class DeterministicViolation(BaseModel):
    type: str
    message: str
    severity: str  # e.g. "low", "medium", "high"


# ---------------------------
# Semantic Violations
# ---------------------------

class SemanticViolation(BaseModel):
    type: str
    explanation: str
    suggestion: str


# ---------------------------
# Semantic Evaluation Output
# ---------------------------

class SemanticEvaluation(BaseModel):
    semantic_score: int = Field(..., ge=0, le=100)
    semantic_violations: List[SemanticViolation] = Field(default_factory=list)
    rewrite: str
    confidence: confloat(ge=0.0, le=1.0)


# ---------------------------
# Final Compliance Report
# ---------------------------

class ComplianceReport(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    deterministic_score: int = Field(..., ge=0, le=100)
    semantic_score: int = Field(..., ge=0, le=100)

    deterministic_violations: List[DeterministicViolation] = Field(default_factory=list)
    semantic_violations: List[SemanticViolation] = Field(default_factory=list)

    rewrite: str
    confidence: confloat(ge=0.0, le=1.0)
