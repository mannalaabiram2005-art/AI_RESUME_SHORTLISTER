# 📘 BEGINNER'S COMPLETE GUIDE — AI Resume Shortlister
### *Written for anyone — even if you have ZERO coding knowledge*

---

> **How to read this guide:**
> Read it top to bottom, like a story. Every section builds on the previous one.
> By the end, you will understand **exactly** what this project does, how it works,
> and why every single tool was chosen.

---

## 🧠 PART 1 — What Is This Project? (The Big Picture)

### Imagine this real-world problem:

A big company posts a job opening. The next day, **500 resumes** arrive in their email.

The HR manager now has to:
1. Open each PDF one by one
2. Read through 500 resumes
3. Compare each person's skills to what the job needs
4. Shortlist the top 10 candidates
5. Do all of this before the deadline tomorrow

This is **exhausting, slow, and humans make mistakes** when tired. They might miss a great candidate or unfairly rate someone just because they read it at 2 AM.

### What our project does:

> **This project is an AI-powered robot that does all of that automatically.**

You give it:
- 📄 A bunch of resume PDF files
- 📋 The job description (what skills the company needs)

It gives you back:
- 🏆 A ranked list: Candidate #1 is the best match, Candidate #2 is second best, and so on
- 📊 Scores for each person (out of 100)
- 📬 Their name, email, phone number, skills — all automatically extracted
- 📥 A downloadable spreadsheet (CSV file) with all results

The entire process takes **seconds**, not hours.

---

## 🗺️ PART 2 — The Project From 10,000 Feet (Simple Overview)

Think of this project like a **factory with an assembly line**:

```
[You upload PDFs]
       ↓
  STATION 1: Receptionist saves the files
       ↓
  STATION 2: Reader opens each PDF and reads the text
       ↓
  STATION 3: AI Translator converts text into special numbers
       ↓
  STATION 4: Comparator checks how similar each resume is to the job
       ↓
  STATION 5: Grader gives each resume a score out of 100
       ↓
  STATION 6: Detective extracts name, email, phone, skills
       ↓
  STATION 7: Leaderboard sorts everyone by score
       ↓
[You see ranked results + download CSV]
```

There are **2 parts running at the same time**:
- 🔧 **The Engine (Backend)** — FastAPI does all the heavy work behind the scenes
- 🖥️ **The Face (Frontend)** — Streamlit shows you a beautiful website to interact with

---

## 📁 PART 3 — The Project Files (What Does Each Folder Do?)

```
Resume_project/
│
├── main.py              → The Manager. Coordinates EVERYTHING.
│
├── ingestion/           → Station 1: Saves uploaded PDF files
│   └── upload.py
│
├── parsing/             → Station 2: Reads text from PDFs
│   └── parser.py
│
├── embeddings/          → Station 3: AI converts text to numbers
│   └── embedder.py
│
├── matching/            → Station 4: Compares resume vs job description
│   └── matcher.py
│
├── scoring/             → Station 5: Calculates the score
│   └── scorer.py
│
├── extraction/          → Station 6: Finds name, email, phone, skills
│   └── extractor.py
│
├── ranking/             → Station 7: Sorts candidates by score
│   └── ranker.py
│
├── ui/                  → The Website (what you see in your browser)
│   └── app.py
│
├── temp_resumes/        → Temporary storage for uploaded PDFs
├── outputs/             → Where the final CSV results are saved
└── requirements.txt     → Shopping list of all tools/libraries needed
```

**Simple rule to remember:** Each folder = one job. One worker. One task.

---

## 🔄 PART 4 — The Full Step-by-Step Journey of a Resume

Let's trace what happens to a single resume file from the moment you upload it to when you see it ranked on screen.

---

### 🔵 STEP 0 — Before Anything: Starting the Project

The project has TWO programs running simultaneously:

**Program 1 — The Engine (run in Terminal 1):**
```
uvicorn main:app --reload --port 8000
```
This starts the brain of the project. It listens at address `http://localhost:8000`.

**Program 2 — The Website (run in Terminal 2):**
```
streamlit run ui/app.py --server.port 8501
```
This starts the visual dashboard you see in your browser at `http://localhost:8501`.

> **What is localhost?** It means "this computer". Port 8000 and 8501 are like door numbers — Program 1 is behind door 8000, Program 2 is behind door 8501.

---

### 🟢 STEP 1 — You Open the Website

You open your browser and go to `http://localhost:8501`.

You see:
- A **"Upload Resumes"** section on the left
- A **"Job Description"** text box on the right
- A big **"Process & Rank Candidates"** button in the middle

The website (Streamlit) also **checks if the Engine is running**. If it is, it shows a green dot: `● API Connected`. If not, it shows red: `● API Offline`.

---

### 🟡 STEP 2 — You Upload Resume PDFs

You drag and drop 10 resume PDF files onto the upload area.

**What happens under the hood:**
1. Streamlit takes those files from your browser
2. It sends them to the Engine via an HTTP request: `POST http://localhost:8000/api/upload`
3. The Engine receives the files and calls `ingestion/upload.py`
4. `upload.py` saves each PDF into a folder called `temp_resumes/`
5. The Engine replies: "5 resumes uploaded successfully."
6. Streamlit shows you a confirmation message

> **What is an HTTP request?** Think of it like a phone call. Streamlit (the website) dials the number of the Engine (FastAPI), and says "Hey, here are some files, please save them." The Engine picks up, does the job, and says "Done."

---

### 🟡 STEP 3 — You Enter the Job Description

You paste the job requirements in the text box:
*"We need a Python developer with 3 years of experience in Machine Learning, NLP, and AWS..."*

**What happens:**
1. Streamlit sends this text to the Engine: `POST http://localhost:8000/api/job-description`
2. The Engine stores it in memory (a variable called `state.job_description`)
3. It replies: "Job description saved."

---

### 🔴 STEP 4 — You Click "Process & Rank Candidates"

This is where the magic happens. Everything runs in sequence.

**Streamlit sends:** `POST http://localhost:8000/api/process`

The Engine now runs all 8 mini-steps inside `main.py`:

---

#### ⚙️ Mini-Step 1 of 8: Parse PDFs (`parsing/parser.py`)

The Engine opens each saved PDF using a library called **PyMuPDF**.

Think of it like this: A PDF is like a locked book. PyMuPDF is like a key that unlocks it and **reads all the text aloud** so the computer can hear it.

**Before parsing:** `john_doe_resume.pdf` (computer can't understand this — it's a picture of text)

**After parsing:** 
```
John Doe
john@email.com | +91 9876543210
Python Developer with 4 years of experience...
Skills: Python, Machine Learning, AWS, Docker...
Education: B.Tech Computer Science, IIT Delhi 2020
```

Now the computer has **plain text** it can work with.

---

#### ⚙️ Mini-Step 2 of 8: Generate Embeddings (`embeddings/embedder.py`)

This is the most "magical" step. The computer now needs to **understand the meaning** of the resume text, not just the words.

**The problem:** Computers can't understand human language. They only understand numbers (0s and 1s).

**The solution:** Use an **AI model** to convert text into a list of 384 numbers. These numbers capture the **meaning** of the text.

Example:
```
"Python Developer" → [0.12, -0.34, 0.87, 0.23, -0.09, ...]  (384 numbers)
"Software Engineer" → [0.11, -0.31, 0.85, 0.24, -0.07, ...]  (384 numbers)
```

Notice: "Python Developer" and "Software Engineer" produce **similar numbers** because they mean similar things! This is the power of AI embeddings.

The AI model used is called **`all-MiniLM-L6-v2`** (more on this model later in the Tech Stack section).

**Both the resume AND the job description get converted to 384 numbers each.**

---

#### ⚙️ Mini-Step 3 of 8: Match Resumes to Job (`matching/matcher.py`)

Now we have:
- Resume 1 → 384 numbers
- Resume 2 → 384 numbers
- Resume 3 → 384 numbers
- Job Description → 384 numbers

**Question:** Which resume is most similar to the job description?

**Answer:** We use **FAISS** (a super-fast search tool by Facebook) to compare all resume vectors to the job description vector.

This comparison technique is called **Cosine Similarity**. Think of it like this: if two resumes are pointing in the same "direction" in space as the job description, they are similar.

**Result:** Each resume gets a similarity score between 0% and 100%.

---

#### ⚙️ Mini-Step 4 of 8: Calculate ATS Score (`scoring/scorer.py`)

ATS stands for **Applicant Tracking System** — the industry-standard way HR software scores resumes.

This is a **rule-based scoring system** (no AI, just logic):

| What is checked | Weight | How |
|---|---|---|
| Keyword Match | 60% | How many job keywords appear in the resume? |
| Section Presence | 20% | Does the resume have Education, Experience, Skills, Contact sections? |
| Resume Length | 10% | Is the resume between 200-1000 words? (Not too short, not too long) |
| Formatting | 10% | Does the resume have an email address and phone number? |

**Example calculation:**
- Keywords: Resume has 7 out of 10 job keywords → 70% → × 0.60 = 42
- Sections: Has all 4 sections → 100% → × 0.20 = 20
- Length: 450 words → 100% → × 0.10 = 10
- Formatting: Has email + phone → 100% → × 0.10 = 10
- **ATS Score = 42 + 20 + 10 + 10 = 82 out of 100**

---

#### ⚙️ Mini-Step 5 of 8: Calculate Final Score

Both scores are combined into one Final Score:

```
Final Score = (Similarity Score × 60%) + (ATS Score × 40%)
```

**Why this formula?**
- Similarity Score (AI-based) is weighted more (60%) because it understands *meaning*
- ATS Score (rule-based) is weighted less (40%) but still important because it checks *structure*

**Example:**
```
Similarity = 85%,  ATS = 78%
Final Score = (85 × 0.60) + (78 × 0.40)
           = 51 + 31.2
           = 82.2 out of 100
```

---

#### ⚙️ Mini-Step 6 of 8: Extract Information (`extraction/extractor.py`)

Now the system needs to pull out specific information from each resume text using **Regex** (pattern matching rules).

**What is Regex?** It's like a search pattern. For example:
- Email pattern: "Find me anything that looks like `something@something.com`"
- Phone pattern: "Find me 10 consecutive digits, possibly with dashes or spaces"
- Name pattern: "The first line of the resume that has 1-5 words and is only letters is probably the name"

**What gets extracted:**
- 👤 Name (e.g., "John Doe")
- 📧 Email (e.g., "john@email.com")
- 📞 Phone (e.g., "+91 9876543210")
- 💻 Skills (matched against a database of 80+ known skills like Python, AWS, React, etc.)
- 🎓 Education (degree pattern matching — B.Tech, M.Tech, PhD, etc.)
- ⏱️ Experience Years (finds "5 years of experience" in text)

---

#### ⚙️ Mini-Step 7 of 8: Rank Candidates (`ranking/ranker.py`)

All candidates now have a Final Score. This step simply **sorts them from highest to lowest** and assigns rank numbers: #1, #2, #3...

This is like a leaderboard in a video game — whoever has the highest score is at the top.

---

#### ⚙️ Mini-Step 8 of 8: Save to CSV + Return Results

The sorted list is:
1. Saved to `outputs/results.csv` (a spreadsheet file you can open in Excel)
2. Sent back to Streamlit, which shows you the beautiful results dashboard

---

### 🟢 STEP 5 — You See the Results

The Streamlit dashboard shows:
- **Metric Cards:** Total candidates, Shortlisted count, Average score, Top score
- **Candidate Cards (or Table):** Each candidate with their rank, name, scores, skills, email, phone
- **Green cards** = Candidates above your threshold (shortlisted ✅)
- **Dim/faded cards** = Candidates below your threshold ❌
- **Expand button** per candidate → Shows matched keywords, missing keywords, education, experience

---

### 🟢 STEP 6 — You Download the CSV

One click on "📥 Download Results as CSV" and you get a spreadsheet with all ranked results that you can open in Microsoft Excel or Google Sheets.

---

## 🛠️ PART 5 — THE COMPLETE TECH STACK (Every Tool Explained)

*For each technology, we answer three questions:*
1. **WHAT** — What is it and what does it do in THIS project?
2. **WHY NOT** — What were the alternatives and why were they not chosen?
3. **WHY THIS** — Why was THIS specific tool the best choice here?

---

### 🐍 1. Python (Programming Language)

#### ✅ WHAT — What is Python and what does it do here?

Python is the programming language that the **entire project is written in**. Every single file — `main.py`, `parser.py`, `embedder.py`, all of them — is Python code.

Think of a programming language like a human language. Just like you write instructions to a person in English, you write instructions to a computer in Python (or another programming language). Python is the language the computer reads and executes.

In this project, Python is used to:
- Write the logic for all 7 processing steps
- Connect all modules together
- Handle file reading/writing
- Do mathematical calculations (scores, similarity)
- Run the API server

#### ❌ WHY NOT — What are the alternatives?

| Alternative | The problem with it |
|---|---|
| **JavaScript (Node.js)** | Has very limited AI/ML libraries compared to Python. The best AI tools only work in Python. |
| **Java** | Very verbose (takes 10x more code to do the same thing). Hard to use AI libraries. |
| **R** | Only for statistics/research. No good web framework. Terrible for production software. |
| **C++** | Extremely fast but incredibly complex to write. No AI libraries for quick development. |
| **PHP** | Only for web pages. Not suitable for AI/data processing tasks at all. |

#### 🏆 WHY THIS — Why Python specifically?

- **#1 Language for AI/ML in the world.** Every major AI library (TensorFlow, PyTorch, Hugging Face) is built for Python first.
- **Readable like English.** A beginner can read Python code and mostly understand it.
- **Massive library ecosystem.** There is a Python library for literally everything — PDF reading, AI, web servers, data processing.
- **FastAPI, Streamlit, FAISS, sentence-transformers** — every library in this project only works efficiently in Python.

---

### ⚡ 2. FastAPI (Backend/API Framework)

#### ✅ WHAT — What is FastAPI and what does it do here?

FastAPI is the **backbone of this project**. It creates a web server (the "Engine") that listens for requests and handles all the processing logic.

