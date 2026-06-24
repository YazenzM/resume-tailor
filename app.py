import streamlit as st
import markdown
import difflib
import os
from weasyprint import HTML
from database import init_db, add_application, get_applications, update_status

# Initialize local database
init_db()

st.set_page_config(layout="wide", page_title="AI Resume System")

# --- Custom Inline Diff Generator ---
def generate_inline_diff(old_text, new_text):
    """Compares two strings and returns HTML with red/green inline highlighting."""
    matcher = difflib.SequenceMatcher(None, old_text, new_text)
    html = "<div style='font-family: monospace; font-size: 14px; line-height: 1.5; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'>"
    
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == 'equal':
            html += old_text[a0:a1].replace('\n', '<br>')
        elif opcode == 'insert':
            html += f"<span style='background-color: #d4edda; color: #155724; font-weight: bold;'>{new_text[b0:b1].replace('\n', '<br>')}</span>"
        elif opcode == 'delete':
            html += f"<span style='background-color: #f8d7da; color: #721c24; text-decoration: line-through;'>{old_text[a0:a1].replace('\n', '<br>')}</span>"
        elif opcode == 'replace':
            html += f"<span style='background-color: #f8d7da; color: #721c24; text-decoration: line-through;'>{old_text[a0:a1].replace('\n', '<br>')}</span>"
            html += f"<span style='background-color: #d4edda; color: #155724; font-weight: bold;'>{new_text[b0:b1].replace('\n', '<br>')}</span>"
            
    html += "</div>"
    return html

# --- Mock AI Function (Markdown Based) ---
def get_ai_tailored_resume(job_description):
    return [
        {
            "id": "edu_utd", "section": "Education", "keep": True, 
            "original_md": "**The University of Texas at Dallas**\n*M.S. Business Analytics and AI (Expected May 2026)*",
            "suggested_md": "**The University of Texas at Dallas**\n*M.S. Business Analytics and AI (Expected May 2026)*",
            "has_changes": False
        },
        {
            "id": "exp_zinzu", "section": "Experience", "keep": True, 
            "original_md": "**Data Engineer | Zinzu**\n*Current*\n* Develop and maintain backend scripts and data infrastructure to support core business operations.\n* Implement automated pipelines for data extraction, transformation, and loading.",
            "suggested_md": "**Data Engineer | Zinzu**\n*Current*\n* Architected scalable backend data infrastructure using Python to optimize core operations.\n* Implemented automated ETL pipelines for robust data extraction and loading.",
            "has_changes": True
        },
        {
            "id": "proj_ga4", "section": "Projects", "keep": True, 
            "original_md": "**GA4 Conversion Predictor**\n* Engineered BigQuery SQL and PySpark scripts to flatten GA4 event data, extracting geo.country parameters.\n* Built predictive models to forecast user conversion based on behavioral navigation paths.",
            "suggested_md": "**GA4 Conversion Predictor**\n* Engineered BigQuery SQL and PySpark workflows to flatten GA4 event data, specifically extracting geo.country.\n* Built predictive machine learning models to forecast user conversion via behavioral navigation paths.",
            "has_changes": True
        },
        {
            "id": "proj_cifar", "section": "Projects", "keep": False, 
            "original_md": "**CIFAR-10 Image Classification**\n* Implemented and evaluated Convolutional Neural Networks for image classification on the CIFAR-10 dataset.",
            "suggested_md": "**CIFAR-10 Image Classification**\n* Implemented and evaluated Convolutional Neural Networks for image classification on the CIFAR-10 dataset.",
            "has_changes": False
        }
    ]

st.title("Document Tailor & Pipeline System")

# Create top-level tabs for the application
tab_editor, tab_tracker = st.tabs(["✏️ Document Editor", "📊 Application Tracker"])

