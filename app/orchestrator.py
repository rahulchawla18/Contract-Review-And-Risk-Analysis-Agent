import json
from concurrent.futures import ThreadPoolExecutor
from app.services.clause_extractor import extract_clauses
from app.services.risk_classifier import classify_risks
from app.services.revision_agent import suggest_revisions


def run_full_review(text: str, progress=None):
    """
    Run full contract review with parallel processing for independent tasks.
    """
    # Step 1: Extract clauses (must be done first)
    if progress:
        progress(0.3, desc="Analyzing contract clauses...")
    clauses = extract_clauses(text)
    
    # Convert clauses dict to string for risk classification and revision suggestions
    clauses_str = json.dumps(clauses) if isinstance(clauses, dict) else str(clauses)
    
    # Step 2 & 3: Run risk classification and revision suggestions in parallel
    # These are independent of each other and can run simultaneously
    if progress:
        progress(0.5, desc="Analyzing risks and generating suggestions (parallel processing)...")
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submit both tasks
        risk_future = executor.submit(classify_risks, clauses_str)
        suggestion_future = executor.submit(suggest_revisions, clauses_str)
        
        # Wait for both to complete
        risks = risk_future.result()
        suggestions = suggestion_future.result()
    
    if progress:
        progress(1.0, desc="Analysis complete!")

    return {
        "clauses": clauses,
        "risks": risks,
        "suggestions": suggestions,
    }