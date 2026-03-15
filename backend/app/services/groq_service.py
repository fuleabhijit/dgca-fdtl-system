import requests

GROQ_API_KEY = "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"
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.3-70b-versatile"   # current active model as of 2026


def explain_violation(violation_type: str, description: str, pilot_name: str = "the pilot") -> str:

    prompt = f"""
You are a DGCA aviation compliance officer. A flight duty time violation has been detected.

Pilot: {pilot_name}
Violation Type: {violation_type}
Details: {description}

In 3-4 sentences:
1. Explain what DGCA regulation was violated
2. Describe the safety risk this creates
3. Give a concrete corrective recommendation

Be direct and professional.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 300
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI explanation unavailable: {str(e)}"