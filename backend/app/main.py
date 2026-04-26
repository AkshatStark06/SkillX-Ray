from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
 
app = FastAPI(title="AI Skill Assessment Agent")
 
# ✅ CORS must be registered BEFORE routers — not after
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# ✅ All routes that exist in app/routes/
from app.routes import agent, session, resume, skills
from app.routes import assessment, results, parse
from app.routes import question, evaluation, skill_gap
 
# ✅ Single consistent /api prefix for everything
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
 
 
@app.get("/")
def root():
    return {"status": "ok", "message": "AI Skill Assessment API is running"}
 
 
@app.get("/health")
def health():
    return {"status": "healthy"}

static_path = os.path.join(os.path.dirname(__file__), "../../static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

@app.get("/{full_path:path}")
def serve_react(full_path: str):
    index = os.path.join(static_path, "index.html")
    return FileResponse(index)