Think of FastAPI like a **restaurant manager**:
- The customer (Streamlit) walks in and says "I want Table 5 cleaned" (POST /api/upload)
- The manager (FastAPI) says "Sure" and tells the waiter (upload.py) to do it
- When done, the manager reports back "Table 5 is clean" (returns a JSON response)

FastAPI defines 6 API endpoints (like menu items):
| Endpoint | What it does |
|---|---|
| `POST /api/upload` | Receive and save resume PDF files |
| `POST /api/job-description` | Save the job description text |
| `POST /api/process` | Run the entire 8-step pipeline |
| `GET /api/results` | Return the ranked results |
| `GET /api/download-csv` | Stream the CSV file for download |
| `DELETE /api/cleanup` | Delete all temporary files |

#### ❌ WHY NOT — What are the alternatives?

| Alternative | The problem with it |
|---|---|
| **Flask** | Older, slower, no automatic data validation, no automatic API docs, no async support |
| **Django** | Too heavy/complex. Designed for full websites with databases and authentication. Overkill for an API. |
| **Express (Node.js)** | Different language (JavaScript). Can't use Python AI libraries. |
| **Tornado** | Very low-level. You have to write a lot more code for simple things. |

#### 🏆 WHY THIS — Why FastAPI specifically?

- **Automatic interactive documentation.** Go to `http://localhost:8000/docs` and you get a beautiful page where you can test every endpoint without writing any code. FastAPI generates this automatically.
- **Fastest Python web framework available.** It is async (non-blocking), meaning it can handle multiple requests at the same time.
- **Automatic data validation.** If you send bad data (like a text file instead of a PDF), FastAPI rejects it automatically with a clear error message.
- **Designed for AI/ML APIs.** It is the industry standard for Python AI backends.

---

### 🦄 3. Uvicorn (The Server Runner)

#### ✅ WHAT — What is Uvicorn and what does it do here?

Uvicorn is the **engine that actually runs FastAPI**. FastAPI is just a blueprint — Uvicorn is what starts it, keeps it running, and listens for incoming connections.

Analogy: If FastAPI is the recipe, Uvicorn is the chef who actually cooks it.

You start it with: `uvicorn main:app --reload --port 8000`
- `main` = the file name (`main.py`)
- `app` = the FastAPI object inside that file
- `--reload` = automatically restart when you save code changes
- `--port 8000` = listen on port 8000 (door number 8000)

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **Gunicorn** | Older, synchronous workers. Not designed for async Python (which FastAPI uses). |
| **Waitress** | Windows-only, slower, not designed for modern async frameworks. |
| **Built-in Flask server** | Toy server. Not suitable for real use. Single-threaded. |

#### 🏆 WHY THIS?

- **Official recommendation.** FastAPI's own documentation says "use Uvicorn."
- **Supports async.** It uses the ASGI standard (Asynchronous Server Gateway Interface), which is what FastAPI is built on.
- **Lightning fast.** One of the fastest Python servers available.
- **Hot reload.** The `--reload` flag means you don't have to restart the server every time you change code.

---

### 🎨 4. Streamlit (Frontend UI Framework)

#### ✅ WHAT — What is Streamlit and what does it do here?

Streamlit creates the **visual website** you interact with in your browser. It is the "face" of this project.

Without Streamlit, you would have to interact with the project by typing raw commands in a terminal. Streamlit turns the project into a beautiful dashboard with:
- File upload buttons
- Text input boxes
- Process buttons
- Result cards with color coding
- Download buttons
- Progress indicators

The Streamlit code lives in `ui/app.py`. It:
1. Shows the page layout (upload area, job description box, results)
2. Makes HTTP calls to FastAPI when you click buttons
3. Displays whatever FastAPI sends back

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **React.js** | Requires JavaScript, HTML, CSS expertise. Completely separate codebase. Much more complex. |
| **Flask + HTML templates** | Have to manually write HTML/CSS/JavaScript. Time-consuming. |
| **Gradio** | Simpler but limited. Less control over layout. Not designed for multi-step data pipelines. |
| **Django templates** | Same issue as Flask — need to write raw HTML/CSS. |
| **Tkinter (desktop app)** | Only runs on local machine, can't be shared as a web page. Ugly by default. |

#### 🏆 WHY THIS?

- **Pure Python.** You write a UI using Python code. No HTML, CSS, or JavaScript needed. A data scientist can build a beautiful app in hours.
- **Designed exactly for AI/data projects.** Streamlit was built specifically for machine learning and data apps.
- **Beautiful by default.** Dark themes, progress bars, data tables, download buttons — all built-in.
- **Fast prototyping.** The entire `ui/app.py` file that creates the full dashboard is only ~500 lines. A React equivalent would be 5x more code.

---

### 📄 5. PyMuPDF / fitz (PDF Parser)

#### ✅ WHAT — What is PyMuPDF and what does it do here?

PyMuPDF is the library that **reads PDF files and extracts text**. The library is installed as `PyMuPDF` but imported in code as `fitz`.

In `parsing/parser.py`, it opens each resume PDF and reads every page's text content:
```
doc = fitz.open("john_doe_resume.pdf")
for page in doc:
    text = page.get_text()   # Gets the plain text from each page
```

**Without this:** The computer would see a PDF as just a binary blob of data (meaningless bytes). PyMuPDF translates the PDF format into readable text.

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **pdfplumber** | Slower for large batches. Less reliable for complex PDF layouts. |
| **pypdf / PyPDF2** | Older and less accurate. Often fails on PDFs with unusual fonts or encoding. |
| **pdfminer** | Complex API. Slower. Good for very detailed layout extraction but overkill here. |
| **Apache PDFBox (Java)** | Different language. Not compatible with our Python project. |
| **Tesseract OCR** | For scanned image PDFs (photos of documents). Overkill for standard resume PDFs. Much slower. |

#### 🏆 WHY THIS?

- **Most reliable.** PyMuPDF is built on top of MuPDF — one of the best PDF rendering engines in the world.
- **Fastest.** It is significantly faster than alternatives for batch processing many PDFs.
- **Handles edge cases.** Works with PDFs that have unusual encodings, multiple languages, or complex layouts.
- **Actively maintained.** Regular updates and a large community.
- **Simple API.** Three lines of code to extract all text from a multi-page PDF.

---

### 🤖 6. Sentence-Transformers (AI Embedding Library)

#### ✅ WHAT — What is sentence-transformers and what does it do here?

`sentence-transformers` is the **AI brain of this project**. It converts human-readable text into mathematical vectors (lists of numbers) that capture the *meaning* of the text.

In `embeddings/embedder.py`:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("Python Developer with ML experience")
# Result: [0.12, -0.34, 0.87, ...] — 384 numbers
```

This library by itself is a high-level wrapper that makes it easy to use powerful **Transformer** AI models (the same technology behind ChatGPT) for creating text embeddings.

**Why do we need embeddings at all?** Because computers cannot compare meaning — they only compare numbers. By converting "Python Developer" and "Software Engineer" into similar number lists, the computer can detect that they are related concepts.

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **OpenAI Embeddings API** | Requires an internet connection and paid API key. Not free. Data leaves your computer (privacy concern). Rate-limited. |
| **TF-IDF (old keyword method)** | Only counts word frequencies. Does NOT understand meaning. "Python developer" and "Python programmer" would score 0% similar. |
| **spaCy word vectors** | Small vocabulary. Poor at multi-word phrases. Not as accurate for semantic search. |
| **Word2Vec** | Old technology (2013). Not as accurate. Doesn't understand sentence context. |
| **BERT (raw)** | Very complex to use directly. Requires much more code. `sentence-transformers` is essentially a user-friendly wrapper around BERT. |
| **Google Universal Sentence Encoder** | Requires TensorFlow, larger model, slower. Less integration with Python ecosystem. |

#### 🏆 WHY THIS?

- **State-of-the-art accuracy.** `sentence-transformers` uses the latest Transformer architecture, the same technology behind ChatGPT and Google Search.
- **Completely free and offline.** No API keys, no internet connection needed during processing (model downloads once), no cost per request.
- **Privacy.** All data stays on your local machine. No resume text goes to any external server.
- **Perfect for this use case.** It was designed specifically for semantic text similarity — exactly what this project needs.
- **Simple API.** Three lines of code to generate embeddings for an entire batch of resumes.

---

### 🔬 7. all-MiniLM-L6-v2 (The Specific AI Model)

#### ✅ WHAT — What is this model and what does it do here?

`all-MiniLM-L6-v2` is the specific AI model loaded inside `sentence-transformers`. It is a **pre-trained neural network** — meaning someone at Microsoft and HuggingFace already trained it on millions of documents, and we are reusing that trained brain for free.

- **"all"** = trained on all kinds of text (not just one domain)
- **"MiniLM"** = a smaller, faster version of the Microsoft MiniLM model
- **"L6"** = has 6 layers of neural network processing
- **"v2"** = version 2 (improved)

Size: About **80 MB** (downloads automatically on first run)
Output: **384-dimensional vector** per text input

#### ❌ WHY NOT — Other models?

| Model | Problem |
|---|---|
| **all-mpnet-base-v2** | 768 dimensions, 2x memory usage, slower, but only ~5% more accurate. Overkill for resumes. |
| **all-roberta-large-v1** | 1024 dimensions, very slow, needs powerful GPU. |
| **paraphrase-MiniLM-L3-v2** | Only 3 layers, less accurate, saved for devices with very limited resources. |
| **text-embedding-ada-002 (OpenAI)** | Paid, requires internet, privacy risk, $0.0001 per 1000 tokens. |
| **multilingual-e5-large** | Designed for multiple languages. Adds complexity without benefit if resumes are only in English. |

#### 🏆 WHY THIS?

- **Best speed/accuracy balance.** Industry benchmarks show it achieves 90%+ of the accuracy of much larger models at 10x the speed.
- **Perfect for batch processing.** When you process 100 resumes, speed matters. This model runs fast on a regular CPU with no GPU.
- **Recommended for semantic search.** The official sentence-transformers documentation recommends this model specifically for semantic similarity tasks — which is exactly our use case.
- **80MB is very manageable.** Downloads once, stored locally forever.

---

### 🔥 8. PyTorch (Deep Learning Framework)

#### ✅ WHAT — What is PyTorch and what does it do here?

PyTorch is the **deep learning engine** that `sentence-transformers` runs on top of. You don't directly write PyTorch code in this project — it works invisibly in the background.

When you call `model.encode("some text")`, PyTorch is the thing that actually runs the neural network computations (matrix multiplications, activation functions, etc.) inside the AI model.

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **TensorFlow/Keras** | `sentence-transformers` can technically use TensorFlow, but PyTorch is the default and better supported. Most modern AI research uses PyTorch. |
| **JAX** | Very specialized. Complex. Not supported by sentence-transformers out of the box. |
| **NumPy alone** | You'd have to implement the neural network from scratch. Impossible in practice. |
| **ONNX Runtime** | For deployment/inference only. Can't run full training workflows. |

#### 🏆 WHY THIS?

- **Default backend for sentence-transformers.** When you install `sentence-transformers`, it automatically installs `torch` as a dependency.
- **Industry standard.** 70%+ of AI research papers and projects use PyTorch.
- **CPU support.** We use `faiss-cpu` (not GPU), and PyTorch works perfectly on CPU.
- **Automatic.** We don't write a single line of PyTorch code — it runs invisibly and we get the benefits for free.

---

### 🔍 9. FAISS (Vector Similarity Search)

#### ✅ WHAT — What is FAISS and what does it do here?

FAISS stands for **Facebook AI Similarity Search**. It is an extremely fast library for finding which vectors (numbers) are most similar to a given query vector.

In `matching/matcher.py`:
1. All resume embeddings (384 numbers each) are loaded into a FAISS "index" (like a phone book of numbers)
2. The job description embedding is used as the "query"
3. FAISS instantly finds the similarity of EVERY resume to the job description
4. Returns similarity scores from 0.0 to 1.0

The similarity method used is **Cosine Similarity** (via Inner Product since vectors are normalized). It measures the "angle" between two vectors in 384-dimensional space. The smaller the angle, the more similar the meaning.

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **Pure NumPy dot product** | Perfectly fine for small sets (under 1000 resumes). We actually use this too (`compute_cosine_similarity`). But FAISS is needed for scalability. |
| **Scikit-learn cosine_similarity** | Works but is slower for large datasets. FAISS is 10-100x faster at scale. |
| **Elasticsearch with vector search** | Requires running a separate Elasticsearch database server. Huge overhead for a local tool. |
| **Pinecone/Weaviate (cloud vector DB)** | Requires internet, API key, subscription cost. |
| **Annoy (Spotify)** | Less accurate (approximate). Uses more memory. |

#### 🏆 WHY THIS?

- **Built by Facebook AI Research.** Used in production at billions of scale at Meta.
- **Blazingly fast.** Searching through millions of vectors in milliseconds.
- **Exact results.** Uses `IndexFlatIP` (Inner Product) which gives exact (not approximate) similarity scores.
- **Completely free and local.** No servers, no fees, no internet connection.
- **Scales perfectly.** Whether you have 10 resumes or 10,000, the code doesn't change.
- **Simple API.** `index.add(embeddings)` then `index.search(query, k)` — two lines to search millions of vectors.

---

### 🔢 10. NumPy (Numerical Computing)

#### ✅ WHAT — What is NumPy and what does it do here?

NumPy provides **fast numerical arrays and math operations** in Python. It is used throughout the project wherever numbers are processed.

Specifically in this project:
- Storing embedding vectors as NumPy arrays (`np.ndarray`) — this is what FAISS expects
- Performing cosine similarity calculations (dot products, vector norms)
- Converting PyTorch tensors to NumPy arrays for FAISS

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **Pure Python lists** | 50-100x slower for mathematical operations. No built-in vector math. |
| **Python math module** | Only for scalar (single number) operations. No arrays or matrices. |
| **SciPy** | Built on top of NumPy. Adds more functionality but NumPy is sufficient for this project. |
| **Pandas** | Designed for tabular data (rows/columns), not for numerical vector operations. |

#### 🏆 WHY THIS?

- **Industry standard.** NumPy is the foundation of ALL scientific computing in Python.
- **Required by dependencies.** FAISS, PyTorch, and sentence-transformers all output/consume NumPy arrays. It's the universal format.
- **Extremely fast.** NumPy operations run at the speed of C code (it's implemented in C internally).
- **No choice not to use it.** Every AI library expects NumPy. Not using it would require writing complex conversion code.

---

### 📊 11. Pandas (Data Analysis Library)

#### ✅ WHAT — What is Pandas and what does it do here?

Pandas is used to create and display the **results table** in the Streamlit UI and for CSV operations.

In `ui/app.py`, when the user switches to "Table View," Pandas converts the list of candidates into a nicely formatted table:
```python
df = pd.DataFrame(candidates)   # List of dicts → Table
st.dataframe(df)                 # Show as interactive table in browser
```

Pandas also handles the column renaming and filtering for display.

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **Python's built-in csv module** | Used in `main.py` for writing CSV. But for displaying interactive tables in Streamlit, the `csv` module returns just text, not a DataFrame that Streamlit's `st.dataframe()` can style. |
| **Polars** | Newer, faster, but less supported by Streamlit's built-in column configurations at time of writing. |
| **SQLite** | Overkill — we're not doing complex queries, just simple tabular display. |

#### 🏆 WHY THIS?

- **Streamlit integration.** `st.dataframe(pd.DataFrame(...))` is the official Streamlit way to show interactive tables with sortable columns, progress bars, etc.
- **Column configuration.** Streamlit's `column_config.ProgressColumn` (the score progress bars) only works with Pandas DataFrames.
- **Universal format.** Pandas DataFrames are the standard output of all data analysis in Python.

---

### 🌐 12. Requests (HTTP Client Library)

#### ✅ WHAT — What is Requests and what does it do here?

`requests` is the library that Streamlit uses to **communicate with FastAPI**. Every time you click a button in the UI, Streamlit sends an HTTP request to FastAPI using this library.

In `ui/app.py`:
```python
import requests
r = requests.post("http://localhost:8000/api/upload", files=file_tuples)
r = requests.post("http://localhost:8000/api/process")
r = requests.get("http://localhost:8000/api/results")
```

Without `requests`, Streamlit would have no way to talk to the FastAPI backend.

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **urllib (built-in)** | Very verbose and painful to use. No JSON parsing, no file uploads easily. |
| **httpx** | Good async alternative, but `requests` is simpler and synchronous calls are fine here. |
| **aiohttp** | Designed for async code. Streamlit doesn't need async for simple API calls. |
| **Direct function calls** | You could import FastAPI modules directly into Streamlit, but then you'd have one monolithic program instead of a clean frontend/backend separation. |

#### 🏆 WHY THIS?

- **The simplest HTTP library in Python.** Just `requests.get(url)` or `requests.post(url, data=data)`.
- **Most popular library ever.** Over 300 million downloads per month. Virtually every Python developer knows it.
- **Perfect for the task.** Synchronous calls (Streamlit waits for the response) are exactly what's needed here.

---

### 🔤 13. Regex / `re` module (Pattern Matching)

#### ✅ WHAT — What is Regex and what does it do here?

`re` is Python's built-in **Regular Expression** module. Regex lets you search for patterns in text.

Used extensively in `extraction/extractor.py` and `scoring/scorer.py`:
- **Email detection:** `r'[\w.+-]+@[\w-]+\.[\w.-]+'` → finds anything matching "letters@letters.letters"
- **Phone detection:** `r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'` → finds phone number patterns
- **Experience years:** `r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)'` → finds "5 years of experience"
- **Degree detection:** Finds "B.Tech", "M.Sc", "PhD" patterns

