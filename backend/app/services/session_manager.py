"""
session_manager.py
In-memory session storage for assessment state.
One session = one candidate's full assessment run.
"""
 
import uuid
 
 
# In-memory store — resets on server restart (fine for hackathon/demo)
_sessions: dict = {}
 
 
def create_session(skills: list) -> str:
    """
    Create a new assessment session for a list of skills.
    Returns the session_id.
    """
    if not skills:
        raise ValueError("Cannot create session with empty skills list.")
 
    session_id = str(uuid.uuid4())
 
    _sessions[session_id] = {
        "skills":         skills,
        "current_index":  0,
        "results":        [],
        "followup_count": 0
    }
 
    print(f"Session created: {session_id} | Skills: {skills}")
    return session_id
 
 
def get_session(session_id: str) -> dict | None:
    """
    Retrieve session by ID. Returns None if not found.
    """
    return _sessions.get(session_id)
 
 
def update_session(session_id: str, data: dict) -> None:
    """
    Overwrite session data for a given session_id.
    """
    if session_id not in _sessions:
        raise KeyError(f"Session {session_id} does not exist.")
    _sessions[session_id] = data
 
 
def delete_session(session_id: str) -> None:
    """
    Remove a session after assessment is complete (optional cleanup).
    """
    _sessions.pop(session_id, None)
 