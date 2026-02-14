#sets up a prompt so that when the api calls summarizer it acts as a paraleagal and knows how gemini should answer the questions as

from google import genai

def summarize_contract(contract_text: str, client: genai.Client) -> str:
    if not contract_text or len(contract_text.strip()) < 20:
        return "Please provide a valid contract text (at least a few sentences)."

    prompt = f"""
    You are a legal paralegal.

    Summarize the following contract in simple English.
    Mention:
    - Duration
    - Payment terms
    - Termination conditions

    Contract:
    {contract_text}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",  # ✅ FREE TIER SAFE
        contents=prompt
    )

    if getattr(response, "text", None):
        return response.text

    try:
        for c in response.candidates:
            for p in c.content.parts:
                if hasattr(p, "text"):
                    return p.text
    except Exception:
        pass

    return "Unable to generate summary."
