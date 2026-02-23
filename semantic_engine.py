import json
from typing import Any

from pydantic import ValidationError

from config import Config
from schemas import (
    StructuredGuidelines,
    SemanticEvaluation,
)


class SemanticEngine:
    """
    Uses GPT-5.2 to perform semantic compliance evaluation.
    Returns strict JSON validated against SemanticEvaluation schema.
    """

    SYSTEM_PROMPT = """
You are a brand compliance evaluation engine.

Evaluate the provided content against structured brand guidelines.

Return ONLY valid JSON.
No markdown.
No explanations.
No extra text.

The JSON must strictly match this schema:

{
  "semantic_score": integer (0-100),
  "semantic_violations": [
    {
      "type": string,
      "explanation": string,
      "suggestion": string
    }
  ],
  "rewrite": string,
  "confidence": float (0.0-1.0)
}

Rules:
- semantic_score must reflect tone and voice alignment.
- Provide clear explanations.
- rewrite must be fully compliant.
- confidence reflects your certainty in the evaluation.
"""

    def __init__(self) -> None:
        self.client = Config.get_client()

    def evaluate(
        self,
        guidelines: StructuredGuidelines,
        content: str,
    ) -> SemanticEvaluation:
        """
        Evaluate semantic compliance.
        Retries up to 2 times if JSON validation fails.
        """

        payload = {
            "structured_guidelines": guidelines.model_dump(),
            "content_to_evaluate": content,
        }

        for attempt in range(3):
            response = self.client.responses.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": json.dumps(payload, indent=2),
                    },
                ],
                max_completion_tokens=Config.MAX_COMPLETION_TOKENS_SEMANTIC,
            )

            raw_output = response.output_text.strip()

            try:
                parsed_json: Any = json.loads(raw_output)
                validated = SemanticEvaluation(**parsed_json)
                return validated

            except (json.JSONDecodeError, ValidationError):
                if attempt == 2:
                    raise ValueError(
                        "Failed to parse semantic evaluation after multiple attempts."
                    )

        raise ValueError("Unexpected semantic evaluation failure.")
