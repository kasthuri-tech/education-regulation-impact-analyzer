import streamlit as st
import re
import os

def render_export_report_tab(data, extracted_text, doc_title):
    """
    Renders Tab 5: Export Report.
    """
    st.markdown("### Downloadable Regulatory Compliance Report")
    st.write("Generate and download a beautifully structured markdown report of the policy analysis.")
    
    sh = data.get("stakeholders", {})
    chron = data.get("chronology", [])
    fc = data.get("impact_forecast", {})
    
    # Build markdown document content
    markdown_content = f"""# Regulatory Impact Report: {data.get('document_title', doc_title)}

## Document Executive Summary
* **Category:** {data.get('category', 'Education Policy')}
* **Compliance Tone:** {data.get('sentiment', 'Neutral')}
* **Length/Density:** {len(extracted_text)} characters

## LLM Summarization
{chr(10).join([f"* {item}" for item in data.get('layman_summary', [])])}

---

## Stakeholder Impact Report
### 1. Students & Learners
* **Benefits:** {", ".join(sh.get('students', {}).get('positives', []))}
* **Constraints:** {", ".join(sh.get('students', {}).get('negatives', []))}
* **Opportunities:** {", ".join(sh.get('students', {}).get('opportunities', []))}

### 2. Faculty & Teachers
* **Benefits:** {", ".join(sh.get('faculty', {}).get('positives', []))}
* **Constraints:** {", ".join(sh.get('faculty', {}).get('negatives', []))}
* **Opportunities:** {", ".join(sh.get('faculty', {}).get('opportunities', []))}

### 3. Institutions & Administrators
* **Benefits:** {", ".join(sh.get('institutions', {}).get('positives', []))}
* **Constraints:** {", ".join(sh.get('institutions', {}).get('negatives', []))}
* **Opportunities:** {", ".join(sh.get('institutions', {}).get('opportunities', []))}

### 4. Accreditation & Compliance Teams
* **Benefits:** {", ".join(sh.get('compliance_accreditation', {}).get('positives', []))}
* **Constraints:** {", ".join(sh.get('compliance_accreditation', {}).get('negatives', []))}
* **Opportunities:** {", ".join(sh.get('compliance_accreditation', {}).get('opportunities', []))}

---

## Policy Timeline & Predecessor Chronology
{chr(10).join([f"* **{item.get('date', 'Previous')}**: {item.get('event', '')} - {item.get('context', '')}" for item in chron])}

---

## Time-Horizon Impact Forecast
* **Short-Term (0-1 year):** {", ".join(fc.get('short_term', []))}
* **Medium-Term (1-5 years):** {", ".join(fc.get('medium_term', []))}
* **Long-Term (>5 years):** {", ".join(fc.get('long_term', []))}

### Identified Implementation Risks & Readiness Issues
{chr(10).join([f"* {item}" for item in fc.get('risks_and_readiness', [])])}

---
*Report generated automatically by ERIA (Education Regulation Impact Analyzer) on behalf of {doc_title}*
"""
    
    # Sanitize the document title for a safe, browser-compliant filename
    safe_title = re.sub(r'[^a-zA-Z0-9]', '_', doc_title)
    safe_title = re.sub(r'_{2,}', '_', safe_title).strip('_')
    safe_title = safe_title[:30]
    if not safe_title:
        safe_title = "Document"
        
    # File Preview
    with st.expander("Preview Markdown Compliance Report", expanded=True):
        st.markdown(markdown_content)
        
    # Dual-Format Download Buttons
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="Download Compliance Report (.md)",
            data=markdown_content,
            file_name=f"ERIA_Report_{safe_title}.md",
            mime="text/plain",
            use_container_width=True
        )
    with col_dl2:
        st.download_button(
            label="Download as Text File (.txt)",
            data=markdown_content,
            file_name=f"ERIA_Report_{safe_title}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
    st.markdown("---")
    st.markdown("### Direct Local Machine Export (Bypasses Browser Security Blocks)")
    st.write("If your browser's security/SmartScreen policies block downloads from localhost, use these buttons to save directly to disk.")
    
    col_local1, col_local2 = st.columns(2)
    with col_local1:
        if st.button("Save directly to Windows Downloads Folder", use_container_width=True, key="save_dl_folder_btn"):
            try:
                downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                os.makedirs(downloads_folder, exist_ok=True)
                
                path_md = os.path.join(downloads_folder, f"ERIA_Report_{safe_title}.md")
                path_txt = os.path.join(downloads_folder, f"ERIA_Report_{safe_title}.txt")
                
                with open(path_md, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                with open(path_txt, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                    
                st.success(f"Saved directly to Downloads folder:\n* ERIA_Report_{safe_title}.md\n* ERIA_Report_{safe_title}.txt")
            except Exception as e:
                st.error(f"Failed to write locally: {e}")
                
    with col_local2:
        if st.button("Save directly to Project 'Generated_Reports/'", use_container_width=True, key="save_workspace_btn"):
            try:
                workspace_folder = os.path.join(os.getcwd(), "Generated_Reports")
                os.makedirs(workspace_folder, exist_ok=True)
                
                path_md = os.path.join(workspace_folder, f"ERIA_Report_{safe_title}.md")
                path_txt = os.path.join(workspace_folder, f"ERIA_Report_{safe_title}.txt")
                
                with open(path_md, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                with open(path_txt, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                    
                st.success(f"Reports written to your project directory Generated_Reports/.")
            except Exception as e:
                st.error(f"Failed to write locally: {e}")
