import { useState } from "react"
import {
  uploadResume,
  extractJDSkills,
  compareSkills,
  startSession,
  runSession,
} from "../services/api"

export default function Dashboard() {
  const [stage,        setStage]        = useState("input")
  const [loading,      setLoading]      = useState(false)
  const [error,        setError]        = useState("")
  const [jdText,       setJdText]       = useState("")
  const [jdSkills,     setJdSkills]     = useState([])
  const [resumeSkills, setResumeSkills] = useState([])
  const [resumeReady,  setResumeReady]  = useState(false)
  const [gapData,      setGapData]      = useState(null)
  const [assessSkills, setAssessSkills] = useState([])
  const [sessionId,    setSessionId]    = useState(null)
  const [question,     setQuestion]     = useState("")
  const [currentSkill, setCurrentSkill] = useState("")
  const [skillIndex,   setSkillIndex]   = useState(0)
  const [answer,       setAnswer]       = useState("")
  const [lastFeedback, setLastFeedback] = useState("")
  const [finalResult,  setFinalResult]  = useState(null)

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setError("")
    setLoading(true)
    try {
      const res = await uploadResume(file)
      setResumeSkills(res.data.skills || [])
      setResumeReady(true)
    } catch {
      setError("Failed to parse resume. Please try again.")
    }
    setLoading(false)
  }

  const handleAnalyse = async () => {
    if (!jdText.trim())  { setError("Please paste a Job Description."); return }
    if (!resumeReady)    { setError("Please upload your resume first."); return }
    setError("")
    setLoading(true)
    try {
      const jdRes  = await extractJDSkills(jdText)
      const jd     = jdRes.data.skills || []
      setJdSkills(jd)
      const gapRes = await compareSkills(jd, resumeSkills)
      const gap    = gapRes.data
      setGapData(gap)
      const toAssess = [
        ...(gap.core_skills    || gap.matched_skills || []),
        ...(gap.jd_only_skills || gap.missing_skills || []),
      ].slice(0, 8)
      setAssessSkills(toAssess)
      setStage("gap")
    } catch {
      setError("Analysis failed. Check if backend is running.")
    }
    setLoading(false)
  }

  const handleStartAssessment = async () => {
    setLoading(true)
    try {
      const sessionRes = await startSession(assessSkills)
      const id         = sessionRes.data.session_id
      setSessionId(id)
      const firstRes   = await runSession(id, null)
      const data       = firstRes.data
      setQuestion(data.question || data.next_question || "")
      setCurrentSkill(data.skill || assessSkills[0] || "")
      setSkillIndex(0)
      setStage("assessment")
    } catch {
      setError("Failed to start assessment. Please try again.")
    }
    setLoading(false)
  }

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) return
    setLoading(true)
    setLastFeedback("")
    try {
      const res  = await runSession(sessionId, answer)
      const data = res.data

      if (data.action === "complete") {
        setFinalResult(data)
        setStage("results")
        setLoading(false)
        return
      }

      if (data.evaluation?.feedback) setLastFeedback(data.evaluation.feedback)

      const nextQuestion = data.question || data.next_question || ""
      const nextSkill    = data.skill || currentSkill

      
      if (nextSkill !== currentSkill) {
        setSkillIndex(prev => Math.min(prev + 1, assessSkills.length - 1))
        setLastFeedback("") // clear feedback when moving to new skill
      }

      setCurrentSkill(nextSkill)
      setQuestion(nextQuestion)
      setAnswer("")

    } catch {
      setError("Something went wrong submitting your answer.")
    }
    setLoading(false)
  }

  const handleRestart = () => {
    setStage("input"); setJdText(""); setResumeReady(false)
    setResumeSkills([]); setJdSkills([]); setGapData(null)
    setSessionId(null); setQuestion(""); setAnswer("")
    setFinalResult(null); setError(""); setSkillIndex(0)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#020617] via-[#020617] to-[#0f172a] text-white flex items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-[#0f172a] p-8 rounded-2xl shadow-2xl border border-white/10">

        <h1 className="text-3xl font-bold text-center mb-2">AI Skill Assessment </h1>
        <p className="text-center text-gray-400 text-sm mb-8">Paste a Job Description + upload your resume to begin</p>

        {error && (
          <div className="mb-4 px-4 py-3 bg-red-900/50 border border-red-500 rounded-lg text-red-300 text-sm">{error}</div>
        )}

        {/* ── STAGE 1: INPUT ── */}
        {stage === "input" && (
          <div className="space-y-5">
            <div>
              <label className="block text-sm text-gray-400 mb-1">📋 Paste Job Description</label>
              <textarea
                rows={6}
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                placeholder="Paste the full job description here..."
                className="w-full p-3 bg-white/5 border border-white/10 rounded-lg text-sm resize-none focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">📄 Upload Resume (PDF)</label>
              <input
                type="file"
                accept=".pdf"
                onChange={handleResumeUpload}
                className="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer"
              />
              {resumeReady && (
                <p className="mt-2 text-green-400 text-xs">✅ Resume parsed — {resumeSkills.length} skills found</p>
              )}
            </div>
            <button
              onClick={handleAnalyse}
              disabled={loading}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg font-semibold transition"
            >
              {loading ? "Analysing..." : "Analyse & Show Skill Gap →"}
            </button>
          </div>
        )}

        {/* ── STAGE 2: GAP PREVIEW ── */}
        {stage === "gap" && gapData && (
          <div className="space-y-5">
            <h2 className="text-xl font-semibold">Skill Gap Analysis</h2>

            {(gapData.core_skills || gapData.matched_skills || []).length > 0 && (
              <div>
                <p className="text-sm text-gray-400 mb-2">✅ Skills you have (will be depth-assessed)</p>
                <div className="flex flex-wrap gap-2">
                  {(gapData.core_skills || gapData.matched_skills).map((s, i) => (
                    <span key={i} className="px-3 py-1 bg-green-700/50 border border-green-500 rounded-full text-sm">{s}</span>
                  ))}
                </div>
              </div>
            )}

            {(gapData.jd_only_skills || gapData.missing_skills || []).length > 0 && (
              <div>
                <p className="text-sm text-gray-400 mb-2">❌ Required but missing from resume</p>
                <div className="flex flex-wrap gap-2">
                  {(gapData.jd_only_skills || gapData.missing_skills).map((s, i) => (
                    <span key={i} className="px-3 py-1 bg-red-700/50 border border-red-500 rounded-full text-sm">{s}</span>
                  ))}
                </div>
              </div>
            )}

            <div className="p-4 bg-white/5 border border-white/10 rounded-lg">
              <p className="text-sm text-gray-300">
                📊 Assessment will cover <span className="text-white font-semibold">{assessSkills.length} skills</span>
              </p>
              <p className="text-xs text-gray-400 mt-1">{assessSkills.join(", ")}</p>
            </div>

            <div className="flex gap-3">
              <button onClick={() => setStage("input")} className="flex-1 py-2 border border-white/20 rounded-lg text-sm hover:bg-white/5 transition">← Go Back</button>
              <button onClick={handleStartAssessment} disabled={loading} className="flex-1 py-3 bg-green-600 hover:bg-green-700 disabled:opacity-50 rounded-lg font-semibold transition">
                {loading ? "Starting..." : "Start Assessment →"}
              </button>
            </div>
          </div>
        )}

        {/* ── STAGE 3: ASSESSMENT ── */}
        {stage === "assessment" && (
          <div className="space-y-5">
            <div>
              <div className="flex justify-between text-xs text-gray-400 mb-1">
                <span>Skill {skillIndex + 1} of {assessSkills.length}</span>
                <span className="capitalize font-medium text-blue-400">{currentSkill}</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full transition-all" style={{ width: `${((skillIndex + 1) / assessSkills.length) * 100}%` }} />
              </div>
            </div>

            {lastFeedback && (
              <div className="px-4 py-3 bg-yellow-900/30 border border-yellow-600/40 rounded-lg text-yellow-300 text-sm">
                💬 {lastFeedback}
              </div>
            )}

            <div className="p-5 bg-white/5 border border-white/10 rounded-xl text-base leading-relaxed">
              {question || "Loading question..."}
            </div>

            <textarea
              rows={4}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer here... (Ctrl+Enter to submit)"
              className="w-full p-3 bg-white/5 border border-white/10 rounded-lg text-sm resize-none focus:outline-none focus:border-purple-500"
              onKeyDown={(e) => { if (e.key === "Enter" && e.ctrlKey) handleSubmitAnswer() }}
            />

            <button
              onClick={handleSubmitAnswer}
              disabled={loading || !answer.trim()}
              className="w-full py-3 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg font-semibold transition"
            >
              {loading ? "Evaluating..." : "Submit Answer →"}
            </button>
          </div>
        )}

        {/* ── STAGE 4: RESULTS ── */}
        {stage === "results" && finalResult && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-center">✅ Assessment Complete</h2>

            <div>
              <h3 className="text-lg font-semibold mb-3">Skill Scores</h3>
              <div className="space-y-2">
                {(finalResult.results || []).map((r, i) => {
                  const score = r.evaluation?.score || 0
                  const level = r.evaluation?.level || "—"
                  const color = score >= 4 ? "green" : score === 3 ? "yellow" : "red"
                  const bgMap = { green: "bg-green-500", yellow: "bg-yellow-500", red: "bg-red-500" }
                  return (
                    <div key={i} className="p-4 bg-white/5 border border-white/10 rounded-lg">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-semibold capitalize">{r.skill}</span>
                        <span className="text-xs px-2 py-1 rounded-full bg-white/10">{level} — {score}/5</span>
                      </div>
                      <div className="w-full bg-white/10 rounded-full h-1.5 mt-2">
                        <div className={`${bgMap[color]} h-1.5 rounded-full`} style={{ width: `${(score / 5) * 100}%` }} />
                      </div>
                      {r.evaluation?.feedback && <p className="text-xs text-gray-400 mt-2">{r.evaluation.feedback}</p>}
                    </div>
                  )
                })}
              </div>
            </div>

            {finalResult.analysis && (
              <div className="grid grid-cols-2 gap-3">
                {finalResult.analysis.strong_skills?.length > 0 && (
                  <div className="p-3 bg-green-900/20 border border-green-700/40 rounded-lg">
                    <p className="text-xs text-green-400 mb-1 font-semibold">STRONG</p>
                    {finalResult.analysis.strong_skills.map((s, i) => <p key={i} className="text-sm capitalize">{s}</p>)}
                  </div>
                )}
                {finalResult.analysis.weak_skills?.length > 0 && (
                  <div className="p-3 bg-red-900/20 border border-red-700/40 rounded-lg">
                    <p className="text-xs text-red-400 mb-1 font-semibold">NEEDS WORK</p>
                    {finalResult.analysis.weak_skills.map((s, i) => <p key={i} className="text-sm capitalize">{s}</p>)}
                  </div>
                )}
              </div>
            )}

            {finalResult.analysis?.plan?.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3">📚 Personalised Learning Plan</h3>
                <div className="space-y-3">
                  {finalResult.analysis.plan.map((p, i) => (
                    <div key={i} className="p-4 bg-white/5 border border-white/10 rounded-xl">
                      <div className="flex justify-between items-start mb-2">
                        <p className="font-semibold capitalize">{p.skill}</p>
                        {p.time_estimate && (
                          <span className="text-xs text-blue-400 bg-blue-900/30 px-2 py-1 rounded-full">⏱ {p.time_estimate}</span>
                        )}
                      </div>
                      <p className="text-sm text-gray-300 mb-3">{p.topics}</p>
                      {p.resources?.length > 0 && (
                        <div>
                          <p className="text-xs text-gray-500 mb-1">Resources:</p>
                          {p.resources.map((r, j) => (
                            <a key={j}
                              href={
                                r.startsWith("http")
                                  ? r
                                  : r.startsWith("www.")
                                  ? `https://${r}`
                                  : `https://www.google.com/search?q=${encodeURIComponent(r)}`
                              }
                              target="_blank" rel="noreferrer"
                              className="block text-xs text-blue-400 hover:underline truncate">🔗 {r}</a>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button onClick={handleRestart} className="w-full py-2 border border-white/20 rounded-lg text-sm hover:bg-white/5 transition">
              ↩ Start New Assessment
            </button>
          </div>
        )}

      </div>
    </div>
  )
}