from app.services.llm_factory import create_llm

# Initialize LLM using Groq
llm = create_llm(temperature=0.2)  # Slightly higher for more creative suggestions


REVISION_PROMPT = """Analyze contract clauses and provide prioritized revision suggestions. Focus on: unlimited liability, missing protections, ambiguous terms, unfair provisions, compliance issues.

Format:
EXECUTIVE SUMMARY: [2-3 sentences on critical issues]

HIGH PRIORITY:
• [Clause]: [Problem]. [Recommended change]. [Rationale]

MEDIUM PRIORITY:
• [Clause]: [Problem]. [Recommended change]. [Rationale]

Be specific and actionable.

Clauses:
{clauses}"""


def suggest_revisions(clauses: str):
    prompt = REVISION_PROMPT.format(clauses=clauses)
    response = llm.invoke(prompt)
    # Extract text content from LLM response
    if hasattr(response, 'content'):
        response = response.content
    return str(response)