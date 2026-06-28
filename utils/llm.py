import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
MODEL = "meta-llama/llama-3.1-8b-instruct"

def analyze_code(code):
    prompt = (
        "You are an expert code reviewer and bug detector.\n\n"
        "Analyze the following code carefully and identify ALL bugs, errors, and issues.\n\n"
        "For each bug found, provide:\n"
        "1. A short title (max 10 words)\n"
        "2. Severity: Critical / High / Medium / Low\n"
        "3. Category: Logic Error / Syntax Error / Runtime Error / Security Issue / Performance Issue\n"
        "4. Description of the bug\n"
        "5. The specific line or section with the bug\n"
        "6. A suggested fix\n\n"
        "Return your response as a valid JSON object like this:\n"
        '{"bugs_found": true, "bug_count": 2, "bugs": [{"title": "Short title", '
        '"severity": "High", "category": "Logic Error", "description": "Detailed description", '
        '"code_snippet": "problematic line", "suggested_fix": "How to fix it"}], '
        '"overall_summary": "Brief summary"}\n\n'
        "If no bugs are found return:\n"
        '{"bugs_found": false, "bug_count": 0, "bugs": [], "overall_summary": "No bugs found."}\n\n'
        "IMPORTANT: Return ONLY the JSON object. No extra text, no markdown.\n\n"
        "Code to analyze:\n"
        + code
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.1
    }

    try:
        response = requests.post(API_URL, headers=headers, json=body, timeout=60)
        response.raise_for_status()

        result = response.json()
        text = result["choices"][0]["message"]["content"].strip()

        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        parsed = json.loads(text)
        return parsed

    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to HuggingFace API. Check your internet."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"API error: {e.response.status_code} — check your HF token"}
    except json.JSONDecodeError:
        return {"error": f"Could not parse response: {text[:200]}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}