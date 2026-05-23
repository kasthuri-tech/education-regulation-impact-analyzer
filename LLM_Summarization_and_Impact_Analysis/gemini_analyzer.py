import os
import json
import google.generativeai as genai
from Gemini_Model_Integration_and_Testing.mock_data import get_mock_analysis

def validate_gemini_api_key(api_key):
    if not api_key:
        return False
    if not api_key.startswith("AIzaSy"):
        return False
    if len(api_key) < 30:
        return False
    return True

def analyze_regulation(text, api_key=None, pdf_bytes=None):
    resolved_api_key = api_key or os.environ.get("GEMINI_API_KEY")
    
    if not resolved_api_key or resolved_api_key.strip() == "" or resolved_api_key.strip().upper() == "MOCK":
        if pdf_bytes:
            raise ValueError("Analyzing custom scanned PDFs requires a valid Gemini API Key to run live OCR. Please enter a key in the sidebar.")
        return get_mock_analysis(text)

    if not validate_gemini_api_key(resolved_api_key.strip()):
        raise ValueError("Invalid Gemini API Key format. A valid key must start with 'AIzaSy' and be at least 30 characters.")

    try:
        genai.configure(api_key=resolved_api_key.strip())
    except Exception as e:
        raise ValueError(f"Failed to configure Gemini API: {str(e)}")
    
    prompt = """
You are an expert Education Policy Analyst and Compliance Officer. 
Analyze the provided official education regulation, circular, notification, or guideline document.
Your objective is to dissect this document and generate a comprehensive, highly accurate analysis.

Please return your response in EXACT JSON format with the following keys. Do not include any markdown styling, code block wrappers (like ```json), or trailing commas. It must be directly parseable as a JSON object.

Required JSON Structure:
{
  "document_title": "Clean, official-sounding title of the regulation",
  "category": "One of: Accreditation, Scholarship, Curriculum, Faculty Policy, Examination, Admissions, Institutional Governance, or General circular",
  "sentiment": "One of: High Compliance Workload, Flexible & Favorable, Operationally Disruptive, Academic Freedom Enhancing, Neutral/Procedural",
  "layman_summary": [
    "A concise 10-20 line bulleted summary explaining exactly what the regulation changes, why it is introduced, and what it means for average readers in plain language."
  ],
  "stakeholders": {
    "students": {
      "positives": ["Bullet point list of benefits, scholarship opportunities, or freedoms for students"],
      "negatives": ["Bullet point list of restrictions, compliance requirements, or challenges for students"],
      "opportunities": ["Bullet point list of new avenues for learning, flexibility, or savings"]
    },
    "faculty": {
      "positives": ["Benefits for professors, teaching assistants, or researchers"],
      "negatives": ["Increased teaching load, mandatory certifications, or paperwork constraints"],
      "opportunities": ["Professional development, research grants, or leadership pathways"]
    },
    "institutions": {
      "positives": ["Reputational upgrades, streamlined processes, or financial support"],
      "negatives": ["Strict operational timelines, penalty clauses, or technological requirements"],
      "opportunities": ["New program launches, corporate partnerships, or expansion models"]
    },
    "compliance_accreditation": {
      "positives": ["Clarity in ranking procedures, automated credit systems, or audits"],
      "negatives": ["Excessive documentation workload, short filing deadlines, or heavy compliance audits"],
      "opportunities": ["Digital transparency, NAAC/NIRF alignment, or standardized benchmarking"]
    }
  },
  "chronology": [
    {
      "event": "Predecessor circular, related amendment, historical committee recommendation, or milestone mentioned or inferred from the text",
      "date": "Approximate date or year (e.g. 'July 2020' or '2020')",
      "context": "How it connects to this current regulation"
    }
  ],
  "impact_forecast": {
    "short_term": ["Actionable steps or changes occurring in the first 0-1 year (e.g., registrations, setup)"],
    "medium_term": ["Changes occurring in 1-5 years (e.g., changes in graduation rates, curricula updates)"],
    "long_term": ["Long-term impacts after 5+ years (e.g., systemic transformation of institutions, quality improvement)"],
    "risks_and_readiness": ["Unintended consequences, major implementation risks, resource constraints, or capacity gaps that could fail the implementation"]
  }
}
"""

    if not pdf_bytes:
        prompt_with_text = f"{prompt}\n\nDocument Content to Analyze:\n\"\"\"\n{text}\n\"\"\""

    try:
        generation_config = {
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
        
        if pdf_bytes:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(pdf_bytes)
                tmp_path = tmp.name
                
            try:
                uploaded_file = genai.upload_file(path=tmp_path, mime_type="application/pdf")
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(
                    [uploaded_file, prompt],
                    generation_config=generation_config
                )
                try:
                    uploaded_file.delete()
                except Exception:
                    pass
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        else:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(
                    prompt_with_text,
                    generation_config=generation_config
                )
            except Exception as primary_err:
                if "not found" in str(primary_err).lower() or "not supported" in str(primary_err).lower():
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt_with_text)
                else:
                    raise primary_err
        
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()
        
        parsed_json = json.loads(raw_text)
        return parsed_json
        
    except json.JSONDecodeError as je:
        raise ValueError(f"Failed to parse AI response as valid JSON: {str(je)}\nRaw AI output: {response.text}")
    except Exception as e:
        raise ValueError(f"Gemini API generation failed. Please verify your API key and network connection: {str(e)}")
