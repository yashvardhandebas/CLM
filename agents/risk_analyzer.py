#responsible for analyzing the risks in the contract and if there are any one sided clauses or something that can harm the clinet
from google import genai
from google.genai.errors import ClientError

def analyze_risks(contract_text: str, client: genai.Client) -> dict:
    if not contract_text or len(contract_text.strip()) < 20:
        return {"error": "Please provide a valid contract text."}

    prompt = f"""
    You are a senior legal risk analyst.

    Analyze the following contract and identify risks.
    Focus on:
    - One-sided clauses
    - Unlimited liability
    - Missing termination rights
    - Excessive penalties
    - Ambiguous terms

    Return the result in JSON with:
    - risk_level
    - risks
    - suggestions

    Contract:
    {contract_text}
    """

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )
    except ClientError:
        return {"error": "AI quota exceeded. Try again later."}

    if getattr(response, "text", None):
        return {"risk_analysis": response.text}

    try:
        for c in response.candidates:
            for p in c.content.parts:
                if hasattr(p, "text"):
                    return {"risk_analysis": p.text}
    except Exception:
        pass

    return {"error": "Unable to analyze risks."}
