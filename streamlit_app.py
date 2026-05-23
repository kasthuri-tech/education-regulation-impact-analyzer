import streamlit as st
import os
from Document_Ingestion_and_Preprocessing.data_extractor import extract_text_from_pdf, scrape_url_content
from LLM_Summarization_and_Impact_Analysis.gemini_analyzer import analyze_regulation, validate_gemini_api_key
from Gemini_Model_Integration_and_Testing.mock_data import SAMPLE_DOCUMENTS
from Streamlit_Dashboard_Components import (
    render_executive_summary_tab,
    render_stakeholder_impact_tab,
    render_policy_timeline_tab,
    render_forecast_and_readiness_tab,
    render_export_report_tab,
    render_comparison_tab,
    inject_custom_styles
)

# Set page configuration with a premium title and icon
st.set_page_config(
    page_title="ERIA | Education Regulation Impact Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS styles from components package
inject_custom_styles()

# ==========================================
# 🏠 Session State Initialization
# ==========================================
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "doc_title" not in st.session_state:
    st.session_state.doc_title = ""
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "all_analyzed_documents" not in st.session_state:
    st.session_state.all_analyzed_documents = {}
    for k, v in SAMPLE_DOCUMENTS.items():
        st.session_state.all_analyzed_documents[k] = v


# ==========================================
# 🏛️ Header / Hero Banner
# ==========================================
st.markdown("""
<div class="title-banner">
    <h1>Education Regulation Impact Analyzer (ERIA)</h1>
    <p>Simplifying complex educational circulars, regulations, and accreditation rules into clear, actionable institutional intelligence</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 🛠️ Sidebar Configuration & Inputs
# ==========================================
with st.sidebar:
    st.markdown("### API & Model Configuration")
    
    # 1. API Key Input
    api_key_input = st.text_input(
        "Gemini API Key", 
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Obtain a key from Google AI Studio: https://aistudio.google.com/"
    )
    
    # 1b. Test API Key Block
    if api_key_input.strip() and api_key_input.strip().upper() != "MOCK":
        if st.button("Test API Connection", use_container_width=True):
            if not validate_gemini_api_key(api_key_input.strip()):
                st.error("❌ Invalid Key Format. Must start with 'AIzaSy' and be at least 30 characters.")
            else:
                with st.spinner("Testing API connection..."):
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=api_key_input.strip())
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        response = model.generate_content("Respond with only 'OK'")

                        if "OK" in response.text.upper():
                            st.success("✅ Connection Successful! Ready for live analysis.")
                        else:
                            st.warning(f"⚠️ Unexpected response: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Connection Failed: {str(e)}")
                        try:
                            available_models = [m.name for m in genai.list_models()]
                            st.info(f"📋 Available models for this key: {available_models}")
                        except Exception as list_err:
                            st.warning("💡 Pro-Tip: Ensure your key is created via AI Studio (aistudio.google.com) and the 'Generative Language API' is enabled.")

                        
    st.markdown("---")
    st.markdown("### Document Ingestion")
    
    # 2. Input Method selection
    input_method = st.radio(
        "Choose Input Source:",
        ["Select Preloaded Demo", "Upload PDF Circular", "Scrape UGC / Academic URL", "Paste Text Manually"]
    )
    
    if input_method == "Select Preloaded Demo":
        demo_choice = st.selectbox("Choose a Demo Circular:", list(SAMPLE_DOCUMENTS.keys()))
        if st.button("Load Preloaded Demo"):
            st.session_state.extracted_text = SAMPLE_DOCUMENTS[demo_choice]
            st.session_state.doc_title = demo_choice
            st.session_state.analysis_results = None
            st.session_state.pdf_bytes = None
            st.success(f"Loaded: {demo_choice}")
            
    elif input_method == "Upload PDF Circular":
        uploaded_file = st.file_uploader("Upload Regulation PDF file:", type=["pdf"])
        if uploaded_file is not None:
            if st.session_state.doc_title != uploaded_file.name:
                with st.spinner("Extracting text from uploaded PDF..."):
                    try:
                        extracted = extract_text_from_pdf(uploaded_file)
                        st.session_state.extracted_text = extracted
                        st.session_state.pdf_bytes = None
                        st.session_state.doc_title = uploaded_file.name
                        st.session_state.analysis_results = None
                        st.success(f"Successfully extracted text from: {uploaded_file.name}!")
                    except Exception as e:
                        # Scanned PDF or layout issue -> capture bytes for multimodal Gemini API OCR
                        st.session_state.pdf_bytes = uploaded_file.getvalue()
                        st.session_state.extracted_text = "[Scanned PDF Circular Loaded - Local plain-text extraction is empty. Live Gemini OCR will process this multimodal PDF directly upon hitting 'Analyze']"
                        st.session_state.doc_title = uploaded_file.name
                        st.session_state.analysis_results = None
                        st.warning("⚠️ Scanned PDF detected (no plain text layer found). We will upload this document directly to Google Gemini for visual multimodal OCR during analysis.")
                        
    elif input_method == "Scrape UGC / Academic URL":
        url_input = st.text_input("Paste Official Circular URL (e.g. UGC, AICTE):", placeholder="https://www.ugc.gov.in/...")
        if st.button("Fetch URL Content"):
            if url_input.strip() == "":
                st.warning("Please paste a valid URL.")
            else:
                with st.spinner("Fetching and scraping URL content..."):
                    try:
                        scraped = scrape_url_content(url_input)
                        st.session_state.extracted_text = scraped
                        st.session_state.pdf_bytes = None
                        st.session_state.doc_title = url_input.split('/')[-1] or "Scraped URL Document"
                        st.session_state.analysis_results = None
                        st.success("Successfully fetched URL content!")
                    except Exception as e:
                        st.error(f"Failed to scrape webpage: {e}")
                        
    elif input_method == "Paste Text Manually":
        manual_title = st.text_input("Document Title:", placeholder="e.g. UGC Guidelines Amendment")
        manual_text = st.text_area("Paste text here:", height=200)
        if st.button("Load Custom Text"):
            if manual_text.strip() == "":
                st.warning("Please paste some text.")
            else:
                st.session_state.extracted_text = manual_text
                st.session_state.pdf_bytes = None
                st.session_state.doc_title = manual_title or "Custom Manual Text"
                st.session_state.analysis_results = None
                st.success("Custom text loaded!")


    st.markdown("---")
    st.info("ERIA helps administrators, professors, and students quickly extract regulatory compliance metrics, timeline changes, and impacts from legal education documents.")

# ==========================================
# 📊 Main Dashboard Logic
# ==========================================

# If no text is loaded yet, show a clean onboarding screen
if not st.session_state.extracted_text:
    st.markdown("""
    <div class="glass-card">
        <h3>Welcome to ERIA!</h3>
        <p>To begin analyzing university circulars and guidelines, choose an ingestion option in the sidebar:</p>
        <ul>
            <li><b>Select Preloaded Demo:</b> Quick, instant trial with realistic UGC regulations (No upload required!).</li>
            <li><b>Upload PDF Circular:</b> Direct parsing of official PDF policy booklets.</li>
            <li><b>Scrape URL:</b> Automatically scrape text from academic notifications or university notices.</li>
            <li><b>Paste Text:</b> Copy and paste specific sections of raw policy articles directly.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 200px;">
            <h4 style="color: #6366f1;">Policy Classification</h4>
            <p style="font-size: 0.95rem; color: inherit;">Instantly categorizes documents (Accreditation, Scholarship, Syllabus reforms) and ranks complexity.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 200px;">
            <h4 style="color: #a855f7;">Stakeholder Mapping</h4>
            <p style="font-size: 0.95rem; color: inherit;">Translates heavy bureaucratic legal terms into clear positives, negatives, and opportunities.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 200px;">
            <h4 style="color: #ec4899;">Impact Forecasting</h4>
            <p style="font-size: 0.95rem; color: inherit;">Outlines timelines, predecessor changes, and schedules short-term vs long-term workloads.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.subheader(f"Active Document: {st.session_state.doc_title}")
    
    # Render preview of text
    with st.expander("View Raw Extracted Text Preview", expanded=False):
        st.code(st.session_state.extracted_text[:1200] + ("\n... [Truncated for preview]" if len(st.session_state.extracted_text) > 1200 else ""), language="text")
        st.caption(f"Total Character Count: {len(st.session_state.extracted_text)}")
        
    # Analyze trigger button
    col_btn, col_msg = st.columns([1, 3])
    with col_btn:
        if st.button("Analyze Regulation", type="primary", use_container_width=True):
            key_to_use = api_key_input.strip() if api_key_input.strip() else "MOCK"
            
            with st.spinner("Analyzing document with Gemini AI Engine..."):
                try:
                    results = analyze_regulation(
                        st.session_state.extracted_text, 
                        api_key=key_to_use, 
                        pdf_bytes=st.session_state.pdf_bytes
                    )
                    st.session_state.analysis_results = results
                    
                    # Dynamically store analyzed custom text to compare it side-by-side
                    resolved_name = results.get("document_title", st.session_state.doc_title)
                    st.session_state.all_analyzed_documents[resolved_name] = st.session_state.extracted_text
                    st.balloons()
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
                        
    with col_msg:
        if st.session_state.analysis_results is None:
            st.info("Pro-Tip: Click 'Analyze Regulation' to instantly load High-Fidelity Sandbox Mode!")
        else:
            if not api_key_input.strip() or api_key_input.strip().upper() == "MOCK":
                st.info("Running in High-Fidelity Sandbox Mode. Enter a Gemini API Key in the sidebar to switch to live document analysis.")
            else:
                st.success("Analysis complete! View the results in the tabs below.")

    # Show results if available
    if st.session_state.analysis_results is not None:
        data = st.session_state.analysis_results
        
        # Tabbed Dashboard Views
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Executive Summary", 
            "Stakeholder Impact", 
            "Policy Timeline", 
            "Multi-Horizon Impact Forecast & Risk Readiness Index",
            "Export Report",
            "Compare Regulations (Optional)"
        ])
        
        with tab1:
            render_executive_summary_tab(data, st.session_state.extracted_text)
            
        with tab2:
            render_stakeholder_impact_tab(data)
            
        with tab3:
            render_policy_timeline_tab(data)
            
        with tab4:
            render_forecast_and_readiness_tab(data)
            
        with tab5:
            render_export_report_tab(data, st.session_state.extracted_text, st.session_state.doc_title)
            
        with tab6:
            render_comparison_tab(st.session_state.all_analyzed_documents, api_key_input)
