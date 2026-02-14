"""
Bias Meter / Fairness Analyzer Agent

This module analyzes contracts for fairness and bias between parties.
It determines which party (Client, Vendor, or Neutral) is favored by the contract
and provides a quantitative bias score along with reasoning.

The agent evaluates:
- Party favoritism (Client vs Vendor vs Neutral)
- Reasons for bias determination
- Bias score from -5 (client heavy) to +5 (vendor heavy)

This is useful for ensuring balanced contracts and identifying potentially
one-sided agreements that may need renegotiation.
"""
from google import genai
from google.genai.errors import ClientError


def analyze_bias(contract_text: str, client: genai.Client) -> dict:
    """
    Analyzes contract fairness and bias between parties.

    Args:
        contract_text: The contract text to analyze
        client: The Gemini AI client instance

    Returns:
        Dictionary containing bias analysis results with score and reasoning
    """
    if not contract_text or len(contract_text.strip()) < 20:
        return {"error": "Please provide a valid contract text."}

    prompt = f"""
You are a contract fairness analyzer.

Analyze the contract and determine:
- Which party is favored (Client / Vendor / Neutral)
- Why (list reasons)
- Give a bias score from -5 (client heavy) to +5 (vendor heavy)

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
        return {"bias_analysis": response.text}

    try:
        for c in response.candidates:
            for p in c.content.parts:
                if hasattr(p, "text"):
                    return {"bias_analysis": p.text}
    except Exception:
        pass

    return {"error": "Unable to analyze contract bias."}

