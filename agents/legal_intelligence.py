from google import genai
from google.genai.errors import ClientError

def analyze_legal_intelligence(contract_text: str, client: genai.Client) -> dict:
    if not contract_text or len(contract_text.strip()) < 20:
        return {"error": "Please provide a valid contract text."}

    prompt = f"""
    You are a legal intelligence assistant for a Contract Lifecycle Management (CLM) system.

    Perform the following:
    1. Identify applicable laws based on jurisdiction and context
    2. Explain those laws in simple language
    3. Detect compliance gaps or missing protections
    4. Detect ambiguous or vague language
    5. Suggest safer and clearer wording
    6. Recommend whether legal review is required

    IMPORTANT:
    - Do NOT give legal advice
    - Do NOT suggest bypassing laws
    - Do NOT decide law hierarchy
    - Use cautious language

    Return STRICTLY in JSON with keys:
    - applicable_laws
    - law_explanations
    - compliance_gaps
    - ambiguous_clauses
    - why_ambiguous
    - safe_suggestions
    - review_recommendation

    Contract:
    {contract_text}
    """

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )
    except ClientError as e:
        if "429" in str(e):
            return {"error": "AI quota exceeded. Please try again later."}
        return {"error": str(e)}

    if getattr(response, "text", None):
        cleaned = response.text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    return {"legal_intelligence": cleaned}


    try:
        for c in response.candidates:
            for p in c.content.parts:
                if hasattr(p, "text"):
                    return {"legal_intelligence": p.text}
    except Exception:
        pass

    return {"error": "Unable to analyze legal intelligence."}
