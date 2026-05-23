import streamlit as st

def inject_custom_styles():
    """
    Injects custom styles for premium glassmorphic typography and timeline widgets.
    """
    st.markdown("""
<style>
    /* Global Styling */
    .main {
        background-color: #0f111a;
        color: #e3e6f3;
    }
    
    /* Header Gradient and Sleek Style */
    .title-banner {
        background: linear-gradient(135deg, #1e2640 0%, #111827 100%);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid #2d3748;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        margin-bottom: 2rem;
        text-align: center;
    }
    .title-banner h1 {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        margin: 0 0 10px 0;
        letter-spacing: -1px;
    }
    .title-banner p {
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 1.25rem;
        font-weight: 400;
        margin: 0;
    }
    
    /* Styled Glass Cards */
    .glass-card {
        background: rgba(128, 128, 128, 0.08);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Dual Column Layout Card Heads */
    .pros-card {
        border-left: 5px solid #10b981;
        background: rgba(16, 185, 129, 0.08);
        padding: 1.2rem;
        border-radius: 8px;
        height: 100%;
    }
    .cons-card {
        border-left: 5px solid #ef4444;
        background: rgba(239, 68, 68, 0.08);
        padding: 1.2rem;
        border-radius: 8px;
        height: 100%;
    }
    
    /* Custom Timeline Styles */
    .timeline {
        border-left: 2px solid #6366f1;
        position: relative;
        padding-left: 30px;
        margin-left: 15px;
    }
    .timeline-item {
        margin-bottom: 30px;
        position: relative;
    }
    .timeline-marker {
        position: absolute;
        top: 0px;
        left: -38px;
        background: #6366f1;
        border: 4px solid #888888;
        border-radius: 50%;
        width: 16px;
        height: 16px;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
    }
    .timeline-content {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 12px;
        padding: 1.25rem;
    }
    .timeline-date {
        font-weight: 700;
        color: #a855f7;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .timeline-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .timeline-desc {
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Forecast Grid Colors */
    .forecast-card-short {
        background: rgba(59, 130, 246, 0.08);
        border-top: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1.2rem;
        height: 100%;
    }
    .forecast-card-medium {
        background: rgba(168, 85, 247, 0.08);
        border-top: 4px solid #a855f7;
        border-radius: 8px;
        padding: 1.2rem;
        height: 100%;
    }
    .forecast-card-long {
        background: rgba(236, 72, 153, 0.08);
        border-top: 4px solid #ec4899;
        border-radius: 8px;
        padding: 1.2rem;
        height: 100%;
    }
    .readiness-card {
        background: rgba(245, 158, 11, 0.08);
        border-left: 5px solid #f59e0b;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)
