import axios from "axios";
 
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",  // uses relative URL in production
});
 
// 📄 Resume Upload → returns { skills: [...] }
export const uploadResume = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post("/resume/parse", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};
 
// 📋 Extract skills from JD text → returns { skills: [...] }
export const extractJDSkills = (jdText) =>
  API.post("/skills/extract", { text: jdText });
 
// 🔍 Compare JD skills vs Resume skills → returns gap analysis
export const compareSkills = (jdSkills, resumeSkills) =>
  API.post("/skill-gap/compare", {
    jd_skills:     jdSkills,
    resume_skills: resumeSkills,
  });
 
// 🚀 Start Session with prioritized skills list
export const startSession = (skills) =>
  API.post("/session/start", { skills });
 
// 🤖 Run Agent loop
// ✅ FIX: send null (not "") for first call so backend correctly generates question
export const runSession = (session_id, answer = null) =>
  API.post("/session/run", {
    session_id,
    answer: answer || null,   // "" becomes null — prevents empty-answer evaluation
  });
 