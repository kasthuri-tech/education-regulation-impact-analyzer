import streamlit as st

def render_kpi_cards(data, extracted_text):
    """
    Renders the three high-level metric cards for Category, Tone, and Structural Density.
    """
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; border-bottom: 4px solid #3b82f6;">
            <p style="color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.2rem;">Document Category</p>
            <h3 style="color: #60a5fa; font-size: 1.4rem; margin:0;">{data.get('category', 'Accreditation')}</h3>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi_col2:
        sent = data.get('sentiment', 'Neutral')
        sent_color = "#38bdf8"
        if "disruptive" in sent.lower() or "workload" in sent.lower():
            sent_color = "#f87171"
        elif "favorable" in sent.lower() or "freedom" in sent.lower():
            sent_color = "#34d399"
        elif "neutral" in sent.lower():
            sent_color = "#fbbf24"
            
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; border-bottom: 4px solid {sent_color};">
            <p style="color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.2rem;">Compliance Tone</p>
            <h3 style="color: {sent_color}; font-size: 1.4rem; margin:0;">{sent}</h3>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi_col3:
        char_count = len(extracted_text)
        complexity = "Standard Complexity"
        complexity_color = "#38bdf8"
        if char_count > 5000:
            complexity = "High Complexity"
            complexity_color = "#f87171"
        elif char_count < 2000:
            complexity = "Low Complexity"
            complexity_color = "#34d399"
            
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; border-bottom: 4px solid {complexity_color};">
            <p style="color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.2rem;">Structural Density</p>
            <h3 style="color: {complexity_color}; font-size: 1.3rem; margin:0;">{complexity}</h3>
        </div>
        """, unsafe_allow_html=True)

def render_executive_summary_tab(data, extracted_text):
    """
    Renders Tab 1: Executive Summary.
    """
    st.markdown(f"### {data.get('document_title', 'Circular Analysis')}")
    
    # Render KPIs
    render_kpi_cards(data, extracted_text)
    
    # LLM Summarization Card
    st.markdown("#### LLM Summarization (Layman Summary)")
    summary_html = "".join([f"<li>{item}</li>" for item in data.get("layman_summary", [])])
    st.markdown(f"""
    <div class="glass-card" style="line-height: 1.6;">
        <ul style="padding-left: 1.2rem; margin: 0; color: inherit;">
            {summary_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Side-by-Side Pros and Cons
    st.markdown("#### High-Level Policy Balancing")
    pros_cols1, pros_cols2 = st.columns(2)
    
    sh = data.get("stakeholders", {})
    high_pros = []
    high_cons = []
    
    for key, val in sh.items():
        if isinstance(val, dict):
            high_pros.extend(val.get("positives", [])[:2])
            high_cons.extend(val.get("negatives", [])[:2])
            
    if not high_pros: high_pros = ["Benefits and structural flexibility improvements."]
    if not high_cons: high_cons = ["Paperwork workload and transition timeline concerns."]
    
    with pros_cols1:
        pros_list = "".join([f"<li>{item}</li>" for item in high_pros])
        st.markdown(f"""
        <div class="pros-card">
            <h4 style="color: #10b981; margin-top: 0;">Positives & Opportunities</h4>
            <ul style="padding-left: 1.2rem; color: inherit; font-size: 0.95rem;">
                {pros_list}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with pros_cols2:
        cons_list = "".join([f"<li>{item}</li>" for item in high_cons])
        st.markdown(f"""
        <div class="cons-card">
            <h4 style="color: #ef4444; margin-top: 0;">Constraints & Administrative Burdens</h4>
            <ul style="padding-left: 1.2rem; color: inherit; font-size: 0.95rem;">
                {cons_list}
            </ul>
        </div>
        """, unsafe_allow_html=True)