# ==========================================
# TAB 1: THE EDITOR
# ==========================================
with tab_editor:
    st.subheader("1. Analyze Job Description")
    job_desc = st.text_area("Paste the job description here:", height=100, label_visibility="collapsed", placeholder="Paste job description...")

    if st.button("Generate Tailored Draft", type="primary"):
        with st.spinner("Analyzing and adapting profile..."):
            st.session_state['resume_data'] = get_ai_tailored_resume(job_desc)
            st.session_state['active_job_desc'] = job_desc

    st.sidebar.subheader("Document Layout")
    font_size = st.sidebar.slider("Base Font Size (pt)", 8.0, 12.0, 10.0, 0.5)
    margin_size = st.sidebar.slider("Page Margins (mm)", 8, 25, 15, 1)

    compiled_markdown = "# Yaseen Mohammed\n\nRichardson, TX | Data Engineer | M.S. Business Analytics & AI\n\n"

    if 'resume_data' in st.session_state:
        st.write("---")
        st.subheader("2. Interactive Document Editor")
        
        edit_col, preview_col = st.columns([1.2, 1])
        
        with edit_col:
            current_section = ""
            
            for idx, block in enumerate(st.session_state['resume_data']):
                if block['section'] != current_section:
                    current_section = block['section']
                    st.markdown(f"<h3 style='color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-top: 20px;'>{current_section}</h3>", unsafe_allow_html=True)
                
                with st.container():
                    toggle_col, empty_col = st.columns([1, 4])
                    with toggle_col:
                        block['keep'] = st.toggle("Include in resume", value=block['keep'], key=f"keep_{idx}")
                    
                    if block['has_changes']:
                        with st.expander("🔍 View AI Edits (Original vs Suggested)", expanded=True):
                            diff_html = generate_inline_diff(block['original_md'], block['suggested_md'])
                            st.markdown(diff_html, unsafe_allow_html=True)
                    
                    line_count = len(block['suggested_md'].split('\n'))
                    box_height = max(100, line_count * 25)
                    
                    block['suggested_md'] = st.text_area(
                        "Editor", 
                        value=block['suggested_md'], 
                        key=f"edit_{idx}", 
                        height=box_height,
                        label_visibility="collapsed"
                    )
                    st.write("")
                    
                if block['keep']:
                    compiled_markdown += f"{block['suggested_md']}\n\n"

        with preview_col:
            st.markdown("""
                <style>
                    div[data-testid="column"]:nth-of-type(2) {
                        position: sticky;
                        top: 3rem;
                    }
                </style>
            """, unsafe_allow_html=True)
            
            html_body = markdown.markdown(compiled_markdown)
            print_css = f"""
            <style>
                @page {{ size: Letter; margin: {margin_size}mm; }}
                body {{
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    font-size: {font_size}pt;
                    color: #333333; line-height: 1.35; background-color: white;
                }}
                h1 {{ font-size: {font_size * 2.2}pt; text-align: center; margin-top: 0; margin-bottom: 2px; color: #2c3e50; }}
                h2 {{ font-size: {font_size * 1.3}pt; border-bottom: 2px solid #2c3e50; margin-top: 14px; margin-bottom: 6px; }}
                ul {{ margin: 0; padding-left: 18px; }}
                li {{ margin-bottom: 3px; }}
            </style>
            """
            
            full_preview_html = f"<html><head>{print_css}</head><body>{html_body}</body></html>"
            st.components.v1.html(full_preview_html, height=750, scrolling=True)
            
            st.divider()
            c1, c2 = st.columns(2)
            with c1: target_company = st.text_input("Company", value="Target_Company")
            with c2: target_role = st.text_input("Role", value="Target_Role")
            
            if st.button("Export to PDF & Log Application", use_container_width=True, type="primary"):
                os.makedirs("resume_outputs", exist_ok=True)
                filename = f"{target_company}_{target_role}_Resume.pdf".replace(" ", "_")
                pdf_path = os.path.join("resume_outputs", filename)
                
                # Compile PDF
                HTML(string=full_preview_html).write_pdf(pdf_path)
                
                # Log to DB
                job_desc_to_log = st.session_state.get('active_job_desc', 'No description provided')
                add_application(target_company, target_role, pdf_path, job_desc_to_log)
                
                st.success(f"Generated {filename} and logged to tracker!")
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF", data=f, file_name=filename, mime="application/pdf", use_container_width=True)

# ==========================================
# TAB 2: THE TRACKER
# ==========================================
with tab_tracker:
    st.subheader("Your Application Pipeline")
    apps = get_applications()
    
    if not apps:
        st.info("No applications logged yet. Go to the Editor tab to generate a resume and save your first application.")
    else:
        for app in apps:
            app_id, company_name, role_title, status, date_applied, path = app
            
            with st.expander(f"**{company_name}** — {role_title} | Applied: {date_applied}", expanded=False):
                st.write(f"📁 **Resume Path:** `{path}`")
                
                statuses = ["Draft", "Applied", "Interviewing", "Offer", "Rejected"]
                try:
                    current_idx = statuses.index(status)
                except ValueError:
                    current_idx = 1
                    
                new_status = st.selectbox(
                    "Update Application Status:", 
                    statuses, 
                    index=current_idx, 
                    key=f"status_{app_id}"
                )
                
                if new_status != status:
                    update_status(app_id, new_status)
                    st.success(f"Status for {company_name} updated to {new_status}!")
                    st.rerun()