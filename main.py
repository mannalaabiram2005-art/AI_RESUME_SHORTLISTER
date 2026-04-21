"""
main.py — FastAPI Backend for AI Resume Shortlister

This is the central API server that orchestrates the entire pipeline:
    Upload → Parse → Embed → Match → Score → Extract → Rank → Export

Endpoints:
    POST /api/upload          — Upload resume PDFs
    POST /api/job-description — Set the job description text
    POST /api/process         — Run the full pipeline
    GET  /api/results         — Retrieve ranked results
    GET  /api/download-csv    — Download results as CSV
    DELETE /api/cleanup       — Remove temp files

Run with:
    uvicorn main:app --reload --port 8000
"""

import os
import csv
import io
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ─── Import project modules ───────────────────────────────────
from ingestion.upload import save_resume, get_all_resumes, cleanup_temp, ensure_directories, OUTPUT_DIR
from parsing.parser import extract_text_from_pdf
from embeddings.embedder import generate_embedding, generate_embeddings_batch
from matching.matcher import match_resumes_to_job
from scoring.scorer import calculate_ats_score, calculate_final_score
from extraction.extractor import extract_all
from ranking.ranker import rank_candidates


# ─── App State (in-memory store) ──────────────────────────────
class AppState:
    """Simple in-memory state to hold JD and results between requests."""
    def __init__(self):
        self.job_description: str = ""
        self.results: list = []
        self.is_processing: bool = False

state = AppState()


# ─── Lifespan (startup/shutdown) ──────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_directories()
    print("[START] AI Resume Shortlister API is starting...")
    yield
    print("[STOP] Shutting down...")


# ─── FastAPI App ──────────────────────────────────────────────
app = FastAPI(
    title="AI Resume Shortlister API",
    description="Upload resumes, compare with job descriptions, rank candidates.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ENDPOINTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "running", "message": "AI Resume Shortlister API v1.0"}


@app.post("/api/upload")
async def upload_resumes(files: list[UploadFile] = File(...)):
    """
    Upload one or more resume PDFs.
    Files are saved to temp_resumes/ directory.
    """
    saved = []
    for f in files:
        if not f.filename.lower().endswith(".pdf"):
            continue
        content = await f.read()
        path = save_resume(content, f.filename)
        saved.append({"filename": f.filename, "path": path})

    if not saved:
        raise HTTPException(status_code=400, detail="No valid PDF files uploaded.")

    return {"message": f"{len(saved)} resume(s) uploaded successfully.", "files": saved}


@app.post("/api/job-description")
async def set_job_description(jd_text: str = Form(...)):
    """Set the job description text for matching."""
    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
    state.job_description = jd_text.strip()
    return {"message": "Job description saved.", "length": len(state.job_description)}


@app.post("/api/process")
async def process_resumes():
    """
    Run the full pipeline:
    Parse → Embed → Match → Score → Extract → Rank → Save CSV
    """
    if state.is_processing:
        raise HTTPException(status_code=409, detail="Processing already in progress.")

    if not state.job_description:
        raise HTTPException(status_code=400, detail="Set a job description first via /api/job-description.")

    resume_paths = get_all_resumes()
    if not resume_paths:
        raise HTTPException(status_code=400, detail="No resumes uploaded. Upload via /api/upload.")

    state.is_processing = True
    try:
        # ── STEP 1: Parse PDFs ────────────────────────────────
        print(f"[STEP 1] Parsing {len(resume_paths)} resume(s)...")
        resume_texts = []
        valid_paths = []
        for path in resume_paths:
            text = extract_text_from_pdf(path)
            if text:
                resume_texts.append(text)
                valid_paths.append(path)

        if not resume_texts:
            raise HTTPException(status_code=400, detail="Could not extract text from any PDF.")

        # ── STEP 2: Generate Embeddings ───────────────────────
        print("[STEP 2] Generating embeddings...")
        resume_embeddings = generate_embeddings_batch(resume_texts)
        jd_embedding = generate_embedding(state.job_description)

        # ── STEP 3: Match (Similarity via FAISS) ──────────────
        print("[STEP 3] Matching resumes to job description...")
        similarity_scores = match_resumes_to_job(resume_embeddings, jd_embedding)

        # ── STEP 4 & 5: Score (ATS + Final) ───────────────────
        print("[STEP 4] Calculating scores...")
        candidates = []
        for i, (text, path) in enumerate(zip(resume_texts, valid_paths)):
            # ATS score
            ats_result = calculate_ats_score(text, state.job_description)
            # Final combined score
            final_score = calculate_final_score(similarity_scores[i], ats_result["ats_score"])

            # ── STEP 6: Extract info ──────────────────────────
            info = extract_all(text)

            candidate = {
                "filename": os.path.basename(path),
                "name": info["name"],
                "email": info["email"],
                "phone": info["phone"],
                "skills": info["skills"],
                "education": info["education"],
                "experience_years": info["experience_years"],
                "similarity_score": round(similarity_scores[i] * 100, 1),
                "ats_score": ats_result["ats_score"],
                "final_score": final_score,
                "matched_keywords": ats_result["matched_keywords"],
                "missing_keywords": ats_result["missing_keywords"],
            }
            candidates.append(candidate)

        # ── STEP 7: Rank ──────────────────────────────────────
        print("[STEP 5] Ranking candidates...")
        ranked = rank_candidates(candidates)
        state.results = ranked

        # ── STEP 8: Save to CSV ───────────────────────────────
        _save_results_csv(ranked)
        print(f"[DONE] Processing complete! {len(ranked)} candidates ranked.")

        return {
            "message": f"Processed {len(ranked)} resume(s) successfully.",
            "candidates": ranked,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        state.is_processing = False


@app.get("/api/results")
async def get_results():
    """Retrieve the latest ranked results."""
    if not state.results:
        return {"message": "No results yet. Run /api/process first.", "candidates": []}
    return {"candidates": state.results, "total": len(state.results)}


@app.get("/api/download-csv")
async def download_csv():
    """Download results as a CSV file."""
    if not state.results:
        raise HTTPException(status_code=404, detail="No results to download.")

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["rank", "name", "email", "phone", "skills", "final_score",
                     "similarity_score", "ats_score", "filename"],
    )
    writer.writeheader()
    for c in state.results:
        row = {k: v for k, v in c.items() if k in writer.fieldnames}
        row["skills"] = ", ".join(c.get("skills", []))
        writer.writerow(row)

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=results.csv"},
    )


@app.delete("/api/cleanup")
async def cleanup():
    """Delete all temporary resume files and clear results."""
    cleanup_temp()
    state.results = []
    state.job_description = ""
    return {"message": "All temporary files deleted and state cleared."}


# ─── Helper: Save CSV to outputs/ ─────────────────────────────
def _save_results_csv(candidates: list):
    """Save ranked results to outputs/results.csv."""
    csv_path = OUTPUT_DIR / "results.csv"
    fieldnames = ["rank", "name", "email", "phone", "skills", "final_score",
                  "similarity_score", "ats_score", "filename"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in candidates:
            row = {k: v for k, v in c.items() if k in fieldnames}
            row["skills"] = ", ".join(c.get("skills", []))
            writer.writerow(row)
    print(f"[SAVED] Results saved to {csv_path}")