#### ❌ WHY NOT — Alternatives?

| Alternative | Problem |
|---|---|
| **spaCy NER (Named Entity Recognition)** | More complex to set up. Adds a large (~200MB) dependency for what regex does in 1KB of code. |
| **BERT NER models** | Extremely heavy (gigabytes of model files). Massive overkill for extracting an email address. |
| **Simple string `.find()` method** | Cannot handle variable patterns. `email.find('@')` would find '@' but can't validate the full email format. |
| **LLM (ChatGPT) extraction** | Requires internet, API key, paid, and extremely slow for batch processing. |

#### 🏆 WHY THIS?

- **Zero dependencies.** `re` is built into Python. No installation needed.
- **Perfect for structured patterns.** Email addresses, phone numbers, and degree patterns are highly structured — regex is the exact right tool.
- **Lightning fast.** Regex matching on 500 resumes takes microseconds.
- **Industry standard.** Every production ATS system uses regex for contact information extraction.

---

### 🧩 14. Python-multipart (Form Data Parser)

#### ✅ WHAT — What is python-multipart and what does it do here?

When Streamlit uploads PDF files to FastAPI, the files are sent as **multipart form data** (a web standard for file uploads). `python-multipart` is the library that FastAPI uses under the hood to parse (decode) these file uploads.

You never write code that directly uses `python-multipart` — it works automatically when FastAPI handles `UploadFile` objects.

#### 🏆 WHY THIS?

- **Required dependency for FastAPI file uploads.** Without it, `UploadFile` in FastAPI simply doesn't work.
- **FastAPI's official documentation says to install it.** No alternative in the FastAPI ecosystem.

---

### 📦 15. The Project's Own Modules (Custom Code)

Beyond the external libraries, the project has 7 custom Python modules:

| Module | File | What it does |
|---|---|---|
| `ingestion` | `upload.py` | Saves/lists/deletes PDF files in `temp_resumes/` folder |
| `parsing` | `parser.py` | Opens PDFs with PyMuPDF, extracts text per page |
| `embeddings` | `embedder.py` | Loads AI model once (singleton pattern), converts text to vectors |
| `matching` | `matcher.py` | Builds FAISS index, computes cosine similarity scores |
| `scoring` | `scorer.py` | ATS keyword/section/length/format scoring + final score formula |
| `extraction` | `extractor.py` | Regex extraction of name, email, phone, skills, education, experience |
| `ranking` | `ranker.py` | Sorts candidates by final score, assigns rank numbers |

---

## 🏗️ PART 6 — The Architecture (How Everything Connects)

```
┌─────────────────────────────────────────────────────┐
│                  YOUR BROWSER                        │
│           http://localhost:8501                      │
└──────────────────┬──────────────────────────────────┘
                   │ You click buttons here
                   ▼
┌─────────────────────────────────────────────────────┐
│            STREAMLIT (ui/app.py)                     │
│         "The Face / The Website"                     │
│  • Shows upload button, JD box, results, CSV button  │
│  • Sends HTTP requests to FastAPI using `requests`   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP Requests (API calls)
                   │ POST /api/upload
                   │ POST /api/process
                   │ GET /api/results
                   ▼
┌─────────────────────────────────────────────────────┐
│           FASTAPI (main.py)                          │
│         "The Manager / The Brain"                    │
│  • Receives requests from Streamlit                  │
│  • Calls modules in sequence                         │
│  • Returns JSON responses                            │
└────┬─────┬──────┬──────┬────┬──────┬────────────────┘
     │     │      │      │    │      │
     ▼     ▼      ▼      ▼    ▼      ▼
  upload  parser embed  match score extract  rank
   .py    .py    er.py  er.py  er.py  or.py  er.py
     │                    │            │
     ▼                    ▼            ▼
temp_resumes/      FAISS Index    outputs/
  (PDF files)    (vector search)  results.csv
                      │
                      ▼
              AI Model (all-MiniLM-L6-v2)
              stored locally after first download
```

**Key architectural decision:** The project uses a **client-server pattern** where:
- **Streamlit** = Client (makes requests, shows results)
- **FastAPI** = Server (does work, returns data)

They communicate via HTTP, the same way your browser talks to websites.

---

## 📐 PART 7 — How Scores Are Calculated (Complete Math)

### ATS Score Breakdown

```
ATS Score = (Keyword Score × 0.60)
           + (Section Score × 0.20)
           + (Length Score × 0.10)
           + (Format Score × 0.10)
```

**Keyword Score (60% weight):**
- Find all technical keywords in the job description (Python, AWS, Docker, etc.)
- Count how many of those keywords also appear in the resume
- Score = (matched keywords / total JD keywords) × 100

**Section Score (20% weight):**
- Check if the resume has: Education section, Experience section, Skills section, Contact info
- Score = (sections found / 4) × 100

**Length Score (10% weight):**
- 200-1000 words → 100 points (ideal resume length)
- 100-200 or 1000-1500 words → 70 points (acceptable)
- Below 100 or above 1500 words → 40 points (too short or too long)

**Format Score (10% weight):**
- Has email? +50 points
- Has phone number? +50 points
- Score = ((has_email + has_phone) / 2) × 100

---

### Final Score Formula

```
Final Score = (Similarity Score × 0.60) + (ATS Score × 0.40)
```

- Similarity Score ranges from 0.0 to 1.0 (gets multiplied by 100 to become 0-100)
- ATS Score is already 0-100
- Result is capped at 100.0 maximum

---

## 🗂️ PART 8 — Data Flow (What Data Looks Like at Each Stage)

### Stage 1: Raw PDF Upload
```
Input: [john_doe.pdf, jane_smith.pdf, bob_wilson.pdf]
Output: Files saved to temp_resumes/ folder
```

### Stage 2: After PDF Parsing
```
Input: john_doe.pdf (binary PDF file)
Output: "John Doe\njohn@gmail.com\n+91 9876543210\n
         Python Developer with 5 years experience...\n
         Skills: Python, Machine Learning, AWS, Docker\n
         B.Tech Computer Science 2019"
```

### Stage 3: After Embedding
```
Input: "Python Developer with 5 years experience..."
Output: [0.121, -0.342, 0.876, 0.234, -0.091, 0.445, ...]  (384 numbers)
```

### Stage 4: After Matching
```
Input: Resume vectors (array of 384 numbers) vs JD vector (384 numbers)
Output: similarity_scores = [0.85, 0.72, 0.91, 0.63, ...]
         (one score per resume, 0.0 to 1.0)
```

### Stage 5: After Scoring
```
Input: Resume text + JD text
Output: {
  "ats_score": 82.5,
  "matched_keywords": ["python", "machine learning", "aws"],
  "missing_keywords": ["docker", "kubernetes"],
  "sections_found": {"education": true, "experience": true, "skills": true, "contact": true}
}
```

### Stage 6: After Extraction
```
Input: Resume plain text
Output: {
  "name": "John Doe",
  "email": "john@gmail.com",
  "phone": "+91 9876543210",
  "skills": ["AWS", "Docker", "Machine Learning", "Python"],
  "education": ["B.Tech Computer Science"],
  "experience_years": "5+ years"
}
```

### Stage 7: After Ranking
```
Input: Unsorted list of candidates with scores
Output: [
  {"rank": 1, "name": "Bob Wilson",  "final_score": 91.2, ...},
  {"rank": 2, "name": "John Doe",    "final_score": 85.0, ...},
  {"rank": 3, "name": "Jane Smith",  "final_score": 72.4, ...}
]
```

### Stage 8: Final Output
```
Displayed in Streamlit dashboard
Saved to outputs/results.csv
Available for CSV download
```

---

## 🚀 PART 9 — How to Run This Project (Beginner Setup Guide)

### Prerequisites
You need **Python 3.10 or higher** installed on your computer.

### Step 1: Install all required libraries
```bash
pip install -r requirements.txt
```
This reads `requirements.txt` and installs every library the project needs. It's like a shopping list — `pip` is the delivery service that brings everything to your computer.

⚠️ **Note:** `torch` (PyTorch) is a large download (~800MB). The first install takes several minutes.

### Step 2: Start the Backend (Terminal 1)
Open a terminal, navigate to the `Resume_project` folder, and run:
```bash
uvicorn main:app --reload --port 8000
```
You should see: `Uvicorn running on http://127.0.0.1:8000`

### Step 3: Start the Frontend (Terminal 2)
Open a **second** terminal window (keep the first one running), and run:
```bash
streamlit run ui/app.py --server.port 8501
```
Your browser should automatically open to `http://localhost:8501`.

### Step 4: Use the Project
1. Upload PDF resumes using the file uploader
2. Paste a job description in the text box
3. Click "🚀 Process & Rank Candidates"
4. Wait a few seconds (first run is slower — downloads the AI model)
5. See your ranked results!
6. Click "📥 Download Results as CSV" to save to Excel

---

## 🏆 PART 10 — Why This Architecture? The Big Design Decisions

### Decision 1: Why separate Frontend and Backend?

**The backend (FastAPI) and frontend (Streamlit) are two separate programs** that talk to each other via HTTP.

**Why not combine them into one program?**
- **Separation of concerns.** The backend only worries about data processing. The frontend only worries about display. Each can be improved independently.
- **The backend can be used by multiple frontends.** Someone could build a mobile app, a different web UI, or a command-line tool — all using the same FastAPI backend.
- **Industry standard pattern.** Every professional software product uses this architecture.
- **Testability.** You can test the backend by itself (using `/docs` or tools like Postman) without needing the UI.

### Decision 2: Why in-memory state (no database)?

The project stores job descriptions and results in Python variables (`state.job_description`, `state.results`) rather than a database like PostgreSQL or SQLite.

**Why not a real database?**
- This is a **local tool**, not a multi-user web application. One HR manager runs it on their laptop.
- Results only need to last for one session (upload → process → download CSV → done)
- A database would add significant complexity (setup, migrations, queries) with no benefit
- The CSV file in `outputs/` serves as persistent storage if you need to reference results later

### Decision 3: Why modular folder structure?

Each processing step is in its own folder (`ingestion/`, `parsing/`, etc.) rather than one big file.

**Why not one big `main.py` with all code?**
- **Readability.** Finding "how does matching work?" → open `matching/matcher.py`. Simple.
- **Team collaboration.** Different developers can work on different modules without conflicts.
- **Testability.** Each module can be tested independently.
- **Reusability.** The `embedder.py` module could be used in a completely different project.

### Decision 4: Why 60/40 split for the Final Score?

Similarity (AI) × 60% + ATS (rules) × 40%

