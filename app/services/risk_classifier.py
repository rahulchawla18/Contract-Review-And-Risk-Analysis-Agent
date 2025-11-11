import json
import re
from app.services.llm_factory import create_llm

# Initialize LLM using Groq
llm = create_llm(temperature=0.1)  # Lower temperature for more consistent, factual responses


RISK_PROMPT = """Classify each contract clause as High/Medium/Low Risk. Return ONLY valid JSON.

HIGH RISK: unlimited liability, no termination rights, excessive penalties, one-sided terms, ambiguous language, regulatory violations
MEDIUM RISK: moderate exposure, some unfavorable terms, minor concerns, needs monitoring
LOW RISK: standard practices, balanced terms, clear language, minimal exposure

Format: "Risk Level: [brief reason]"

{{
  "clause_name": "High Risk: reason" | "Medium Risk: reason" | "Low Risk: reason"
}}

Clauses:
{clauses}"""


def classify_risks(clauses: str):
    prompt = RISK_PROMPT.format(clauses=clauses)
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
            "raw_response": str(response)
        }