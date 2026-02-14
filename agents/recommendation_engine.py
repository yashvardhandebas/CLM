"""
Recommendation Engine Agent

This module produces a final decision-support recommendation by synthesizing
all prior analyses: risk, legal intelligence, bias, stress test, and fraud indicators.
It outputs an overall risk level, fairness assessment, legal stability, and a clear
recommendation (Accept / Review Before Signing / Reject) with reasoning and next steps.

Does NOT provide legal advice; provides structured decision-support insights.
"""
from google import genai
from google.genai.errors import ClientError


def generate_recommendation(
    contract_text: str,
    risk_data: str,
    legal_data: str,
    bias_data: str,
    stress_test_data: str,
    fraud_data: str,
    client: genai.Client,
) -> dict:
    """
    Synthesizes all analysis outputs into a single recommendation.

    Uses the Gemini client to run a structured prompt that considers:
    - Risk analysis
    - Legal intelligence
    - Bias/fairness
    - Stress test results
    - Fraud indicators

    Returns a dict with key "final_recommendation" containing the model's
    structured text (risk level, fairness, stability, recommendation, reasoning, next steps).
    """
    # Build a single prompt that injects all prior analyses so the model can
    # produce one coherent recommendation (risk level, fairness, stability, accept/review/reject).
    prompt = f"""
You are a senior legal decision-support AI.

Based on the following analyses:

RISK ANALYSIS:
{risk_data}

LEGAL INTELLIGENCE:
{legal_data}

BIAS ANALYSIS:
{bias_data}

STRESS TEST RESULTS:
{stress_test_data}

FRAUD RISK INDICATORS:
{fraud_data}

Now provide:

1. Overall Risk Level (Low / Medium / High)
2. Contract Fairness (Client-Favored / Vendor-Favored / Balanced)
3. Legal Stability (Stable / Questionable / Weak)
4. Final Recommendation:
   - Accept
   - Review Before Signing
   - Reject
5. Clear bullet-point reasoning
6. Practical next steps

Keep the explanation professional and structured.
Do NOT provide legal advice. Provide decision-support insights.
"""

    # Call Gemini with the combined prompt; handle quota/API errors like other agents.
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
        )
    except ClientError as e:
        if "429" in str(e):
            return {"error": "AI quota exceeded. Please try again later."}
        return {"error": str(e)}

    # Extract text from response: prefer response.text, then fall back to
    # iterating candidates/parts (same pattern as other agents).
    text = getattr(response, "text", None)
    if text:
        return {"final_recommendation": text}

    try:
        for c in response.candidates:
            for p in c.content.parts:
                if hasattr(p, "text"):
                    return {"final_recommendation": p.text}
    except Exception:
        pass

    return {"error": "Unable to generate recommendation."}
