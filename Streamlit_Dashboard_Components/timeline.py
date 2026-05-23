import streamlit as st

def render_policy_timeline_tab(data):
    """
    Renders Tab 3: Timeline & Chronology.
    """
    st.markdown("### Policy Evolution & Chronology")
    st.write("Tracks predecessor policies, related guidelines, amendments, and historical committees linked to this regulation.")
    
    chron = data.get("chronology", [])
    
    if not chron:
        st.info("No explicit historical predecessor timeline items were identified in this circular.")
        return
        
    timeline_html_items = []
    for item in chron:
        event_title = item.get("event", "Historical Policy Action")
        event_date = item.get("date", "Previous Period")
        event_ctx = item.get("context", "")
        
        item_html = f"""<div class="timeline-item">
<div class="timeline-marker"></div>
<div class="timeline-content">
<div class="timeline-date">{event_date}</div>
<div class="timeline-title">{event_title}</div>
<div class="timeline-desc">{event_ctx}</div>
</div>
</div>"""
        timeline_html_items.append(item_html)
        
    full_timeline_html = f"""<div class="timeline">
{"".join(timeline_html_items)}
<div class="timeline-item">
<div class="timeline-marker" style="background: #10b981; box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);"></div>
<div class="timeline-content" style="border: 1px solid rgba(16, 185, 129, 0.3);">
<div class="timeline-date" style="color: #10b981;">CURRENT STATE</div>
<div class="timeline-title">{data.get('document_title', 'This Regulation')}</div>
<div class="timeline-desc">Fully operational and active under local compliance laws.</div>
</div>
</div>
</div>"""
    st.markdown(full_timeline_html, unsafe_allow_html=True)
