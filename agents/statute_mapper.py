"""
Statute Mapper Agent

This module maps contract clauses to applicable legal statutes and regulations.
It helps identify which laws govern the contract, how clauses relate to statutes,
and whether any statutes can override or limit specific contract provisions.

The agent provides:
- Identification of applicable laws based on jurisdiction and context
- Mapping of contract clauses to relevant statutes
- Analysis of potential statute overrides or limitations
- Educational explanations (not legal advice)

This is useful for compliance checking and understanding the legal framework
that governs the contract.
"""
from google import genai
from google.genai.errors import ClientError


def map_statutes(contract_text: str, client: genai.Client) -> dict:
    """
    Maps contract clauses to applicable legal statutes and regulations.

    Args:
        contract_text: The contract text to analyze
        client: The Gemini AI client instance

    Returns:
        Dictionary containing statute mapping analysis results
    """
    if not contract_text or len(contract_text.strip()) < 20:
        return {"error": "Please provide a valid contract text."}

    prompt = f"""
You are a legal statute mapping assistant.

For the contract:
- Identify applicable laws
- Map clauses to statutes
- Explain if any statute can override or limit a clause
- Use simple explanations

Do NOT give legal advice. Explain educationally.

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
        return {"statute_mapping": response.text}

    try:
        for c in response.candidates:
            for p in c.content.parts:
                if hasattr(p, "text"):
                    return {"statute_mapping": p.text}
    except Exception:
        pass

    return {"error": "Unable to map statutes."}

