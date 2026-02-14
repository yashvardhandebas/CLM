"""
Fraud Detector Agent

This module analyzes contract text for fraud-related red flags and indicators.
It helps identify clauses or patterns that could indicate fraudulent intent,
unusual payment terms, identity/authority risks, or other fraud indicators.

Does NOT provide legal advice; provides decision-support insights.
"""
from google import genai
from google.genai.errors import ClientError


def detect_fraud_indicators(contract_text: str, client: genai.Client) -> dict:
    """
    Scans contract text for fraud risk indicators.

    Args:
        contract_text: The contract text to analyze
        client: The Gemini AI client instance

    Returns:
        Dictionary containing fraud_indicators text (or error key on failure)
    """
    if not contract_text or len(contract_text.strip()) < 20:
        return {"error": "Please provide a valid contract text."}

    prompt = f"""
You are a contract fraud-risk analyst.

Analyze the contract for fraud-related red flags, such as:
- Unusual or rushed payment terms (e.g., upfront full payment, wire-only)
- Vague or missing party identity / authority
- Clauses that obscure who is liable or who performs work
- Pressure tactics or urgency language
- Missing or weak dispute resolution / recourse
- Inconsistencies between parties, amounts, or deliverables
- Any other indicators that could suggest fraud risk

Provide:
1. Overall fraud risk level (Low / Medium / High)
2. List of specific indicators found (or "None identified")
3. Brief reasoning for each
4. Practical next steps (e.g., verify identity, get legal review)

Do NOT provide legal advice. Provide decision-support insights only.

Contract:
{contract_text}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
        )
    except ClientError as e:
        if "429" in str(e):
            return {"error": "AI quota exceeded. Please try again later."}
        return {"error": str(e)}

    if getattr(response, "text", None):
        return {"fraud_indicators": response.text}

    try:
        for c in response.candidates:
            for p in c.content.parts:
                if hasattr(p, "text"):
                    return {"fraud_indicators": p.text}
    except Exception:
        pass

    return {"error": "Unable to detect fraud indicators."}
