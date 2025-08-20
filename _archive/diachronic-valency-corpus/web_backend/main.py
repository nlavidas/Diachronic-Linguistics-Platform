
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import asyncpg
import os
import secrets

app = FastAPI(title="Diachronic Valency Corpus API")
security = HTTPBasic()

BASIC_AUTH_USER = os.getenv("BASIC_AUTH_USER", "admin")
BASIC_AUTH_PASS = os.getenv("BASIC_AUTH_PASS", "changeme")

def check_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, BASIC_AUTH_USER)
    correct_password = secrets.compare_digest(credentials.password, BASIC_AUTH_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/corpus")

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# Contrastive analysis endpoint: compare valency patterns across languages/periods
@app.get("/api/contrastive")
async def contrastive_analysis(lang1: str, lang2: str, pattern: str = None, user: str = Depends(check_basic_auth)):
    base_query = "SELECT language, year, verb, pattern, arguments FROM valency_patterns JOIN texts ON valency_patterns.text_id = texts.id WHERE language = $1"
    if pattern:
        base_query += " AND pattern = $2"
    async with app.state.db.acquire() as conn:
        if pattern:
            res1 = await conn.fetch(base_query, lang1, pattern)
            res2 = await conn.fetch(base_query, lang2, pattern)
        else:
            res1 = await conn.fetch(base_query, lang1)
            res2 = await conn.fetch(base_query, lang2)
    return {"lang1": [dict(r) for r in res1], "lang2": [dict(r) for r in res2]}



# List all validated, non-quarantined texts and their metadata by default
@app.get("/api/texts")
async def list_texts(validated_only: bool = True, user: str = Depends(check_basic_auth)):
    # By default, only show validated and not quarantined texts
    if validated_only:
        query = "SELECT id, filename, language, year, validated, quarantined FROM texts WHERE validated = TRUE AND quarantined = FALSE"
    else:
        query = "SELECT id, filename, language, year, validated, quarantined FROM texts"
    async with app.state.db.acquire() as conn:
        results = await conn.fetch(query)
    return [dict(r) for r in results]

# Update validation/quarantine status for a text
@app.post("/api/texts/{text_id}/status")
async def update_text_status(text_id: int, validated: bool = None, quarantined: bool = None, user: str = Depends(check_basic_auth)):
    if validated is None and quarantined is None:
        raise HTTPException(status_code=400, detail="No status provided")
    updates = []
    values = []
    if validated is not None:
        updates.append("validated = $1")
        values.append(validated)
    if quarantined is not None:
        updates.append("quarantined = $2" if validated is not None else "quarantined = $1")
        values.append(quarantined)
    set_clause = ", ".join(updates)
    query = f"UPDATE texts SET {set_clause} WHERE id = $${len(values)+1} RETURNING id, validated, quarantined"
    values.append(text_id)
    async with app.state.db.acquire() as conn:
        row = await conn.fetchrow(query, *values)
    if not row:
        raise HTTPException(status_code=404, detail="Text not found")
    return dict(row)

# Get valency patterns/annotations for a given text, only if validated and not quarantined
@app.get("/api/annotations/{text_id}")
async def get_annotations(text_id: int, user: str = Depends(check_basic_auth)):
    # Check validation/quarantine status first
    meta_query = "SELECT validated, quarantined FROM texts WHERE id = $1"
    async with app.state.db.acquire() as conn:
        meta = await conn.fetchrow(meta_query, text_id)
        if not meta or not meta['validated'] or meta['quarantined']:
            return {"error": "Text is not validated or is quarantined."}
        query = "SELECT verb, pattern, arguments FROM valency_patterns WHERE text_id = $1"
        results = await conn.fetch(query, text_id)
    if not results:
        return {"error": "No annotations found for this text."}
    return [
        {"verb": r["verb"], "pattern": r["pattern"], "arguments": r["arguments"].split(",")}
        for r in results
    ]

# Publish/register a new text (metadata only, for demo)
# By default, new texts are not validated and not quarantined
@app.post("/api/publish")
async def publish_data(filename: str, language: str, year: int, user: str = Depends(check_basic_auth)):
    query = "INSERT INTO texts (filename, language, year, validated, quarantined) VALUES ($1, $2, $3, FALSE, FALSE) RETURNING id"
    async with app.state.db.acquire() as conn:
        row = await conn.fetchrow(query, filename, language, year)
    return {"status": "ok", "id": row["id"]}
# ---
# BEGINNER INSTRUCTIONS (for overnight automation):
# 1. Make sure your database has 'validated' and 'quarantined' columns in the 'texts' table.
# 2. Start the platform with: docker-compose up --build
# 3. Upload texts via the web interface or API. Only validated, non-quarantined texts will be processed and shown.
# 4. Use the /api/texts/{text_id}/status endpoint to validate or quarantine texts as needed.
# 5. The orchestrator and agents will run 24/7, processing only real, validated data.
# 6. Review logs and flagged data in the morning for quality control.

@app.get("/api/valency/changes")
async def diachronic_changes(lang: str = None, user: str = Depends(check_basic_auth)):
    query = "SELECT year, COUNT(*) as count FROM valency_patterns GROUP BY year ORDER BY year"
    async with app.state.db.acquire() as conn:
        results = await conn.fetch(query)
    return [dict(r) for r in results]

@app.get("/api/parallel")
async def parallel_translations(work: str, user: str = Depends(check_basic_auth)):
    # Example endpoint for parallel translations
    query = "SELECT * FROM translations WHERE work = $1"
    async with app.state.db.acquire() as conn:
        results = await conn.fetch(query, work)
    return [dict(r) for r in results]

# Healthcheck endpoint for Docker
@app.get("/health")
async def health():
    try:
        async with app.state.db.acquire() as conn:
            await conn.execute("SELECT 1")
        return {"status": "ok"}
    except Exception:
        return {"status": "error"}
