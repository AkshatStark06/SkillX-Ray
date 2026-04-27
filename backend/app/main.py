from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="AI Skill Assessment Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── All API routes ──
from app.routes import agent, session, resume, skills
from app.routes import assessment, results, parse
from app.routes import question, evaluation, skill_gap

app.include_router(agent.router,      prefix="/api", tags=["Agent"])
app.include_router(session.router,    prefix="/api", tags=["Session"])
app.include_router(resume.router,     prefix="/api", tags=["Resume"])
app.include_router(skills.router,     prefix="/api", tags=["Skills"])
app.include_router(assessment.router, prefix="/api", tags=["Assessment"])
app.include_router(results.router,    prefix="/api", tags=["Results"])
app.include_router(parse.router,      prefix="/api", tags=["Parse"])
app.include_router(question.router,   prefix="/api", tags=["Question"])
app.include_router(evaluation.router, prefix="/api", tags=["Evaluation"])
app.include_router(skill_gap.router,  prefix="/api", tags=["SkillGap"])

# ── Serve React frontend ──
# Must come AFTER all API routes
static_path = os.path.join(os.path.dirname(__file__), "../static")

if os.path.exists(static_path):
    # Serve static assets (JS, CSS, images)
    app.mount("/assets", StaticFiles(
        directory=os.path.join(static_path, "assets")
    ), name="assets")

    # ✅ Serve index.html for ALL non-API routes
    # This REPLACES the old @app.get("/") JSON route
    @app.get("/")
    def root():
        return FileResponse(os.path.join(static_path, "index.html"))

    @app.get("/{full_path:path}")
    def serve_react(full_path: str):
        # Don't intercept API calls
        if full_path.startswith("api/"):
            return {"error": "not found"}
        return FileResponse(os.path.join(static_path, "index.html"))
else:
    # Fallback if static folder missing (local dev)
    @app.get("/")
    def root():
        return {"status": "ok", "message": "AI Skill Assessment API is running"}