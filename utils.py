import os
import re
import json
import requests
import io
from bs4 import BeautifulSoup
import pypdf
import google.generativeai as genai
from mock_data import get_mock_analysis, SAMPLE_DOCUMENTS

# ==========================================
# 📋 Document Ingestion & Text Preprocessing
# ==========================================

def extract_text_from_pdf(file_file):
    """
    Extracts plain text from a PDF file-like object using pypdf.
    """
    try:
        reader = pypdf.PdfReader(file_file)
        text_content = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
        
        extracted = "\n".join(text_content).strip()
        if not extracted:
            raise ValueError("The uploaded PDF contains no indexable text layer (scanned image only).")
        return extracted
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")

def scrape_url_content(url):
    """
    Scrapes the main textual content from an official academic/regulation webpage.
    Supports both HTML web pages and direct PDF downloads.
    Clean up boilerplate like navbars, footers, etc.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Check if response content is a PDF
        content_type = response.headers.get('Content-Type', '').lower()
        if url.lower().endswith('.pdf') or 'application/pdf' in content_type:
            pdf_file = io.BytesIO(response.content)
            reader = pypdf.PdfReader(pdf_file)
            text_content = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
            
            cleaned_text = "\n".join(text_content).strip()
            if not cleaned_text:
                raise ValueError("The PDF document contains no indexable text layers (scanned image only).")
            return cleaned_text
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove navigation, script, style, footer elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        # Extract headings and paragraphs
        lines = []
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
            text = element.get_text().strip()
            if text:
                lines.append(text)
                
        cleaned_text = "\n\n".join(lines)
        
        # Clean extra whitespaces
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        return cleaned_text
    except Exception as e:
        raise ValueError(f"Error scraping URL: {str(e)}")

# ==========================================
# 🤖 Gemini API Integration & NLP Analytics
# ==========================================

def validate_gemini_api_key(api_key):
    """
    Validates the format of the Gemini API key.
    """
    if not api_key:
        return False
    # Google AI Studio API keys typically start with AIzaSy
    if not api_key.startswith("AIzaSy"):
        return False
    if len(api_key) < 30:
        return False
    return True

def analyze_regulation(text, api_key=None, pdf_bytes=None):
    """
    Performs AI-driven regulation analysis using Google Gemini API.
    Supports a robust offline mock fallback when api_key is "MOCK" or not provided,
    allowing the dashboard to be playtested instantly.
    If pdf_bytes is provided and api_key is active, performs multimodal PDF OCR processing.
    """
    # 1. Resolve API key
    resolved_api_key = api_key or os.environ.get("GEMINI_API_KEY")
    
    # 2. Intercept mock or empty key and return beautiful preloaded analysis instantly
    if not resolved_api_key or resolved_api_key.strip() == "" or resolved_api_key.strip().upper() == "MOCK":
        if pdf_bytes:
            raise ValueError("Analyzing custom scanned PDFs requires a valid Gemini API Key to run live OCR. Please enter a key in the sidebar.")
        return get_mock_analysis(text)

    # Validate key format
    if not validate_gemini_api_key(resolved_api_key.strip()):
        raise ValueError("Invalid Gemini API Key format. A valid key must start with 'AIzaSy' and be at least 30 characters.")

    # 3. Configure the Gemini API library
    try:
        genai.configure(api_key=resolved_api_key.strip())
    except Exception as e:
        raise ValueError(f"Failed to configure Gemini API: {str(e)}")
    
    # 4. Create structured prompt
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
                # Upload the PDF via the File API for visual multimodal parsing (handles scanned PDFs perfectly)
                uploaded_file = genai.upload_file(path=tmp_path, mime_type="application/pdf")
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(
                    [uploaded_file, prompt],
                    generation_config=generation_config
                )
                try:
                    uploaded_file.delete()
                except Exception:
                    pass  # Fail-silent if file delete API fails
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        else:
            # Try gemini-2.5-flash first (preferred for JSON mode)
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(
                    prompt_with_text,
                    generation_config=generation_config
                )
            except Exception as primary_err:
                # If the model is not found or unsupported, fallback to gemini-pro
                if "not found" in str(primary_err).lower() or "not supported" in str(primary_err).lower():
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt_with_text)
                else:
                    raise primary_err
        
        # Clean response string if there are wrappers
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