**Why not 100% AI or 100% rules?**
- **100% AI only:** A resume could sound very similar to the JD (good writing) but lack key technical skills listed in the JD. ATS keyword matching catches this.
- **100% ATS rules only:** A resume could have the right keywords but use them in the wrong context ("I am learning Python" vs "5 years of Python"). AI similarity understands context better.
- **60/40 balance:** Tested and found to give the most fair results for technical job matching.

---

## 📋 PART 11 — Complete Technology Reference Card

| Technology | Category | Version | Purpose in Project |
|---|---|---|---|
| Python | Language | 3.10+ | Everything is written in Python |
| FastAPI | Web Framework | ≥0.115 | Backend API server with 6 endpoints |
| Uvicorn | Server | ≥0.30 | Runs FastAPI, handles connections |
| Streamlit | UI Framework | ≥1.38 | Browser-based user interface |
| PyMuPDF (fitz) | PDF Library | ≥1.24 | Extracts text from PDF resumes |
| sentence-transformers | AI Library | ≥3.0 | Converts text to AI embedding vectors |
| all-MiniLM-L6-v2 | AI Model | latest | 80MB neural network for text understanding |
| PyTorch | Deep Learning | ≥2.0 | Runs neural network computations |
| FAISS (faiss-cpu) | Vector Search | ≥1.8 | Finds most similar resumes to JD |
| NumPy | Math Library | ≥1.26 | Numerical arrays, vector math |
| Pandas | Data Library | ≥2.2 | Results tables, CSV operations |
| requests | HTTP Client | ≥2.32 | Streamlit calls FastAPI endpoints |
| python-multipart | Form Parser | ≥0.0.9 | FastAPI handles file upload data |
| re (regex) | Built-in | Python stdlib | Extracts emails, phones, patterns |

---

## 🎓 PART 12 — Key Concepts Glossary (Plain English Definitions)

| Term | Plain English Definition |
|---|---|
| **API** | A set of rules for how two programs talk to each other. Like a waiter who takes your order (request) to the kitchen (server) and brings back your food (response). |
| **Endpoint** | A specific "door" on an API. `/api/upload` is one door, `/api/process` is another. |
| **HTTP** | The language of the internet. GET = "give me data", POST = "here's data, do something with it", DELETE = "remove something". |
| **JSON** | A format for sending data between programs. Looks like: `{"name": "John", "score": 85}`. |
| **Embedding** | A list of numbers that represents the meaning of text. Similar texts → similar numbers. |
| **Vector** | A list of numbers. A 384-dimensional vector is just a list of 384 numbers. |
| **Cosine Similarity** | A math formula that measures how similar two vectors (lists of numbers) are. Returns 0.0 (completely different) to 1.0 (identical). |
| **ATS** | Applicant Tracking System. Software companies use to automatically filter resumes. |
| **Regex** | A pattern language for searching text. `\d{10}` means "10 consecutive digits" (phone number). |
| **Singleton** | Only one instance exists. The AI model loads once and is reused, not re-loaded every time (saves time and memory). |
| **Batch processing** | Processing many items together instead of one at a time. Faster for embedding many resumes. |
| **localhost** | Your own computer, accessed via browser. `localhost:8000` = "door 8000 on this computer." |
| **Port** | A numbered "door" on a computer. Programs listen on specific ports. Browser default is 80/443. |
| **CSV** | Comma-Separated Values. A simple spreadsheet format. Opens in Excel. |
| **PDF** | Portable Document Format. The standard format for sharing formatted documents. |
| **Transformer** | A type of neural network architecture (invented by Google in 2017) that powers most modern AI language models including ChatGPT. |
| **Pre-trained model** | An AI model that was already trained by someone else on millions of documents. We reuse it without retraining. |

---

## 🔚 FINAL SUMMARY — The Complete Picture

Here is the entire project in one paragraph:

> **The AI Resume Shortlister is a two-part application. The first part is a FastAPI backend server that exposes 6 API endpoints. The second part is a Streamlit frontend that users interact with in their browser. When a user uploads resume PDFs and enters a job description, Streamlit sends them to FastAPI. FastAPI then runs an 8-step pipeline: (1) saves the files with ingestion/upload.py, (2) extracts text from PDFs using PyMuPDF in parsing/parser.py, (3) converts all text to 384-dimensional AI vectors using the all-MiniLM-L6-v2 model via sentence-transformers in embeddings/embedder.py, (4) compares all resume vectors to the job description vector using FAISS in matching/matcher.py, (5) calculates keyword/section/length/format ATS scores and combines with similarity for a final score in scoring/scorer.py, (6) extracts structured info (name, email, skills) using regex in extraction/extractor.py, (7) sorts all candidates by final score in ranking/ranker.py, and (8) saves a CSV and returns the ranked list to Streamlit. Streamlit then displays the results as beautiful cards or a table, with green for shortlisted candidates and download button for the CSV.**

---

*This guide was written so that anyone — regardless of technical background — can fully understand what this project is, how it works, and why it was built the way it was.*

---

---

# 🔬 PART 13 — EVERY FILE EXPLAINED IN FULL DETAIL
### *How each file works, what every function does, and exactly how each piece contributes to the pipeline*

> **Purpose of this section:**
> Every module folder, every file inside it, every function — explained step by step
> in plain English. By the end you will know exactly what happens when the project runs,
> file by file, function by function.

---

## 📌 FIRST: UNDERSTANDING `__init__.py` FILES

Every module folder (`ingestion/`, `parsing/`, `embeddings/`, etc.) contains a file called `__init__.py`. Before diving into individual modules, let's understand why.

### What is `__init__.py`?

Python treats a folder as a **"package"** (a reusable collection of code) only when that folder contains a file called `__init__.py`. Without this file, Python cannot import anything from that folder.

Think of a Python package like a shop in a mall. The Python interpreter walks through the mall. It only enters shops that have an **"Open for Business"** sign on the door. The `__init__.py` file IS that sign.

**How it matters in this project:**

In `main.py`, these import lines work **because** every module folder has `__init__.py`:
```python
from ingestion.upload import save_resume          # works because ingestion/__init__.py exists
from parsing.parser import extract_text_from_pdf  # works because parsing/__init__.py exists
from embeddings.embedder import generate_embedding # works because embeddings/__init__.py exists
from matching.matcher import match_resumes_to_job  # works because matching/__init__.py exists
from scoring.scorer import calculate_ats_score     # works because scoring/__init__.py exists
from extraction.extractor import extract_all       # works because extraction/__init__.py exists
from ranking.ranker import rank_candidates         # works because ranking/__init__.py exists
```

**What happens if you delete one?**
Delete `embeddings/__init__.py` → `main.py` crashes immediately with:
`ModuleNotFoundError: No module named 'embeddings'`
The entire project stops working.

**All 8 `__init__.py` files in this project:**

| File | Content | Job |
|---|---|---|
| `ingestion/__init__.py` | `# Ingestion module - handles file upload and storage` | Makes `ingestion/` importable |
| `parsing/__init__.py` | `# Parsing module - PDF to text conversion` | Makes `parsing/` importable |
| `embeddings/__init__.py` | `# Embeddings module - text to vector conversion` | Makes `embeddings/` importable |
| `matching/__init__.py` | `# Matching module - resume vs job similarity` | Makes `matching/` importable |
| `scoring/__init__.py` | `# Scoring module - ATS and final score calculation` | Makes `scoring/` importable |
| `extraction/__init__.py` | `# Extraction module - structured info extraction from resumes` | Makes `extraction/` importable |
| `ranking/__init__.py` | `# Ranking module - sort candidates by score` | Makes `ranking/` importable |
| `ui/__init__.py` | `# UI module - Streamlit dashboard` | Makes `ui/` importable |

These are deliberately kept minimal — just a comment. Their entire purpose is to exist so Python recognizes the folder as a package.

---

## 📂 MODULE 1 — `ingestion/` — The Receptionist

**Pipeline Role:** STEP 1 of 8. Receives uploaded PDF files and saves them to disk. Also provides the list of saved files to the pipeline and cleans up when done.

**Real-world analogy:** A hotel receptionist takes a guest's luggage (uploaded PDF), stores it safely in a room (`temp_resumes/`), can retrieve a list of all stored luggage (`get_all_resumes()`), and clears the room when the guest checks out (`cleanup_temp()`).

---

### 📄 `ingestion/__init__.py`
One line: `# Ingestion module - handles file upload and storage`
Marks the folder as a Python package. No logic here.

---

### 📄 `ingestion/upload.py` — Full Breakdown

**Why this file exists:**
The project needs a dedicated place to handle all file system operations. Every other module works purely with text or numbers — none of them should have to worry about *where* files are stored, *how* to create folders, or *how* to delete temporary data. `upload.py` owns all of that complexity so the rest of the project stays clean.

---

