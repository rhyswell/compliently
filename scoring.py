from typing import List

from config import Config
from schemas import (
    ComplianceReport,
    DeterministicViolation,
    SemanticEvaluation,
)


class ScoringEngine:
    """
    Aggregates deterministic and semantic results
    into a final ComplianceReport.
    """

    def aggregate(
        self,
        deterministic_score: int,
        deterministic_violations: List[DeterministicViolation],
        semantic_evaluation: SemanticEvaluation,
    ) -> ComplianceReport:
        """
        Combines:
        - deterministic score (weighted)
        - semantic score (weighted)
        - merges violations
        - returns final ComplianceReport
        """

        overall_score = self._calculate_weighted_score(
            deterministic_score,
            semantic_evaluation.semantic_score,
        )

        return ComplianceReport(
            overall_score=overall_score,
            deterministic_score=deterministic_score,
            semantic_score=semantic_evaluation.semantic_score,
            deterministic_violations=deterministic_violations,
            semantic_violations=semantic_evaluation.semantic_violations,
            rewrite=semantic_evaluation.rewrite,
            confidence=semantic_evaluation.confidence,
        )

    def _calculate_weighted_score(
        self,
        deterministic_score: int,
        semantic_score: int,
    ) -> int:
        """
        Weighted average using Config weights.
        """

        weighted = (
            deterministic_score * Config.DETERMINISTIC_WEIGHT
            + semantic_score * Config.SEMANTIC_WEIGHT
        )

        return max(0, min(100, int(round(weighted))))
