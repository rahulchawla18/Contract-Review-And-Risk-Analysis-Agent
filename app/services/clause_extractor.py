import json
import re
from app.services.llm_factory import create_llm

# Initialize LLM using Groq
llm = create_llm(temperature=0.1)  # Lower temperature for more consistent, factual responses


CLAUSE_PROMPT = """Extract these 5 clause types from the contract. Return ONLY valid JSON, no markdown.

TERMINATION: termination conditions, notice periods, consequences, automatic triggers
CONFIDENTIALITY: NDA obligations, confidential info definition, duration, exceptions
PAYMENT_TERMS: amounts, schedules, due dates, late fees, currency, payment method
LIABILITY: liability caps, indemnification, warranties, damage limits, insurance
GOVERNING_LAW: jurisdiction, applicable law, dispute resolution (arbitration/courts)

Use "not_found" if a clause type is missing. Extract actual provisions, not just mentions.

{{
  "termination": "summary or 'not_found'",
  "confidentiality": "summary or 'not_found'",
  "payment_terms": "summary or 'not_found'",
  "liability": "summary or 'not_found'",
  "governing_law": "summary or 'not_found'"
}}

Contract:
{content}"""


def extract_clauses(content: str):
    prompt = CLAUSE_PROMPT.format(content=content)
    response = llm.invoke(prompt)
    # Extract text content from LLM response
    if hasattr(response, 'content'):
        response = response.content
    response = str(response)
    
    # Try to parse JSON from the response
    try:
        # Extract JSON from markdown code blocks if present
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            response = json_match.group(1)
        
        # Try to find JSON object in the response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        
        # If no JSON found, try parsing the whole response
        return json.loads(response)
    except (json.JSONDecodeError, AttributeError):
        # Fallback: return a dict with the raw response
        return {
            "error": "Failed to parse JSON response",
            "raw_response": str(response),
            "termination": "not_found",
            "confidentiality": "not_found",
            "payment_terms": "not_found",
            "liability": "not_found",
            "governing_law": "not_found"
        }