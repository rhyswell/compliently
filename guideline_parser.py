import json
from typing import Any

from pydantic import ValidationError

from config import Config
from schemas import StructuredGuidelines


class GuidelineParser:
    """
    Uses GPT-5.2 to convert raw brand guidelines text
    into structured JSON that matches StructuredGuidelines schema.
    """

    SYSTEM_PROMPT = """
You are a strict information extraction engine.

Extract structured brand rules from the provided brand guidelines.

Return ONLY valid JSON.
No markdown.
No explanations.
No extra text.

The JSON must strictly match this schema:

{
  "tone": string,
  "forbidden_words": string[],
  "mandatory_phrases": string[],
  "no_emojis": boolean,
  "max_sentence_length": integer | null
}

If a field is not specified in the guidelines:
- Use empty list for arrays
- Use false for booleans
- Use null for optional integers
"""

    def __init__(self) -> None:
        self.client = Config.get_client()

    def parse(self, raw_guidelines: str) -> StructuredGuidelines:
        """
        Parse guidelines text into StructuredGuidelines object.
        Retries up to 2 times if JSON validation fails.
        """

        for attempt in range(3):
            response = self.client.responses.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Brand Guidelines:\n{raw_guidelines}",
                    },
                ],
                max_completion_tokens=Config.MAX_COMPLETION_TOKENS_GUIDELINES,
            )

            raw_output = response.output_text.strip()

            try:
                parsed_json: Any = json.loads(raw_output)
                validated = StructuredGuidelines(**parsed_json)
                return validated

            except (json.JSONDecodeError, ValidationError):
                if attempt == 2:
                    raise ValueError(
                        "Failed to parse structured guidelines after multiple attempts."
                    )

        raise ValueError("Unexpected parsing failure.")
