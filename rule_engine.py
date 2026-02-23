import re
from typing import List, Tuple

from schemas import StructuredGuidelines, DeterministicViolation


class RuleEngine:
    """
    Deterministic compliance checker.
    Performs rule-based validation without AI.
    """

    def evaluate(
        self,
        guidelines: StructuredGuidelines,
        content: str,
    ) -> Tuple[int, List[DeterministicViolation]]:
        """
        Returns:
        - deterministic_score (0–100)
        - list of deterministic violations
        """

        violations: List[DetinisticViolation] = []

        violations.extend(self._check_forbidden_words(guidelines, content))
        violations.extend(self._check_mandatory_phrases(guidelines, content))
        violations.extend(self._check_emojis(guidelines, content))
        violations.extend(self._check_sentence_length(guidelines, content))

        score = self._calculate_score(violations)

        return score, violations

    # -------------------------
    # Individual Checks
    # -------------------------

    def _check_forbidden_words(
        self,
        guidelines: StructuredGuidelines,
        content: str,
    ) -> List[DeterministicViolation]:

        violations = []
        content_lower = content.lower()

        for word in guidelines.forbidden_words:
            if word.lower() in content_lower:
                violations.append(
                    DeterministicViolation(
                        type="forbidden_word",
                        message=f'Forbidden word detected: "{word}"',
                        severity="high",
                    )
                )

        return violations

    def _check_mandatory_phrases(
        self,
        guidelines: StructuredGuidelines,
        content: str,
    ) -> List[DeterministicViolation]:

        violations = []

        for phrase in guidelines.mandatory_phrases:
            if phrase not in content:
                violations.append(
                    DeterministicViolation(
                        type="missing_mandatory_phrase",
                        message=f'Mandatory phrase missing: "{phrase}"',
                        severity="medium",
                    )
                )

        return violations

    def _check_emojis(
        self,
        guidelines: StructuredGuidelines,
        content: str,
    ) -> List[DeterministicViolation]:

        violations = []

        if guidelines.no_emojis:
            # Basic emoji detection range
            emoji_pattern = re.compile(
                "["
                "\U0001F600-\U0001F64F"
                "\U0001F300-\U0001F5FF"
                "\U0001F680-\U0001F6FF"
                "\U0001F1E0-\U0001F1FF"
                "]+",
                flags=re.UNICODE,
            )

            if emoji_pattern.search(content):
                violations.append(
                    DeterministicViolation(
                        type="emoji_detected",
                        message="Emojis are not allowed by brand guidelines.",
                        severity="medium",
                    )
                )

        return violations

    def _check_sentence_length(
        self,
        guidelines: StructuredGuidelines,
        content: str,
    ) -> List[DeterministicViolation]:

        violations = []

        if guidelines.max_sentence_length is None:
            return violations

        sentences = re.split(r"[.!?]+", content)

        for sentence in sentences:
            words = sentence.strip().split()
            if len(words) > guidelines.max_sentence_length:
                violations.append(
                    DeterministicViolation(
                        type="sentence_too_long",
                        message=(
                            f"Sentence exceeds maximum length of "
                            f"{guidelines.max_sentence_length} words."
                        ),
                        severity="low",
                    )
                )

        return violations

    # -------------------------
    # Scoring
    # -------------------------

    def _calculate_score(
        self,
        violations: List[DeterministicViolation],
    ) -> int:
        """
        Simple weighted deduction scoring:
        - high severity: -20
        - medium severity: -10
        - low severity: -5
        Minimum score = 0
        """

        score = 100

        for violation in violations:
            if violation.severity == "high":
                score -= 20
            elif violation.severity == "medium":
                score -= 10
            elif violation.severity == "low":
                score -= 5

        return max(score, 0)
