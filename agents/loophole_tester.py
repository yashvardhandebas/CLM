"""
Loophole Tester / Stress Test Agent

This module provides contract stress testing functionality by simulating realistic breach scenarios.
It helps identify potential vulnerabilities and legal outcomes by testing how the contract would
hold up under different breach conditions (vendor breach, client breach, etc.).

The agent analyzes:
- Legal fault determination in breach scenarios
- Contract protection mechanisms
- Likely court outcomes
- Simple explanations of legal reasoning

This is useful for proactive risk assessment and understanding contract resilience.
"""
from google import genai
from google.genai.errors import ClientError


def stress_test_contract(contract_text: str, client: genai.Client) -> dict:
    """
    Simulates realistic breach scenarios to test contract resilience.

    Args:
        contract_text: The contract text to analyze
        client: The Gemini AI client instance

    Returns:
        Dictionary containing stress test analysis results
    """
    if not contract_text or len(contract_text.strip()) < 20:
        return {"error": "Please provide a valid contract text."}

    prompt = f"""
You are a legal risk simulation assistant.

Simulate 2 realistic breach scenarios based on the contract:
1. Vendor breach
2. Client breach

For each scenario, answer:
- Who is legally at fault?
- Who is protected by the contract?
- Who is likely to win in court?
- Why (in simple terms)

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
        return {"stress_test": response.text}

    try:
        for c in response.candidates:
            for p in c.content.parts:
                if hasattr(p, "text"):
                    return {"stress_test": p.text}
    except Exception:
        pass

    return {"error": "Unable to perform stress test analysis."}

