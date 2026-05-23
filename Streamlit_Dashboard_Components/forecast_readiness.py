import streamlit as st

def render_forecast_and_readiness_tab(data):
    """
    Renders Tab 4: Multi-Horizon Impact Forecast & Risk Readiness Index.
    """
    st.markdown("### Multi-Horizon Impact Forecast & Risk Readiness Index")
    st.write("Visual projections mapping how this regulation triggers immediate tasks and long-term evolutionary patterns.")
    
    fc = data.get("impact_forecast", {})
    col_fc1, col_fc2, col_fc3 = st.columns(3)
    
    with col_fc1:
        st.markdown("""
        <div class="forecast-card-short">
            <h4 style="color: #3b82f6; margin-top:0;">Short-Term Impact</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; font-weight: 700; margin-bottom: 0.5rem;">0–1 YEAR (Operational Setup)</p>
        """, unsafe_allow_html=True)
        for item in fc.get("short_term", ["Immediate compliance alignments."]):
            st.markdown(f"<div style='margin-bottom:0.4rem; font-size:0.92rem; color: inherit;'>• {item}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_fc2:
        st.markdown("""
        <div class="forecast-card-medium">
            <h4 style="color: #a855f7; margin-top:0;">Medium-Term Impact</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; font-weight: 700; margin-bottom: 0.5rem;">1–5 YEARS (Structural Evolution)</p>
        """, unsafe_allow_html=True)
        for item in fc.get("medium_term", ["Curricula standard adjustments."]):
            st.markdown(f"<div style='margin-bottom:0.4rem; font-size:0.92rem; color: inherit;'>• {item}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_fc3:
        st.markdown("""
        <div class="forecast-card-long">
            <h4 style="color: #ec4899; margin-top:0;">Long-Term Impact</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; font-weight: 700; margin-bottom: 0.5rem;">5+ YEARS (Systemic Changes)</p>
        """, unsafe_allow_html=True)
        for item in fc.get("long_term", ["Macro-level educational reforms."]):
            st.markdown(f"<div style='margin-bottom:0.4rem; font-size:0.92rem; color: inherit;'>• {item}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Readiness and Risks Card
    st.markdown("""
    <div class="readiness-card">
        <h4 style="color: #f59e0b; margin-top: 0; display: flex; align-items: center;">
            Risks & Institutional Readiness Challenges
        </h4>
    """, unsafe_allow_html=True)
    for item in fc.get("risks_and_readiness", ["Infrastructure capability gaps and teacher administrative fatigue."]):
        st.markdown(f"<div style='margin-bottom:0.5rem; font-size:0.95rem; color: inherit;'>• <b>{item}</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
