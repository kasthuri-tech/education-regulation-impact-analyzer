import streamlit as st
try:
    from gemini_analyzer import analyze_regulation
except ImportError:
    from LLM_Summarization_and_Impact_Analysis.gemini_analyzer import analyze_regulation

def render_comparison_tab(all_analyzed_documents, api_key_input):
    """
    Renders Tab 6: Multi-Document Comparison.
    """
    st.markdown("### Side-by-Side Regulation Comparison")
    st.write("Compare the compliance loads, stakeholder impacts, and implementation readiness of two regulations side-by-side.")
    
    col_comp1, col_comp2 = st.columns(2)
    with col_comp1:
        doc_a_choice = st.selectbox("Select Regulation A:", list(all_analyzed_documents.keys()), index=0, key="comp_select_a")
    with col_comp2:
        doc_b_choice = st.selectbox("Select Regulation B:", list(all_analyzed_documents.keys()), index=1 if len(all_analyzed_documents) > 1 else 0, key="comp_select_b")
        
    if st.button("Execute Side-by-Side Comparison", type="primary", use_container_width=True, key="comp_execute_btn"):
        text_a = all_analyzed_documents[doc_a_choice]
        text_b = all_analyzed_documents[doc_b_choice]
        
        with st.spinner("Comparing regulations..."):
            try:
                key_to_use = api_key_input.strip() if api_key_input.strip() else "MOCK"
                data_a = analyze_regulation(text_a, api_key=key_to_use)
                data_b = analyze_regulation(text_b, api_key=key_to_use)
                
                st.markdown("#### Structural Comparison Matrix")
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 5px solid #3b82f6; padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; color: inherit;">
                        <h4 style="margin: 0; color: #3b82f6;">Regulation A</h4>
                        <h3 style="margin: 0.5rem 0; color: inherit;">{data_a.get('document_title')}</h3>
                        <p><b>Category:</b> {data_a.get('category')}</p>
                        <p><b>Tone:</b> {data_a.get('sentiment')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 5px solid #10b981; padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; color: inherit;">
                        <h4 style="margin: 0; color: #10b981;">Regulation B</h4>
                        <h3 style="margin: 0.5rem 0; color: inherit;">{data_b.get('document_title')}</h3>
                        <p><b>Category:</b> {data_b.get('category')}</p>
                        <p><b>Tone:</b> {data_b.get('sentiment')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.info("A: Layman Directives Summary")
                    for item in data_a.get('layman_summary', []):
                        st.write(f"- {item}")
                with col_s2:
                    st.success("B: Layman Directives Summary")
                    for item in data_b.get('layman_summary', []):
                        st.write(f"- {item}")
                        
                st.markdown("#### Stakeholder Impact (Students & Faculty)")
                col_sh1, col_sh2 = st.columns(2)
                with col_sh1:
                    st.markdown("##### **Regulation A**")
                    st.write("**Students Positives:**")
                    for item in data_a.get('stakeholders', {}).get('students', {}).get('positives', []):
                        st.write(f"- {item}")
                    st.write("**Faculty Negatives:**")
                    for item in data_a.get('stakeholders', {}).get('faculty', {}).get('negatives', []):
                        st.write(f"- {item}")
                with col_sh2:
                    st.markdown("##### **Regulation B**")
                    st.write("**Students Positives:**")
                    for item in data_b.get('stakeholders', {}).get('students', {}).get('positives', []):
                        st.write(f"- {item}")
                    st.write("**Faculty Negatives:**")
                    for item in data_b.get('stakeholders', {}).get('faculty', {}).get('negatives', []):
                        st.write(f"- {item}")
                        
                st.markdown("#### Short-Term Action Horizon Forecast")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    st.warning("A: Short-Term Actions Required")
                    for item in data_a.get('impact_forecast', {}).get('short_term', []):
                        st.write(f"- {item}")
                with col_f2:
                    st.warning("B: Short-Term Actions Required")
                    for item in data_b.get('impact_forecast', {}).get('short_term', []):
                        st.write(f"- {item}")
                        
            except Exception as e:
                st.error(f"Error executing comparison: {e}")
