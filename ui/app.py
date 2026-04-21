"""
Streamlit Dashboard — AI Resume Shortlister UI

A premium dark-themed dashboard that communicates with the FastAPI backend.
Features:
    - Upload multiple resume PDFs
    - Enter/paste job description
    - Process and view ranked candidates
    - View detailed candidate info (skills, scores, keywords)
    - Download results as CSV
    - Cleanup temporary files

Run with:
    streamlit run ui/app.py --server.port 8501
"""

import streamlit as st
import requests
import pandas as pd
import time

# ─── Configuration ─────────────────────────────────────────────
API_BASE = "http://localhost:8000"

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Shortlister",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS for Premium Dark Theme ─────────────────────────
st.markdown("""
<style>
    /* ── Import Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .hero-banner h1 {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        color: #a0a0c0;
        font-size: 1.05rem;
        font-weight: 400;
    }

    /* ── Metric Cards ── */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        flex: 1;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(100, 100, 255, 0.15);
    }
    .metric-card .value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card .label {
        color: #8888aa;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }

    /* ── Candidate Card ── */
    .candidate-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transition: transform 0.2s ease;
    }
    .candidate-card:hover {
        transform: translateY(-2px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    .candidate-card .rank-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 0.8rem;
    }
    .candidate-card .name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #e0e0ff;
        display: inline;
    }
    .candidate-card .score {
        float: right;
        font-size: 1.4rem;
        font-weight: 700;
        color: #4ade80;
    }
    .candidate-card .details {
        color: #9999bb;
        font-size: 0.9rem;
        margin-top: 0.6rem;
    }
    .candidate-card .skills-row {
        margin-top: 0.7rem;
    }
    .skill-tag {
        display: inline-block;
        background: rgba(102, 126, 234, 0.15);
        color: #667eea;
        border: 1px solid rgba(102, 126, 234, 0.25);
        padding: 0.2rem 0.6rem;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 500;
        margin: 0.15rem 0.2rem;
    }

    /* ── Sidebar Styling ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29, #1a1a2e);
    }

    /* ── Status Badges ── */
    .status-connected { color: #4ade80; font-weight: 600; }
    .status-disconnected { color: #f87171; font-weight: 600; }

    /* ── Progress Section ── */
    .step-indicator {
        background: rgba(102, 126, 234, 0.1);
        border-left: 3px solid #667eea;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.4rem 0;
        color: #c0c0e0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def check_api():
    """Check if the FastAPI backend is running."""
    try:
        r = requests.get(f"{API_BASE}/", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def upload_files(files):
    """Upload PDF files to the API."""
    file_tuples = [("files", (f.name, f.getvalue(), "application/pdf")) for f in files]
    r = requests.post(f"{API_BASE}/api/upload", files=file_tuples, timeout=30)
    return r.json()


def set_jd(text):
    """Send job description to the API."""
    r = requests.post(f"{API_BASE}/api/job-description", data={"jd_text": text}, timeout=10)
    return r.json()


def process():
    """Trigger the processing pipeline."""
    r = requests.post(f"{API_BASE}/api/process", timeout=300)
    return r.json()


def get_results():
    """Fetch results from the API."""
    r = requests.get(f"{API_BASE}/api/results", timeout=10)
    return r.json()


def cleanup():
    """Cleanup temp files via API."""
    r = requests.delete(f"{API_BASE}/api/cleanup", timeout=10)
    return r.json()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # API status
    api_ok = check_api()
    if api_ok:
        st.markdown('<p class="status-connected">● API Connected</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-disconnected">● API Offline</p>', unsafe_allow_html=True)
        st.warning("Start the FastAPI server first:\n```\nuvicorn main:app --reload --port 8000\n```")

    st.divider()

    # Score threshold
    threshold = st.slider("🎯 Shortlist Threshold", 0, 100, 60, step=5,
                          help="Candidates below this score will be greyed out")

    st.divider()

    # Cleanup button
    if st.button("🗑️ Clear All Data", use_container_width=True, type="secondary"):
        try:
            result = cleanup()
            st.success(result.get("message", "Cleaned up!"))
            if "results" in st.session_state:
                del st.session_state["results"]
        except Exception as e:
            st.error(f"Cleanup failed: {e}")

    st.divider()
    st.markdown("""
    <div style="text-align:center; color:#666; font-size:0.8rem;">
        <p>AI Resume Shortlister v1.0</p>
        <p>FastAPI + Streamlit + FAISS</p>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MAIN CONTENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ── Hero Banner ───────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>🧠 AI Resume Shortlister</h1>
    <p>Upload resumes • Match with job descriptions • Rank the best candidates</p>
</div>
""", unsafe_allow_html=True)


# ── Upload Section ────────────────────────────────────────────
col_upload, col_jd = st.columns(2, gap="large")

with col_upload:
    st.markdown("### 📄 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Drop your PDF resumes here",
        type=["pdf"],
        accept_multiple_files=True,
        key="resume_uploader",
    )
    if uploaded_files:
        st.info(f"📎 {len(uploaded_files)} file(s) selected")

with col_jd:
    st.markdown("### 📋 Job Description")
    jd_text = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="Example: We are looking for a Python developer with experience in machine learning, deep learning, and NLP...",
        key="jd_input",
    )
    if jd_text:
        st.info(f"📝 {len(jd_text.split())} words entered")


# ── Process Button ────────────────────────────────────────────
st.markdown("---")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    process_btn = st.button(
        "🚀 Process & Rank Candidates",
        use_container_width=True,
        type="primary",
        disabled=not (uploaded_files and jd_text and api_ok),
    )

if process_btn:
    with st.status("🔄 Processing resumes...", expanded=True) as status:
        try:
            # Step 1: Upload
            st.write("📤 Uploading resumes...")
            upload_result = upload_files(uploaded_files)
            st.write(f"✅ {upload_result['message']}")

            # Step 2: Set JD
            st.write("📋 Setting job description...")
            jd_result = set_jd(jd_text)
            st.write(f"✅ {jd_result['message']}")

            # Step 3: Process
            st.write("🧠 Running AI pipeline (Parse → Embed → Match → Score → Rank)...")
            st.write("⏳ This may take a moment for first run (model download)...")
            result = process()
            st.write(f"✅ {result['message']}")

            # Store results
            st.session_state["results"] = result.get("candidates", [])
            status.update(label="✅ Processing complete!", state="complete", expanded=False)

        except requests.exceptions.ConnectionError:
            status.update(label="❌ Connection failed", state="error")
            st.error("Cannot connect to API. Is the FastAPI server running?")
        except Exception as e:
            status.update(label="❌ Error", state="error")
            st.error(f"Processing failed: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  RESULTS SECTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if "results" in st.session_state and st.session_state["results"]:
    candidates = st.session_state["results"]

    st.markdown("---")
    st.markdown("## 🏆 Results")

    # ── Metric Cards ──────────────────────────────────────────
    total = len(candidates)
    shortlisted = sum(1 for c in candidates if c["final_score"] >= threshold)
    avg_score = sum(c["final_score"] for c in candidates) / total if total else 0
    top_score = candidates[0]["final_score"] if candidates else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{total}</div>
            <div class="label">Total Candidates</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{shortlisted}</div>
            <div class="label">Shortlisted</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{avg_score:.1f}</div>
            <div class="label">Avg Score</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{top_score:.1f}</div>
            <div class="label">Top Score</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── View Toggle ───────────────────────────────────────────
    view_mode = st.radio("View Mode", ["📇 Cards", "📊 Table"], horizontal=True, label_visibility="collapsed")

    if view_mode == "📇 Cards":
        # ── Candidate Cards ──────────────────────────────────
        for c in candidates:
            is_shortlisted = c["final_score"] >= threshold
            score_color = "#4ade80" if is_shortlisted else "#f87171"
            opacity = "1" if is_shortlisted else "0.5"
            skills_html = "".join(f'<span class="skill-tag">{s}</span>' for s in c.get("skills", [])[:10])

            st.markdown(f"""
            <div class="candidate-card" style="opacity: {opacity}">
                <div>
                    <span class="rank-badge">#{c['rank']}</span>
                    <span class="name">{c['name']}</span>
                    <span class="score" style="color: {score_color}">{c['final_score']:.1f}</span>
                </div>
                <div class="details">
                    📧 {c['email'] or 'N/A'} &nbsp;&nbsp; 📞 {c['phone'] or 'N/A'} &nbsp;&nbsp;
                    📄 {c['filename']}
                </div>
                <div class="details">
                    🎯 Similarity: {c['similarity_score']:.1f}% &nbsp;&nbsp;
                    📋 ATS: {c['ats_score']:.1f}% &nbsp;&nbsp;
                    🏅 Final: {c['final_score']:.1f}%
                </div>
                <div class="skills-row">{skills_html}</div>
            </div>
            """, unsafe_allow_html=True)

            # Expandable details
            with st.expander(f"🔍 Details for {c['name']}", expanded=False):
                det1, det2 = st.columns(2)
                with det1:
                    st.markdown("**✅ Matched Keywords:**")
                    if c.get("matched_keywords"):
                        st.write(", ".join(c["matched_keywords"]))
                    else:
                        st.write("None")
                with det2:
                    st.markdown("**❌ Missing Keywords:**")
                    if c.get("missing_keywords"):
                        st.write(", ".join(c["missing_keywords"]))
                    else:
                        st.write("None")
                st.markdown("**🎓 Education:**")
                st.write(", ".join(c.get("education", [])) or "Not detected")
                st.markdown(f"**💼 Experience:** {c.get('experience_years', 'N/A')}")

    else:
        # ── Table View ────────────────────────────────────────
        df = pd.DataFrame(candidates)
        display_cols = ["rank", "name", "email", "phone", "final_score",
                        "similarity_score", "ats_score", "filename"]
        display_cols = [c for c in display_cols if c in df.columns]
        df_display = df[display_cols].copy()
        df_display.columns = ["Rank", "Name", "Email", "Phone", "Final Score",
                              "Similarity %", "ATS Score", "File"][:len(display_cols)]

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Final Score": st.column_config.ProgressColumn(
                    "Final Score", min_value=0, max_value=100, format="%.1f"
                ),
                "Similarity %": st.column_config.ProgressColumn(
                    "Similarity %", min_value=0, max_value=100, format="%.1f"
                ),
                "ATS Score": st.column_config.ProgressColumn(
                    "ATS Score", min_value=0, max_value=100, format="%.1f"
                ),
            },
        )

    # ── Download Button ───────────────────────────────────────
    st.markdown("---")
    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        try:
            r = requests.get(f"{API_BASE}/api/download-csv", timeout=10)
            st.download_button(
                "📥 Download Results as CSV",
                data=r.content,
                file_name="resume_shortlist_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
        except Exception:
            st.warning("Could not fetch CSV from API.")

elif not api_ok:
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:3rem; color:#8888aa;">
        <h3>🔌 Backend Not Connected</h3>
        <p>Start the FastAPI server to begin:</p>
        <code>cd resume_project && uvicorn main:app --reload --port 8000</code>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:3rem; color:#8888aa;">
        <h3>📤 Upload resumes and paste a job description to get started</h3>
        <p>The AI will parse, analyze, score, and rank your candidates automatically.</p>
    </div>
    """, unsafe_allow_html=True)