**The Imports:**
```python
import os
import shutil
from pathlib import Path
```
- **`os`** — Python's built-in operating system interface. Lets you check if files/folders exist, get file sizes, work with environment variables.
- **`shutil`** — Built-in "shell utility" module. Provides high-level file operations. Here it's used for `shutil.rmtree()` which deletes an entire folder tree (like right-clicking → Delete on a folder with all contents).
- **`pathlib.Path`** — Modern Python way to work with file system paths. The `/` operator joins paths cross-platform: `BASE_DIR / "temp_resumes"` works on Windows (`\`), Mac (`/`), and Linux (`/`) automatically. Much safer than string concatenation.

---

**The Constants:**
```python
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / "temp_resumes"
OUTPUT_DIR = BASE_DIR / "outputs"
```

Step by step what `BASE_DIR` does:
- `__file__` — A special Python variable. Its value is the path of the current script file. Here: `".../Resume_project/ingestion/upload.py"`
- `Path(__file__)` — Wraps that string as a `Path` object so we can call path methods on it
- `.resolve()` — Converts to an absolute path (removes any `../` or relative parts)
- `.parent` — Moves one directory up: from `ingestion/` → `Resume_project/ingestion` → `Resume_project/`
- `.parent` again — Wait, one `.parent` already gives `Resume_project/`. Let's be precise: `.parent` on `upload.py`'s path gives `ingestion/` directory. `.parent.parent` gives `Resume_project/` directory.

Result: `BASE_DIR = Resume_project/`

- `TEMP_DIR = BASE_DIR / "temp_resumes"` → `Resume_project/temp_resumes/`
- `OUTPUT_DIR = BASE_DIR / "outputs"` → `Resume_project/outputs/`

**Why constants instead of hardcoded strings?** If you ever move the project, these paths auto-adjust. If you hardcoded `"C:/AI_RESUME_SHORTLISTER/Resume_project/temp_resumes/"`, it would break on any other machine.

---

**Function 1: `ensure_directories()`**
```python
def ensure_directories():
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```
**What it does:** Creates `temp_resumes/` and `outputs/` folders if they don't already exist.

**Parameter meanings:**
- `parents=True` → If parent directories are also missing, create them too. Like `mkdir -p` in Linux or creating nested folders in one go.
- `exist_ok=True` → If the folder already exists, do nothing (don't throw an error). Without this, calling `mkdir()` on an existing folder crashes with `FileExistsError`.

**Why it's called everywhere:** On a fresh clone of the project, neither folder exists. If `save_resume()` tried to write a file into `temp_resumes/` before the folder was created, Python would throw `FileNotFoundError`. By calling `ensure_directories()` before every file operation, this situation is impossible.

**Who calls it:**
- `save_resume()` calls it before writing
- `get_all_resumes()` calls it before scanning
- `main.py`'s `lifespan` startup event calls it once when the server starts

---

**Function 2: `save_resume(file_bytes, filename)`**
```python
def save_resume(file_bytes: bytes, filename: str) -> str:
    ensure_directories()
    filepath = TEMP_DIR / filename
    with open(filepath, "wb") as f:
        f.write(file_bytes)
    return str(filepath)
```
**What it does:** Takes the raw binary data of an uploaded PDF and writes it to a file on disk.

**Breaking it down:**
- `file_bytes: bytes` — When FastAPI receives an uploaded file, it arrives as `bytes` (raw binary data — the actual 0s and 1s of the PDF). This parameter holds that data.
- `filename: str` — The original name the user gave the file (e.g., `"john_doe_resume.pdf"`).
- `filepath = TEMP_DIR / filename` → Full path becomes `Resume_project/temp_resumes/john_doe_resume.pdf`
- `open(filepath, "wb")` — Opens a file for **writing** in **binary mode**.
  - `"w"` = write mode (creates file or overwrites)
  - `"b"` = binary mode (don't interpret data as text — PDFs are binary, not plain text)
- `f.write(file_bytes)` — Writes every byte of the PDF into the file
- `with open(...) as f:` — The `with` statement automatically closes the file when done, even if an error occurs
- `return str(filepath)` — Returns the full disk path as a string so `main.py` can pass it to the parser

**What is returned:** `"C:/AI_RESUME_SHORTLISTER/Resume_project/temp_resumes/john_doe_resume.pdf"`

**What happens in `main.py`:**
```python
path = save_resume(content, f.filename)
saved.append({"filename": f.filename, "path": path})
```
The returned path is stored and later used by `extract_text_from_pdf(path)` in the parsing step.

---

**Function 3: `get_all_resumes()`**
```python
def get_all_resumes() -> list:
    ensure_directories()
    return [str(f) for f in TEMP_DIR.glob("*.pdf")]
```
**What it does:** Scans the `temp_resumes/` folder and returns the file paths of every PDF found there.

**`TEMP_DIR.glob("*.pdf")`:**
- `glob()` is a pattern-matching file finder
- `"*.pdf"` means: match any filename that ends with `.pdf`
- Returns a generator of `Path` objects matching the pattern

**`[str(f) for f in ...]`** — A "list comprehension": converts each `Path` object to a plain string. Result is a list of string paths.

**Why this function instead of hardcoding filenames?** `main.py` doesn't know how many files were uploaded or what they're named. It just calls `get_all_resumes()` and gets the complete list. The pipeline then works on every PDF found.

**What is returned:** `["...temp_resumes/john.pdf", "...temp_resumes/jane.pdf", "...temp_resumes/bob.pdf"]`

---

**Function 4: `cleanup_temp()`**
```python
def cleanup_temp():
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    print("[DONE] Temporary files cleaned up.")
```
**What it does:** Deletes ALL uploaded PDFs and recreates a clean empty `temp_resumes/` folder.

**Why delete AND recreate:**
- `shutil.rmtree(TEMP_DIR)` removes the folder AND everything inside it
- Without immediately calling `mkdir()` again, the next upload attempt would fail (no folder to write into)
- So we destroy everything and rebuild the empty container immediately

**Who triggers this:** The `DELETE /api/cleanup` endpoint in `main.py`, which is called by the "🗑️ Clear All Data" button in the Streamlit sidebar. Also resets `state.job_description` and `state.results` in `main.py`.

---

## 📂 MODULE 2 — `parsing/` — The Reader

**Pipeline Role:** STEP 2 of 8. Opens each PDF file saved by ingestion and converts it into plain readable text that the rest of the pipeline can work with.

**Real-world analogy:** A professional typist who can open any PDF book, read every page, and type out the entire content as plain text — removing all formatting, colors, fonts, images, and decorations. Only the raw words remain.

**Why text extraction is non-trivial:**
A PDF file is NOT a text file. A PDF stores content as a mix of:
- Text with font embedding instructions
- Vector drawings and shapes
- Raster images
- Page layout coordinates
- Metadata (author, creation date, etc.)

You cannot `open("resume.pdf", "r").read()` and get meaningful text. You need a library that understands the PDF specification and can extract just the text layer.

---

### 📄 `parsing/__init__.py`
One line: `# Parsing module - PDF to text conversion`
Marks `parsing/` as a Python package. No logic.

---

### 📄 `parsing/parser.py` — Full Breakdown

**Why this file exists:**
`parser.py` is the single point in the entire project that deals with PDFs. Every other module receives plain text — the messy PDF-reading problem is entirely contained here. If you ever wanted to support DOCX files or web-scraped text, you'd add a new function here without touching anything else.

---

**The Import:**
```python
import fitz  # PyMuPDF
```
- The PyMuPDF library installs as `PyMuPDF` (that's the package name in `requirements.txt`) but it is imported using the name `fitz` (its historical internal name from the "MuPDF" C library it wraps).
- `fitz` provides `Document`, `Page`, and other classes for working with PDF files programmatically.

---

**Function 1: `extract_text_from_pdf(pdf_path)`**
```python
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"[ERROR] Error reading PDF '{pdf_path}': {e}")
        return ""
    return text.strip()
```
**What it does:** Opens a PDF from its file path on disk, reads every page, and returns all text as one combined string.

**Step-by-step breakdown:**
1. `text = ""` — Start with an empty text accumulator
2. `fitz.open(pdf_path)` — Opens the PDF file. Returns a `Document` object (like an opened book). PyMuPDF reads the file header, page tree, and content streams.
3. `for page in doc:` — Iterates through each page of the document (page 1, 2, 3...)
4. `page.get_text()` — Extracts all text from that single page. PyMuPDF reads the content stream, interprets the text drawing operations, and returns the visible text characters in reading order.
5. `text += page.get_text()` — Appends each page's text to the accumulator. Multi-page resumes are handled naturally by this loop.
6. `doc.close()` — Releases the file handle back to the OS. Good practice to avoid memory leaks when processing many files.
7. `try/except Exception as e:` — The most important safety net in the project. If ANYTHING goes wrong reading this PDF (corrupted file, password-protected, image-only scan, empty file, wrong encoding), the exception is caught, an error is printed, and `""` (empty string) is returned. **The pipeline continues with the other resumes — one bad file doesn't crash everything.**
8. `return text.strip()` — `.strip()` removes leading and trailing whitespace/newlines from the final combined text.

**What is returned (example):**
```
John Doe
john.doe@email.com  |  +91 9876543210  |  linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Python Developer with 5 years of experience in Machine Learning and NLP...

TECHNICAL SKILLS
Python, TensorFlow, PyTorch, AWS, Docker, Kubernetes, SQL, Git

WORK EXPERIENCE
Senior ML Engineer — TechCorp (Jan 2021 – Present)
  • Developed NLP pipeline processing 1M+ documents daily...

EDUCATION
B.Tech Computer Science — IIT Delhi — 2019 — CGPA: 8.7
```

**Who calls this:** `main.py`'s `process_resumes()` function:
```python
for path in resume_paths:
    text = extract_text_from_pdf(path)
    if text:                           # ← only process if text was extracted
        resume_texts.append(text)
        valid_paths.append(path)
```

---

**Function 2: `extract_text_from_bytes(pdf_bytes)`**
```python
def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"[ERROR] Error reading PDF bytes: {e}")
        return ""
    return text.strip()
```
**What it does:** Identical logic to `extract_text_from_pdf()` but takes raw bytes in memory instead of a file path.

**The key difference:**
- `fitz.open(pdf_path)` — Reads from a file on disk
- `fitz.open(stream=pdf_bytes, filetype="pdf")` — Reads from bytes in RAM. `stream=` tells PyMuPDF "here is the raw data," `filetype="pdf"` tells it how to interpret those bytes.

**Why this function exists:** Provides an alternative code path for processing PDFs that are still in memory (never written to disk). The current pipeline saves files first then reads them with `extract_text_from_pdf()`, but `extract_text_from_bytes()` is available if the architecture is ever changed to be fully in-memory (faster, avoids disk I/O).

---

## 📂 MODULE 3 — `embeddings/` — The AI Translator

**Pipeline Role:** STEP 3 of 8. The most technically sophisticated step. Converts raw text into 384-dimensional mathematical vectors using a pre-trained neural network. These vectors encode the **semantic meaning** of the text.

**Real-world analogy:** Imagine a Universal Translator that can convert any sentence into a unique "meaning fingerprint" — a list of 384 numbers. Two sentences that mean the same thing (like "Python developer" and "software programmer") produce almost identical fingerprints. Two sentences that mean very different things produce very different fingerprints. The AI model IS this translator.

**Why numerical vectors instead of text comparison?**
Text comparison (looking for exact word matches) is brittle:
- "Python developer" vs "Python programmer" → 0% word overlap (only "Python" matches) but they mean nearly the same thing
- "I am not experienced in Python" vs "Python experience required" → "Python" and "experience" match but they mean OPPOSITE things

Embeddings solve both problems by encoding meaning into a geometric space where semantically similar texts point in the same mathematical direction.

---

### 📄 `embeddings/__init__.py`
One line: `# Embeddings module - text to vector conversion`
Marks `embeddings/` as a Python package.

---

### 📄 `embeddings/embedder.py` — Full Breakdown

**Why this file exists:**
Two separate modules need AI embeddings — resumes need `generate_embeddings_batch()` and the job description needs `generate_embedding()`. Centralizing model loading and embedding generation in one file means: (1) the expensive model load happens only once, (2) the embedding logic is maintained in one place.

---

**The Imports:**
```python
import numpy as np
from sentence_transformers import SentenceTransformer
```
- **`numpy as np`** — The output of `model.encode()` needs to be converted to a NumPy array with `float32` precision because that is exactly the format FAISS requires for its index.
- **`SentenceTransformer`** — The main class from the `sentence-transformers` library. It wraps a pre-trained Transformer neural network and exposes a simple `.encode(text)` API.

---

**The Singleton Variable:**
```python
_model = None
```
This module-level variable starts as `None` (model not yet loaded). It will hold the loaded model after first use.

**What is a singleton?** A design pattern that ensures only ONE instance of an object ever exists. The leading underscore `_model` is Python convention for "this is a private variable, not for external use."

**Why a singleton for the AI model?**
- Loading `all-MiniLM-L6-v2` takes 3–8 seconds and uses ~200MB of RAM
- If the model were reloaded on every embedding call, processing 50 resumes = loading the model 51 times = 150–400 seconds of pure loading time
- With the singleton: load once on first call (~5 seconds), reuse 51 times instantly (milliseconds each)

---

**Function 1: `get_model()`**
```python
def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print("[LOADING] Loading embedding model (all-MiniLM-L6-v2)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("[DONE] Model loaded successfully.")
    return _model
```
**What it does:** Implements the singleton pattern. Loads the model on first call, returns cached model on all subsequent calls.

**Breaking it down:**
- `global _model` — Tells Python: "When I say `_model` in this function, I mean the module-level variable, not a local one." Without `global`, assigning `_model = ...` inside the function would create a local variable that disappears after the function returns.
- `if _model is None:` — Only enters this block on the very first call (when model hasn't been loaded yet)
- `SentenceTransformer("all-MiniLM-L6-v2")` — This single line:
  1. Checks if the model exists in local cache (`~/.cache/huggingface/`)
  2. If not: downloads ~80MB of model weights from HuggingFace Hub (requires internet, first run only)
  3. Loads the model into RAM
  4. Returns a ready-to-use `SentenceTransformer` object
- Second call: `_model` is no longer `None`, skips loading, returns immediately

**Who calls it:** `generate_embedding()` and `generate_embeddings_batch()` both start with `model = get_model()`.

---

**Function 2: `generate_embedding(text)`**
```python
def generate_embedding(text: str) -> np.ndarray:
    model = get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return np.array(embedding, dtype=np.float32)
```
**What it does:** Converts a single text string into a 384-dimensional numerical vector.

**Breaking it down:**
- `model.encode(text, normalize_embeddings=True)`:
  - `encode()` runs the text through the neural network's 6 transformer layers
  - The network processes each word in context of every other word (the "attention" mechanism)
  - The output is a 384-number vector representing the text's meaning in "semantic space"
  - `normalize_embeddings=True` — Scales the vector to unit length (L2 norm = 1.0). **Critical for FAISS.** When vectors are L2-normalized, the Inner Product (dot product) between two vectors equals their Cosine Similarity. This means FAISS's `IndexFlatIP` gives us cosine similarity scores directly.
- `np.array(embedding, dtype=np.float32)` — Converts to NumPy float32 array. FAISS requires `float32` specifically (not `float64`). Using the wrong type would cause a FAISS error.

**What is returned:** A NumPy array of shape `(384,)` — 384 floating-point numbers.

**Example (conceptual):**
```
"Python Machine Learning Engineer"  →  [0.121, -0.342, 0.876, 0.234, -0.091, ...]
"Java Backend Developer"            →  [-0.234, 0.456, -0.123, 0.678, 0.345, ...]
"ML Python Scientist"               →  [0.118, -0.338, 0.871, 0.229, -0.089, ...]
```
Notice the first and third (semantically similar) produce very similar number lists.

**Who calls this:** `main.py`: `jd_embedding = generate_embedding(state.job_description)` — called once for the job description.

---

**Function 3: `generate_embeddings_batch(texts)`**
```python
def generate_embeddings_batch(texts: list) -> np.ndarray:
    model = get_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    return np.array(embeddings, dtype=np.float32)
```
**What it does:** Converts a list of text strings into embeddings all at once using batch processing.

**Why batch is much faster than a loop:**
- Individual calls: The model processes one text, produces output, waits, processes next text... Serial execution.
- Batch call: The model receives ALL texts at once and processes them together using matrix operations on all CPU cores simultaneously. Batch is typically 5–15x faster.

**`show_progress_bar=True`** — When processing many resumes, this prints a live progress bar to the terminal so you can see it's working (not frozen).

**What is returned:** A 2D NumPy array of shape `(num_resumes, 384)`. Each row is one resume's embedding.

**Visual:**
```
resumes = ["John Doe resume text...", "Jane Smith resume text...", "Bob Wilson resume text..."]

Result shape: (3, 384)
[
  [0.121, -0.342, 0.876, ...],   ← John's embedding (384 numbers)
  [0.234, -0.123, 0.654, ...],   ← Jane's embedding (384 numbers)
  [0.087, -0.456, 0.912, ...],   ← Bob's embedding  (384 numbers)
]
```

**Who calls this:** `main.py`: `resume_embeddings = generate_embeddings_batch(resume_texts)` — called once for all resumes together.

---

## 📂 MODULE 4 — `matching/` — The Comparator

**Pipeline Role:** STEP 4 of 8. Takes all resume vectors and the JD vector, then measures how similar each resume is to the JD. Produces one similarity score (0.0–1.0) per resume.

**Analogy:** You have a target color (the JD's meaning vector) and 50 paint samples (resume vectors). The comparator precisely measures how close each paint sample is to the target — giving a percentage match for each.

**Core concept — Cosine Similarity:** Two vectors are like arrows in space. Cosine similarity measures the angle between them. Same direction → 1.0 (100% match). 90° apart → 0.0 (unrelated). Because embeddings represent meaning, resumes about similar topics to the JD point in similar directions → high similarity.

---

### 📄 `matching/__init__.py`
`# Matching module - resume vs job similarity` — marks the folder as a package.

---

### 📄 `matching/matcher.py` — Full Breakdown

**The Imports:**
```python
import numpy as np
import faiss
```
- `numpy` — Handles the embedding arrays passed in and used internally
- `faiss` — Facebook AI Similarity Search: builds a searchable vector index and finds similar vectors at high speed

---

**Function 1: `compute_cosine_similarity(vec_a, vec_b)`**
```python
def compute_cosine_similarity(vec_a, vec_b) -> float:
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))
```
**What it does:** Directly calculates cosine similarity between two vectors using the mathematical formula.

- `np.dot(vec_a, vec_b)` — Dot product: multiply each pair of corresponding numbers and sum. For 384-dim vectors: 384 multiplications + 383 additions.
- `np.linalg.norm(vec_a)` — Vector magnitude: `√(a₁² + a₂² + ... + a₃₈₄²)`
- `dot_product / (norm_a * norm_b)` — Divides by both magnitudes → removes length effect → pure directional similarity. Result: -1.0 to 1.0.
- Zero-vector guard: if either vector is all zeros, similarity is undefined → return 0.0 (avoids division-by-zero crash)

**When used:** Useful for direct single-pair comparison (testing, debugging). The main pipeline uses FAISS for bulk comparison.

---

**Function 2: `build_faiss_index(embeddings)`**
```python
def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index
```
**What it does:** Creates a searchable FAISS index from all resume embeddings.

**Think of it as:** Registering all resumes in a "meaning phonebook." Once registered (`index.add()`), you can look up "which resumes are closest to this JD?" in milliseconds.

- `embeddings.shape[1]` — Gets dimension 384 from the 2D array shape `(num_resumes, 384)`
- `faiss.IndexFlatIP(dim)`:
  - `Flat` = exact search (checks every vector, perfect accuracy). Suitable for up to ~100K vectors.
  - `IP` = Inner Product metric. For L2-normalized vectors (which we have), IP equals Cosine Similarity mathematically — so we get cosine similarity for free.
- `index.add(embeddings)` — Loads all resume vectors into FAISS memory, ready for searching

---

**Function 3: `search_similar(index, query_embedding, top_k=10)`**
```python
def search_similar(index, query_embedding, top_k=10):
    query = query_embedding.reshape(1, -1)
    k = min(top_k, index.ntotal)
    scores, indices = index.search(query, k)
    return scores[0], indices[0]
```
**What it does:** Searches the FAISS index for the K most similar resumes to the JD embedding.

- `query_embedding.reshape(1, -1)` — FAISS's `search()` expects a 2D array. Our JD embedding is `(384,)`. Reshape to `(1, 384)` = "a batch of 1 query." The `-1` means "compute this dimension automatically."
- `k = min(top_k, index.ntotal)` — Safety: if only 3 resumes exist but you ask for top 10, just return all 3.
- `index.search(query, k)` — **The FAISS magic.** Compares query against ALL stored vectors instantly. Returns `scores` (similarities, best first) and `indices` (original array positions), both 2D.
- `scores[0], indices[0]` — Extract single-query results from the batch format.

---

**Function 4: `match_resumes_to_job(resume_embeddings, job_embedding)` ← main pipeline function**
```python
def match_resumes_to_job(resume_embeddings, job_embedding) -> list:
    n = len(resume_embeddings)
    index = build_faiss_index(resume_embeddings)
    scores, indices = search_similar(index, job_embedding, top_k=n)
    result = [0.0] * n
    for score, idx in zip(scores, indices):
        if 0 <= idx < n:
            result[int(idx)] = round(float(score), 4)
    return result
```
**What it does:** Orchestrates the full matching process and re-maps FAISS results back to original resume order.

**Why re-mapping is critical:**
FAISS returns results sorted by similarity (best first). But `main.py` needs `result[0]` = john's score, `result[1]` = jane's score, `result[2]` = bob's score — matching the original upload order so each score can be paired with the correct resume.

**Concrete example:**
```
Upload order:  john(0), jane(1), bob(2)
FAISS output:  scores=[0.91, 0.85, 0.72], indices=[2, 0, 1]
               → bob(idx=2)=0.91, john(idx=0)=0.85, jane(idx=1)=0.72

Re-mapping:
  result[2] = 0.91   ← bob at his original position
  result[0] = 0.85   ← john at his original position
  result[1] = 0.72   ← jane at her original position

Final: [0.85, 0.72, 0.91]  ← john, jane, bob — original order ✓
```

**Who calls this:** `main.py`: `similarity_scores = match_resumes_to_job(resume_embeddings, jd_embedding)`

---

## 📂 MODULE 5 — `scoring/` — The Grader

**Pipeline Role:** STEP 5 of 8. Two jobs in one: (a) Calculate ATS score using rules, (b) Combine similarity + ATS into one Final Score per candidate.

**Analogy:** An exam with two parts — Part A is multiple choice (keyword match — did you have the skill or not?) and Part B is an essay scored holistically (AI similarity — does this resume overall match?). Final grade = weighted average of both parts.

---

### 📄 `scoring/__init__.py`
`# Scoring module - ATS and final score calculation` — marks the folder as a package.

---

### 📄 `scoring/scorer.py` — Full Breakdown

**The Import:**
```python
import re
```
`re` — Python's built-in Regular Expressions module. Used in the formatting check section to detect email and phone patterns.

---

**The `SKILL_KEYWORDS` Database:**
A list of ~60 skill keywords (all lowercase) covering:
- Programming languages: `"python"`, `"java"`, `"javascript"`, `"sql"`, etc.
- AI/ML: `"machine learning"`, `"deep learning"`, `"nlp"`, `"tensorflow"`, etc.
- Cloud: `"aws"`, `"azure"`, `"gcp"`, `"docker"`, `"kubernetes"`
- Databases: `"mongodb"`, `"postgresql"`, `"redis"`, etc.
- Soft skills: `"leadership"`, `"communication"`, `"teamwork"`, `"agile"`

**Why all lowercase?** The comparison function lowercases all text before searching. Storing keywords lowercase means direct string matching — no extra `.lower()` call needed per keyword during comparison.

**This list is the ATS "answer key."** Without it, there's nothing to compare against. If a required skill like `"docker"` is not in this list, the ATS scorer will never detect it even if it's in both the JD and resume.

---

**Function 1: `extract_keywords(text)`**
```python
def extract_keywords(text: str) -> list:
    text_lower = text.lower()
    return [kw for kw in SKILL_KEYWORDS if kw in text_lower]
```
- Converts the entire input text to lowercase once (efficient — one conversion, not one per keyword)
- For each keyword in the master list, checks if it appears as a substring in the text
- Returns only the keywords that were found

**Example:** Input: `"Need Python + AWS + Docker experience"` → Output: `["python", "aws", "docker"]`

---

**Function 2: `calculate_ats_score(resume_text, jd_text)` ← most detailed function**

Has 4 independent scoring sections:

**Section A — Keyword Match (60% weight):**
```python
jd_keywords = extract_keywords(jd_text)
resume_keywords = extract_keywords(resume_text)
if jd_keywords:
    matched = [kw for kw in jd_keywords if kw in resume_keywords]
    missing = [kw for kw in jd_keywords if kw not in resume_keywords]
    keyword_score = (len(matched) / len(jd_keywords)) * 100
else:
    matched, missing = [], []
    keyword_score = 50.0
```
- `jd_keywords` = what the JD requires. `resume_keywords` = what the resume claims.
- `matched` = skills the candidate HAS that the job NEEDS
- `missing` = skills the job NEEDS that the candidate LACKS
- Score = `(matched count / total JD keywords) × 100`
- If JD has no recognized keywords → default to 50 (neutral, fair for generic JDs)
- **`matched` and `missing` are stored in the candidate record and displayed in the UI's expandable details.**

**Section B — Section Presence (20% weight):**
```python
sections = {
    "education": any(s in resume_lower for s in ["education","degree","university","college","bachelor","master"]),
    "experience": any(s in resume_lower for s in ["experience","work history","employment","worked at","intern"]),
    "skills": any(s in resume_lower for s in ["skills","technical skills","technologies","proficient"]),
    "contact": any(s in resume_lower for s in ["email","phone","@","linkedin"]),
}
section_score = (sum(sections.values()) / len(sections)) * 100
```
- Checks for the 4 essential sections every professional resume should have
- `any(s in resume_lower for s in [...])` — True if ANY trigger word for that section appears
- Score = `(sections found / 4) × 100` — 4/4 = 100%, 3/4 = 75%, 2/4 = 50%, etc.

**Section C — Resume Length (10% weight):**
```python
word_count = len(resume_text.split())
if 200 <= word_count <= 1000:    length_score = 100.0
elif 100 <= word_count <= 1500:  length_score = 70.0
else:                             length_score = 40.0
```
- `resume_text.split()` splits text on whitespace → list of words → `len()` counts them
- 200-1000 words: ideal (enough detail, not overwhelming) → 100 points
- 100-200 or 1000-1500 words: acceptable → 70 points
- Below 100 or above 1500: too sparse or too long → 40 points

**Section D — Formatting Basics (10% weight):**
```python
has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', resume_text))
has_phone = bool(re.search(r'[\+]?[\d\s\-\(\)]{10,}', resume_text))
format_score = ((int(has_email) + int(has_phone)) / 2) * 100
```
- Checks if resume has an email address (regex pattern: `something@something.something`)
- Checks if resume has a phone number (regex: 10+ consecutive digit characters, possibly with spaces/dashes)
- Score: 100 if both present, 50 if only one, 0 if neither

**Final ATS calculation:**
```python
ats_score = round(
    keyword_score * 0.60 + section_score * 0.20
    + length_score * 0.10 + format_score * 0.10, 1
)
return {"ats_score": min(ats_score, 100.0), "matched_keywords": matched, "missing_keywords": missing, ...}
```
Weighted sum of the 4 components, capped at 100.

**What is returned:** A dictionary containing `ats_score`, `matched_keywords`, `missing_keywords`, `sections_found`, `keyword_score`, and `word_count`.

**Who calls this:** `main.py` per resume: `ats_result = calculate_ats_score(text, state.job_description)`

---

**Function 3: `calculate_final_score(similarity_score, ats_score, similarity_weight=0.6, ats_weight=0.4)`**
```python
def calculate_final_score(similarity_score, ats_score, similarity_weight=0.6, ats_weight=0.4) -> float:
    sim_scaled = similarity_score * 100
    final = round(sim_scaled * similarity_weight + ats_score * ats_weight, 1)
    return min(final, 100.0)
```
**What it does:** The master formula that combines the AI score and the ATS score into one final ranking number.

- `similarity_score * 100` — Converts similarity from 0.0–1.0 scale to 0–100 scale (to match ATS scale)
- `sim_scaled * 0.6 + ats_score * 0.4` — Weighted average: 60% AI + 40% rules
- `min(final, 100.0)` — Safety cap at 100 (floating point might produce 100.000001 sometimes)
- Default weights are parameters: you could change the balance by passing `similarity_weight=0.5, ats_weight=0.5` without modifying the function

**Why 60/40 split?** AI similarity understands context and meaning better (worth more) but ATS keyword matching catches missing skills the AI might overlook (still important). 60/40 is the balance that gives fair, comprehensive ranking.

**Who calls this:** `main.py`: `final_score = calculate_final_score(similarity_scores[i], ats_result["ats_score"])`

---

## 📂 MODULE 6 — `extraction/` — The Detective

**Pipeline Role:** STEP 6 of 8. Extracts specific structured data points from raw resume text: name, email, phone, skills, education, and years of experience.

**Analogy:** A detective examining a crime scene. The scene is the raw resume text. The detective identifies specific clues: "Here's a phone number. Here's an email. Here are the skills listed. Here's a degree." No AI needed — just sharp pattern-recognition rules.

**Why not AI for this?** Because the patterns are highly structured and predictable. An email address always looks like `x@y.z`. A phone number is always 10+ digits. Using an AI model (like a named entity recognition model) would add 200MB+ of model files and seconds of processing time for tasks that 10 lines of regex can handle in microseconds.

---

### 📄 `extraction/__init__.py`
`# Extraction module - structured info extraction from resumes` — marks the folder as a package.

---

### 📄 `extraction/extractor.py` — Full Breakdown

**The Import:**
```python
import re
```
`re` — Python's built-in Regular Expressions module. Every extraction function uses this to search for text patterns.

---

**The `KNOWN_SKILLS` Database:**
A list of ~80 skills in proper casing (e.g., `"Python"`, `"TensorFlow"`, `"AWS"`, `"Node.js"`) covering:
- Programming: Python, Java, JavaScript, TypeScript, C++, C#, Ruby, Go, Rust, Scala, Kotlin, Swift, PHP, SQL, HTML, CSS
- Frameworks: React, Angular, Vue, Node.js, Django, Flask, FastAPI, Spring, Express
- AI/ML: Machine Learning, Deep Learning, NLP, TensorFlow, PyTorch, Keras, Scikit-learn, Pandas, NumPy, OpenCV, Transformers
- Cloud/DevOps: AWS, Azure, GCP, Docker, Kubernetes, CI/CD, Jenkins, Terraform, Ansible
- Databases: MongoDB, PostgreSQL, MySQL, Redis, Elasticsearch, Cassandra, SQLite
- Tools: Git, GitHub, Linux, REST API, GraphQL, Kafka, Spark, Airflow, Streamlit
- Soft skills: Leadership, Communication, Problem Solving, Teamwork, Agile, Scrum

**Why proper casing here (vs. lowercase in scorer.py)?** These skills are displayed to the user in the UI as tags. You want to show `"Python"` and `"TensorFlow"`, not `"python"` and `"tensorflow"`. The comparison is still done case-insensitively (`skill.lower() in text_lower`).

---

**Function 1: `extract_email(text)`**
```python
def extract_email(text: str) -> str:
    pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'
    match = re.search(pattern, text)
    return match.group(0) if match else ""
```
**Regex explained:** `[\w.+-]+@[\w-]+\.[\w.-]+`
- `[\w.+-]+` → One or more of: word chars (letters/digits/underscore), dots, plus signs, hyphens — the local part before @
- `@` → Literal @ sign
- `[\w-]+` → Domain name part (letters, digits, hyphens)
- `\.` → Literal dot (must escape with `\` — bare `.` in regex means "any character")
- `[\w.-]+` → Domain extension: `.com`, `.co.in`, `.org`, `.io`

**`re.search()`** — Scans through the text and returns the first match found (or `None` if not found).
**`match.group(0)`** — Returns the full matched text (group 0 = entire match).
**Returns:** `"john@gmail.com"` or `""` if no email found.

---

**Function 2: `extract_phone(text)`**
```python
def extract_phone(text: str) -> str:
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+?\d{2}[-.\s]?\d{5}[-.\s]?\d{5}',
        r'\+?\d{10,13}',
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return ""
```
**Why 4 patterns?** Phone number formats vary enormously globally. The 4 patterns cover:
1. `+1 (555) 123-4567` or `+91 98765 43210` — international with country code
2. `+91 98765 43210` — Indian format specifically (2-digit country code + 5+5)
3. `9876543210` or `+919876543210` — plain digits, 10-13 total
4. `(555) 123-4567` or `555-123-4567` — US format without country code

Tries patterns in order, returns the first match. `.strip()` removes leading/trailing spaces from the matched number.

---

**Function 3: `extract_name(text)` ← most sophisticated extractor**
```python
def extract_name(text: str) -> str:
    lines = text.strip().split('\n')
    for line in lines[:7]:
        line = line.strip()
        if not line or len(line) < 2:
            continue
        skip_patterns = [
            r'^(resume|curriculum|cv|vitae|profile|objective|summary)',
            r'@', r'\d{5,}', r'^(http|www)',
            r'^(address|phone|email|contact|linkedin)',
            r'^(page\s|copyright)',
        ]
        should_skip = False
        for pattern in skip_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                should_skip = True
                break
        if should_skip:
            continue
        clean = re.sub(r'[^\w\s]', '', line).strip()
        words = clean.split()
        if 1 <= len(words) <= 5 and all(w.isalpha() for w in words):
            return line.strip()
    return "Unknown"
```
**The heuristic:** Names are always near the top of a resume, are short (1-5 words), and contain only alphabetic characters.

**Step-by-step logic:**
1. `text.strip().split('\n')` — Split resume into individual lines
2. `lines[:7]` — Only check the first 7 lines (names appear at the very top)
3. Skip empty/very short lines
4. **Skip-pattern checks** — Skip any line that looks like:
   - Section headers: "Resume", "CV", "Profile", "Objective", "Summary"
   - Contains `@` → likely an email address
   - Contains 5+ consecutive digits → likely a phone number or zip code
   - Starts with `http` or `www` → a URL
   - Starts with contact field labels: "Address", "Phone", "Email", "LinkedIn"
   - Page number indicators: "Page 1", "Copyright"
5. `re.sub(r'[^\w\s]', '', line)` — Remove all punctuation from the candidate line
6. Check: 1–5 words AND all words are alphabetic (`w.isalpha()`)
7. If passes all checks → this is the name!
8. If nothing found in 7 lines → return `"Unknown"`

**Why heuristic-based and not AI?** This rule works on 95% of real resumes. The name is almost always the first meaningful, short, all-letters line. Using a Named Entity Recognition (NER) AI model would be dramatically more complex, slower, and still only marginally more accurate for this specific pattern.

---

**Function 4: `extract_skills(text)`**
```python
def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)
    return sorted(set(found))
```
- Converts full resume text to lowercase once
- For each skill in `KNOWN_SKILLS`, checks if `skill.lower()` appears anywhere in the text
- `set(found)` — Removes any duplicates (e.g., "Python" listed twice in a resume)
- `sorted(...)` — Alphabetically sorts the results for consistent display

**Returns:** `["AWS", "Docker", "Machine Learning", "Python", "TensorFlow"]` — proper casing, sorted.

---

**Function 5: `extract_education(text)`**
```python
def extract_education(text: str) -> list:
    degree_patterns = [
        r"(?:B\.?(?:Tech|E|Sc|A|Com|S)\.?|Bachelor(?:'s)?)\s*(?:of|in)?\s*[\w\s,]+",
        r"(?:M\.?(?:Tech|E|Sc|A|Com|S|BA)\.?|Master(?:'s)?)\s*(?:of|in)?\s*[\w\s,]+",
        r"(?:Ph\.?D\.?|Doctorate)\s*(?:in)?\s*[\w\s,]*",
        r"(?:Diploma|Certificate)\s*(?:in)?\s*[\w\s,]+",
    ]
    education = []
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        education.extend([m.strip()[:80] for m in matches])
    return education[:5]
```
Four patterns covering:
- **Bachelor's:** B.Tech, B.E., B.Sc, B.A., Bachelor of Science, Bachelor's in Computer Science
- **Master's:** M.Tech, M.Sc, M.A., Master of Engineering, Master's in Data Science
- **Doctorate:** Ph.D., PhD, Doctorate in Machine Learning
- **Diploma/Cert:** Diploma in Web Development, Certificate in Data Analytics

- `re.findall()` — Returns ALL non-overlapping matches (not just the first)
- `[:80]` — Truncates each match to 80 characters (prevents runaway regex matches)
- `[:5]` — Returns at most 5 education entries per resume

---

**Function 6: `extract_experience_years(text)`**
```python
def extract_experience_years(text: str) -> str:
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'(?:experience|exp)\s*(?:of)?\s*(\d+)\+?\s*(?:years?|yrs?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}+ years"
    return "Not specified"
```
Two patterns handle two common orderings:
1. `"5 years of experience"` / `"5+ yrs experience"` — number first
2. `"experience of 5 years"` / `"exp: 5 yrs"` — word first

- `(\d+)` — The parentheses in the regex create a **capture group** — the matched digits are saved separately
- `match.group(1)` — Retrieves the captured group (just the number, not the surrounding words)
- `f"{match.group(1)}+ years"` — Formats result as `"5+ years"`
- If no match: returns `"Not specified"`

---

**Function 7: `extract_all(text)` ← the master function called by the pipeline**
```python
def extract_all(text: str) -> dict:
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_years": extract_experience_years(text),
    }
```
**What it does:** Runs all 6 extractors on the same text and bundles everything into one dictionary.

**Why one `extract_all()` instead of calling each individually?** Clean API. `main.py` writes `info = extract_all(text)` — one line — instead of 6 separate calls. All extraction happens in one place, making the pipeline loop tidy.

**Who calls this:** `main.py`: `info = extract_all(text)` for each resume. The returned dict is spread into the candidate record:
```python
candidate = {
    "name": info["name"],
    "email": info["email"],
    "phone": info["phone"],
    "skills": info["skills"],
    "education": info["education"],
    "experience_years": info["experience_years"],
    ...
}
```

---

## 📂 MODULE 7 — `ranking/` — The Leaderboard

**Pipeline Role:** STEP 7 of 8. Sorts all candidates by their Final Score (highest first) and assigns rank numbers (#1, #2, #3...).

**Analogy:** After all athletes complete their race and receive scores, the Leaderboard module creates the official standings: gold, silver, bronze... in descending order of score.

**Why a dedicated module for simple sorting?** While the logic is simple, isolating it means: (1) `main.py` stays clean, (2) you can write tests purely for ranking logic, (3) you can swap in a more complex ranking formula (e.g., weighted by experience years) by editing only this one file.

---

### 📄 `ranking/__init__.py`
`# Ranking module - sort candidates by score` — marks the folder as a package.

---

### 📄 `ranking/ranker.py` — Full Breakdown

No external library imports — pure Python sorting logic only.

---

**Function 1: `rank_candidates(candidates)` ← the main pipeline function**
```python
def rank_candidates(candidates: list) -> list:
    sorted_candidates = sorted(
        candidates,
        key=lambda x: x.get("final_score", 0),
        reverse=True,
    )
    for i, candidate in enumerate(sorted_candidates, start=1):
        candidate["rank"] = i
    return sorted_candidates
```
**What it does:** Takes an unsorted list of candidate dictionaries, sorts by `final_score` descending, and adds a `"rank"` key to each.

**Breaking it down:**
- `sorted(candidates, key=..., reverse=True)` — Python's built-in stable sort.
  - `key=lambda x: x.get("final_score", 0)` — A "key function" that extracts the sort value from each candidate. `lambda x:` means "given a candidate dict `x`, return...". `.get("final_score", 0)` safely gets `final_score` or 0 if missing.
  - `reverse=True` — Sort highest score first (descending). Without this, Python sorts ascending (lowest first).
- `enumerate(sorted_candidates, start=1)` — Loops with a counter `i` starting at 1 (not 0). `enumerate` yields `(i, item)` pairs.
- `candidate["rank"] = i` — Adds the rank number directly into the candidate's dictionary. This mutates the dict in-place.

**Example:**
```python
# Input (any order):
[
  {"name": "Jane", "final_score": 72.4},
  {"name": "Bob",  "final_score": 91.2},
  {"name": "John", "final_score": 85.0},
]
# Output (sorted, ranked):
[
  {"name": "Bob",  "final_score": 91.2, "rank": 1},
  {"name": "John", "final_score": 85.0, "rank": 2},
  {"name": "Jane", "final_score": 72.4, "rank": 3},
]
```

**Who calls this:** `main.py`: `ranked = rank_candidates(candidates)` → result stored in `state.results` and saved to CSV.

---

**Function 2: `get_top_candidates(candidates, top_n=5)`**
```python
def get_top_candidates(candidates: list, top_n: int = 5) -> list:
    ranked = rank_candidates(candidates)
    return ranked[:top_n]
```
- Calls `rank_candidates()` to sort first, then takes only the first `top_n` items
- `ranked[:top_n]` — Python list slicing. `[:5]` returns elements at index 0, 1, 2, 3, 4.
- Default: top 5 candidates

**Current use:** Available as a utility function. Could be used to show "Top 5 only" in the UI or send only top candidates to an email report.

---

**Function 3: `get_shortlisted(candidates, threshold=60.0)`**
```python
def get_shortlisted(candidates: list, threshold: float = 60.0) -> list:
    ranked = rank_candidates(candidates)
    return [c for c in ranked if c.get("final_score", 0) >= threshold]
```
- Sorts candidates, then filters to keep only those at or above the threshold score
- `[c for c in ranked if ...]` — List comprehension: "give me every candidate `c` where their score meets the minimum"
- Default threshold: 60.0 (candidates below 60 are not shortlisted)

**Current use:** The threshold filtering in the UI is done visually in Streamlit (cards are faded, not removed). This function provides the same filtering at the data level — useful for programmatic shortlisting, exporting only qualified candidates, or sending emails only to shortlisted candidates.

---

## 📂 MODULE 8 — `ui/` — The Face (The Website)

**Pipeline Role:** Not a processing step. The user-facing interface. Orchestrates the full pipeline by calling FastAPI endpoints through browser interactions.

**Analogy:** The reception desk of a company. Visitors (users) interact only with the receptionist (Streamlit). Behind the scenes, the receptionist routes requests to the appropriate departments (FastAPI modules). Visitors never go directly to those back-office departments.

---

### 📄 `ui/__init__.py`
`# UI module - Streamlit dashboard` — marks the folder as a package.

---

### 📄 `ui/app.py` — Full Breakdown

This 504-line file creates the entire browser dashboard. Here is every section explained:

---

**Section 1 — Imports:**
```python
import streamlit as st
import requests
import pandas as pd
import time
API_BASE = "http://localhost:8000"
```
- `streamlit as st` — Every `st.xxx()` call creates a UI element (button, text box, table, etc.)
- `requests` — The HTTP library used to call FastAPI endpoints from within Streamlit
- `pandas as pd` — Used for the table view: converts candidate list → DataFrame → interactive table
- `API_BASE` — The FastAPI server's base URL. All API calls prefix with this. Changing one variable updates all calls.

---

**Section 2 — Page Configuration:**
```python
st.set_page_config(
    page_title="AI Resume Shortlister",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
```
- Sets browser tab title and emoji favicon
- `layout="wide"` — Uses full browser width (default is a narrow centered column)
- `initial_sidebar_state="expanded"` — Left sidebar is visible on load

---

**Section 3 — Custom CSS Dark Theme:**
A large `st.markdown("""<style>...</style>""")` block that injects custom CSS. Key styles:
- `.hero-banner` — The dark purple gradient header at the top of the page
- `.metric-card` — Floating stat boxes with gradient text values and hover lift effect
- `.candidate-card` — Dark card for each candidate with hover color border
- `.skill-tag` — Blue-tinted badge for each skill inside candidate cards
- `section[data-testid="stSidebar"]` — Dark background for the sidebar
- `.status-connected` / `.status-disconnected` — Green/red API status text

`unsafe_allow_html=True` is required here to let Streamlit render custom HTML/CSS (normally blocked for security).

---

**Section 4 — 5 Helper Functions:**

**`check_api()`**
```python
def check_api():
    try:
        r = requests.get(f"{API_BASE}/", timeout=3)
        return r.status_code == 200
    except Exception:
        return False
```
Pings FastAPI's health check endpoint (`GET /`). Returns `True` if server responds with status 200, `False` if connection fails or times out. Called once per page render. Used to show green/red dot and disable the Process button if offline.

**`upload_files(files)`**
```python
file_tuples = [("files", (f.name, f.getvalue(), "application/pdf")) for f in files]
r = requests.post(f"{API_BASE}/api/upload", files=file_tuples, timeout=30)
return r.json()
```
Takes Streamlit `UploadedFile` objects, formats them as multipart form data (the web standard for file uploads), sends them to FastAPI's `/api/upload` endpoint.

**`set_jd(text)`** — Posts job description text to `/api/job-description` as form data.

**`process()`** — Calls `POST /api/process` with a 300-second timeout (allows for slow first-run model loading).

**`get_results()`** — Calls `GET /api/results` and returns the candidate JSON.

**`cleanup()`** — Calls `DELETE /api/cleanup` to wipe temp files and reset state.

---

**Section 5 — Sidebar:**
```python
with st.sidebar:
```
Everything inside `with st.sidebar:` renders in the left panel:
- API status dot (green = connected, red = offline) using `check_api()`
- `st.slider("🎯 Shortlist Threshold", 0, 100, 60)` — A draggable slider (default 60). Candidates scoring below this value appear faded in results.
- "🗑️ Clear All Data" button — calls `cleanup()`, clears `st.session_state["results"]`
- Version info at the bottom

---

**Section 6 — Main Upload + JD Area:**
```python
col_upload, col_jd = st.columns(2, gap="large")
```
Creates two equal side-by-side columns. Left column has the file uploader. Right column has the JD text area.

- `st.file_uploader(type=["pdf"], accept_multiple_files=True)` — Only accepts `.pdf` files, allows multi-select. Returns a list of `UploadedFile` objects.
- `st.text_area(height=200)` — Multi-line text input. Returns the text as a string whenever the script re-runs.
- Live counts: shows file count and word count as you type/select.

---

**Section 7 — Process Button:**
```python
process_btn = st.button(
    "🚀 Process & Rank Candidates",
    disabled=not (uploaded_files and jd_text and api_ok),
)
```
**Auto-disabled** if any of: no files, no JD text, API offline. This prevents partial/invalid processing.

When clicked, a `with st.status(...)` spinner block shows live progress steps:
1. `upload_files()` → shows "✅ N resume(s) uploaded"
2. `set_jd()` → shows "✅ Job description saved"
3. `process()` → shows "🧠 Running AI pipeline..." (this takes the most time — model + FAISS)
4. Stores result in `st.session_state["results"]`

**`st.session_state`** — Streamlit re-runs the entire Python script every time you interact with ANY UI element. Without `session_state`, results would disappear on the next interaction. `session_state` persists values across re-runs for the duration of the browser session.

---

**Section 8 — Results Display:**
Shown when `st.session_state["results"]` exists and has data.

**Metric cards row (4 columns):**
- Total Candidates, Shortlisted (above threshold), Average Score, Top Score
- Rendered using custom HTML `.metric-card` divs for the gradient styling

**View toggle:**
```python
view_mode = st.radio("View Mode", ["📇 Cards", "📊 Table"], horizontal=True)
```

**Cards View:** For each candidate in ranked order:
- `opacity: 1` if score ≥ threshold (shortlisted), `opacity: 0.5` if below (visually faded)
- Score color: green `#4ade80` if shortlisted, red `#f87171` if not
- Rank badge, name, final score
- Email, phone, filename details
- Similarity %, ATS %, Final % scores
- First 10 skill tags as `span.skill-tag` elements
- `st.expander()` — Collapsible section showing matched/missing keywords, education, experience years

**Table View:**
```python
df = pd.DataFrame(candidates)
st.dataframe(df, column_config={"Final Score": st.column_config.ProgressColumn(...)})
```
Converts candidate list to Pandas DataFrame, displays as interactive sortable table. `ProgressColumn` shows each score as both a number and a progress bar visualization.

---

**Section 9 — Download Button:**
```python
r = requests.get(f"{API_BASE}/api/download-csv", timeout=10)
st.download_button("📥 Download Results as CSV", data=r.content, file_name="resume_shortlist_results.csv", mime="text/csv")
```
Fetches the CSV binary from FastAPI's `/api/download-csv` endpoint, creates a browser download button. Clicking it triggers a file download in the user's browser — no page reload needed.

---

## 📄 THE CENTRAL FILE — `main.py` — The Manager & Orchestrator

**What it is:** The single most important file in the project. It is both the FastAPI application AND the controller that calls every other module in the right sequence.

**Why it exists as a separate file (not inside a module folder):** `main.py` sits at the project root because it IS the application entry point. You run `uvicorn main:app` — Uvicorn opens `main.py` and starts everything from there.

---

**Imports — External Libraries:**
```python
import os, csv, io
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
```
- `os` — For `os.path.basename(path)` to extract just the filename from a full path
- `csv` — Python's built-in CSV writing module (used in `_save_results_csv()`)
- `io` — For `io.StringIO()` and `io.BytesIO()` — in-memory file-like objects (used for CSV download streaming)
- `pathlib.Path` — Consistent path handling
- `asynccontextmanager` — Decorator for creating async context managers (used for the lifespan startup/shutdown)
- FastAPI classes: `FastAPI` (the app), `UploadFile` (uploaded files), `File`/`Form` (request body types), `HTTPException` (error responses)
- `StreamingResponse` — Sends data as a stream (used for CSV download)
- `CORSMiddleware` — Allows cross-origin requests (lets Streamlit at port 8501 call FastAPI at port 8000)

**Imports — Project Modules:**
```python
from ingestion.upload import save_resume, get_all_resumes, cleanup_temp, ensure_directories, OUTPUT_DIR
from parsing.parser import extract_text_from_pdf
from embeddings.embedder import generate_embedding, generate_embeddings_batch
from matching.matcher import match_resumes_to_job
from scoring.scorer import calculate_ats_score, calculate_final_score
from extraction.extractor import extract_all
from ranking.ranker import rank_candidates
```
These 7 import lines connect all 7 processing modules. `main.py` is the only file that imports from all other modules — it is the coordinator that ties everything together.

---

**The `AppState` Class:**
```python
class AppState:
    def __init__(self):
        self.job_description: str = ""
        self.results: list = []
        self.is_processing: bool = False

state = AppState()
```
**Why this exists:** HTTP is stateless — each request is completely independent. But the pipeline needs to remember the JD (set in one request) when processing starts (a different request later). `AppState` is an in-memory store that persists for the lifetime of the server process.

- `job_description` — Holds the JD text between the `POST /api/job-description` call and the `POST /api/process` call
- `results` — Holds the ranked candidates between `POST /api/process` and `GET /api/results`
- `is_processing` — A concurrency lock: set to `True` during processing, prevents two simultaneous `/api/process` requests from running the pipeline twice at the same time

---

**The `lifespan` Function (Startup/Shutdown):**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_directories()
    print("[START] AI Resume Shortlister API is starting...")
    yield
    print("[STOP] Shutting down...")
```
- Everything **before** `yield` runs once when the server starts
- Everything **after** `yield` runs once when the server stops
- `ensure_directories()` on startup guarantees `temp_resumes/` and `outputs/` exist before any request arrives

---

**The 6 API Endpoints — Complete Breakdown:**

**`GET /`** — Health check. Returns `{"status": "running"}`. Streamlit's `check_api()` calls this to determine if the backend is online.

**`POST /api/upload`:**
```python
async def upload_resumes(files: list[UploadFile] = File(...)):
    for f in files:
        if not f.filename.lower().endswith(".pdf"):
            continue
        content = await f.read()
        path = save_resume(content, f.filename)
```
- `list[UploadFile]` — FastAPI receives multiple file uploads
- Only accepts `.pdf` extensions (silently skips non-PDF files)
- `await f.read()` — Async reads the file bytes from the HTTP request body
- `save_resume(content, f.filename)` — Passes bytes + name to the ingestion module

**`POST /api/job-description`:**
```python
async def set_job_description(jd_text: str = Form(...)):
    state.job_description = jd_text.strip()
```
- `Form(...)` — Tells FastAPI to read `jd_text` from form data (not JSON body)
- `.strip()` — Removes leading/trailing whitespace
- Stored in `state` for use during processing

**`POST /api/process`** — The pipeline orchestrator (the most important endpoint):
```python
state.is_processing = True
try:
    # Step 1: Parse
    resume_texts, valid_paths = [], []
    for path in resume_paths:
        text = extract_text_from_pdf(path)
        if text:
            resume_texts.append(text)
            valid_paths.append(path)

    # Step 2: Embed
    resume_embeddings = generate_embeddings_batch(resume_texts)
    jd_embedding = generate_embedding(state.job_description)

    # Step 3: Match
    similarity_scores = match_resumes_to_job(resume_embeddings, jd_embedding)

    # Step 4 & 5: Score + Extract + Build candidate records
    candidates = []
    for i, (text, path) in enumerate(zip(resume_texts, valid_paths)):
        ats_result = calculate_ats_score(text, state.job_description)
        final_score = calculate_final_score(similarity_scores[i], ats_result["ats_score"])
        info = extract_all(text)
        candidate = {"filename": os.path.basename(path), **info,
                     "similarity_score": round(similarity_scores[i] * 100, 1),
                     "ats_score": ats_result["ats_score"],
                     "final_score": final_score,
                     "matched_keywords": ats_result["matched_keywords"],
                     "missing_keywords": ats_result["missing_keywords"]}
        candidates.append(candidate)

    # Step 6: Rank
    ranked = rank_candidates(candidates)
    state.results = ranked

    # Step 7: Save CSV
    _save_results_csv(ranked)
    return {"message": f"...", "candidates": ranked}
finally:
    state.is_processing = False
```
The `finally` block guarantees `is_processing` is reset to `False` even if an exception occurs — otherwise the lock would never release and future requests would always fail with "processing already in progress."

**`GET /api/results`** — Returns `state.results` as JSON. If no results yet, returns a helpful message.

**`GET /api/download-csv`** — Reads `state.results`, writes them to an in-memory `io.StringIO` buffer as CSV, converts to bytes, and streams back with `Content-Disposition: attachment` header (tells browser to download, not display).

**`DELETE /api/cleanup`** — Calls `cleanup_temp()`, resets `state.results = []` and `state.job_description = ""`. A fresh start.

---

**The `_save_results_csv()` Helper:**
```python
def _save_results_csv(candidates: list):
    csv_path = OUTPUT_DIR / "results.csv"
    fieldnames = ["rank", "name", "email", "phone", "skills",
                  "final_score", "similarity_score", "ats_score", "filename"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in candidates:
            row = {k: v for k, v in c.items() if k in fieldnames}
            row["skills"] = ", ".join(c.get("skills", []))
            writer.writerow(row)
```
- Prefixed with `_` (underscore) = private helper function, not an API endpoint
- Saves ranked results to `outputs/results.csv` as a persistent backup
- `csv.DictWriter` — Writes dictionaries as CSV rows, matching dict keys to column headers
- `row["skills"] = ", ".join(...)` — Converts the skills list `["Python", "AWS"]` to a string `"Python, AWS"` (CSV cells can't contain lists)
- `newline=""` — Required for `csv` module on Windows to prevent double-newlines
- `encoding="utf-8"` — Ensures special characters are handled correctly

---

## 📄 `requirements.txt` — The Shopping List

This file tells `pip install -r requirements.txt` exactly which libraries to install and what minimum versions to use.

```
PyMuPDF>=1.24.0          # PDF reading (parser.py)
sentence-transformers>=3.0.0  # AI embeddings (embedder.py)
torch>=2.0.0             # Neural network engine (used by sentence-transformers)
faiss-cpu>=1.8.0         # Vector similarity search (matcher.py)
numpy>=1.26.0            # Numerical arrays (everywhere)
fastapi>=0.115.0         # Backend API framework (main.py)
uvicorn[standard]>=0.30.0  # ASGI server to run FastAPI
python-multipart>=0.0.9  # File upload parsing for FastAPI
streamlit>=1.38.0        # UI dashboard (ui/app.py)
requests>=2.32.0         # HTTP client (ui/app.py → FastAPI calls)
pandas>=2.2.0            # Data tables and CSV in UI
```

**`>=` means:** "install this version OR any newer version that is backward-compatible." This prevents the project from breaking when library authors release updates, while allowing security patches and improvements.

**`[standard]` in `uvicorn[standard]`:** Installs Uvicorn with optional extras — specifically `websockets` and `httptools` which make it significantly faster. Just `uvicorn` would work but be slower.

---

## 🗺️ PART 14 — THE COMPLETE CALL CHAIN (How Every File Connects)

When you click "🚀 Process & Rank Candidates", here is the **exact sequence of function calls** across all files:

```
Browser click
  └─ Streamlit (ui/app.py)
       ├─ upload_files()      → POST /api/upload
       │    └─ main.py: upload_resumes()
       │         └─ ingestion/upload.py: save_resume()
       │
       ├─ set_jd()            → POST /api/job-description
       │    └─ main.py: set_job_description()  [stores in state]
       │
       └─ process()           → POST /api/process
            └─ main.py: process_resumes()
                 ├─ ingestion/upload.py: get_all_resumes()
                 │
                 ├─ [LOOP per PDF]
                 │   └─ parsing/parser.py: extract_text_from_pdf()
                 │        └─ fitz.open() → page.get_text()  [PyMuPDF]
                 │
                 ├─ embeddings/embedder.py: generate_embeddings_batch()
                 │   └─ get_model() → SentenceTransformer("all-MiniLM-L6-v2")
                 │        └─ model.encode(texts)  [PyTorch runs neural network]
                 │
                 ├─ embeddings/embedder.py: generate_embedding()  [for JD]
                 │
                 ├─ matching/matcher.py: match_resumes_to_job()
                 │   ├─ build_faiss_index()
                 │   │   └─ faiss.IndexFlatIP().add(embeddings)
                 │   └─ search_similar()
                 │       └─ index.search(jd_vector, k)
                 │
                 ├─ [LOOP per resume]
                 │   ├─ scoring/scorer.py: calculate_ats_score()
                 │   │   └─ extract_keywords() × 2 + regex checks
                 │   ├─ scoring/scorer.py: calculate_final_score()
                 │   └─ extraction/extractor.py: extract_all()
                 │       ├─ extract_name()    [regex heuristic]
                 │       ├─ extract_email()   [regex]
                 │       ├─ extract_phone()   [regex, 4 patterns]
                 │       ├─ extract_skills()  [KNOWN_SKILLS matching]
                 │       ├─ extract_education() [regex, 4 degree patterns]
                 │       └─ extract_experience_years() [regex, 2 patterns]
                 │
                 ├─ ranking/ranker.py: rank_candidates()
                 │   └─ sorted() + enumerate() [pure Python]
                 │
                 └─ _save_results_csv()  [outputs/results.csv]

  └─ Streamlit receives ranked JSON
       └─ Displays candidate cards / table
            └─ st.download_button → GET /api/download-csv
```

---

## ✅ PART 15 — QUICK REFERENCE: WHAT BREAKS IF EACH FILE IS DELETED

| File Deleted | What Breaks |
|---|---|
| Any `__init__.py` | `main.py` imports crash with `ModuleNotFoundError` on startup |
| `ingestion/upload.py` | Cannot save, retrieve, or clean up PDF files. All 6 API endpoints that handle files break. |
| `parsing/parser.py` | Cannot convert PDFs to text. Pipeline crashes at Step 1 with `NameError`. |
| `embeddings/embedder.py` | No embeddings generated. Pipeline crashes at Step 2. No AI matching possible. |
| `matching/matcher.py` | No similarity scores. Pipeline crashes at Step 3. |
| `scoring/scorer.py` | No ATS scores, no final scores. Pipeline crashes at Step 4. |
| `extraction/extractor.py` | No name/email/phone/skills extracted. Candidate cards show empty fields. |
| `ranking/ranker.py` | Candidates not sorted or ranked. Results appear in random upload order. |
| `main.py` | The entire backend ceases to exist. Nothing works. |
| `ui/app.py` | No browser interface. Can only interact via raw HTTP (command-line tools). |
| `requirements.txt` | Fresh install impossible. Developers cannot set up the project. |

---

*End of Part 13–15. Every file in the AI Resume Shortlister has now been explained in full detail — what it is, why it exists, what every function does, and how it connects to the rest of the project.*
