import streamlit as st

def render_stakeholder_impact_tab(data):
    """
    Renders Tab 2: Stakeholder Impact Mapping.
    """
    st.markdown("### Interactive Stakeholder Impact Mapping")
    st.write("Understand how different institutional roles will be influenced by this regulation.")
    
    sh = data.get("stakeholders", {})
    
    roles = [
        ("Students & Learners", sh.get("students", {})),
        ("Academic Faculty & Researchers", sh.get("faculty", {})),
        ("Institutions, Administrators & Deans", sh.get("institutions", {})),
        ("Accreditation & Compliance Teams", sh.get("compliance_accreditation", {}))
    ]
    
    for role_name, role_data in roles:
        st.markdown(f"#### {role_name}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("Benefits & Protections")
            for p in role_data.get("positives", ["No specific benefits listed."]):
                st.write(f"- {p}")
        with col2:
            st.warning("Constraints & Requirements")
            for n in role_data.get("negatives", ["No specific constraints listed."]):
                st.write(f"- {n}")
        with col3:
            st.success("Academic Avenues & Opportunities")
            for o in role_data.get("opportunities", ["No specific opportunities listed."]):
                st.write(f"- {o}")
        st.markdown("---")
