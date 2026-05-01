import { ArrowRight, BrainCircuit, CheckCircle2, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { LoadingState } from "../components/LoadingState";
import { SectionCard } from "../components/SectionCard";
import { SkillPill } from "../components/SkillPill";
import { api } from "../lib/api";
import { useSessionStore } from "../lib/session-store";
import type { Question, SessionDetail } from "../types/api";

export function AssessmentPage() {
  const { activeSessionId } = useSessionStore();
  const [session, setSession] = useState<SessionDetail | null>(null);
  const [nextQuestion, setNextQuestion] = useState<Question | null>(null);
  const [answerText, setAnswerText] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function load() {
      if (!activeSessionId) {
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        setError("");
        const detail = await api.getSession(activeSessionId);
        setSession(detail);
        if (!detail.questions.length) {
          const generated = await api.generateQuestions(activeSessionId);
          setSession(generated.session);
          setNextQuestion(generated.next_question);
          return;
        }
        const response = await api.getQuestions(activeSessionId);
        setNextQuestion(response.next_question);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not load the assessment.");
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, [activeSessionId]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!activeSessionId || !nextQuestion) {
      return;
    }
    try {
      setSubmitting(true);
      setError("");
      const response = await api.submitAnswer(activeSessionId, nextQuestion.id, answerText);
      setSession(response.session);
      setNextQuestion(response.next_question);
      setAnswerText("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not submit the answer.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <LoadingState label="Preparing assessment flow..." />;
  }

  if (!session) {
    return (
      <SectionCard title="No Active Assessment" eyebrow="Start analysis first">
        <p className="text-mist/75">Create or open an assessment session before answering questions.</p>
        <Link
          to="/analysis"
          className="mt-5 inline-flex items-center gap-2 rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90"
        >
          Go To Analysis
          <ArrowRight className="h-4 w-4" />
        </Link>
      </SectionCard>
    );
  }

  const completed = !nextQuestion && session.questions.length > 0;
  const answeredQuestions = session.questions.filter((question) => question.answer);

  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
      <div className="space-y-6">
        <SectionCard title="Conversational Skill Assessment" eyebrow="Step 4">
          <div className="flex flex-wrap gap-3">
            <SkillPill label={`Progress: ${session.progress.answered_questions}/${session.progress.total_questions}`} tone="good" />
            <SkillPill label={`Readiness: ${session.overall_readiness_score}%`} tone="warn" />
            <SkillPill label={`Candidate: ${session.resume.candidate_name}`} tone="neutral" />
          </div>

          {error ? <p className="mt-4 rounded-2xl border border-coral/30 bg-coral/10 px-4 py-3 text-sm text-coral">{error}</p> : null}

          {completed ? (
            <div className="mt-6 rounded-[2rem] border border-teal/20 bg-teal/10 p-6">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="h-6 w-6 text-teal" />
                <div>
                  <p className="font-display text-2xl text-white">Assessment complete</p>
                  <p className="text-sm text-mist/75">All assessment questions have been answered and scored.</p>
                </div>
              </div>
              <Link
                to="/report"
                className="mt-5 inline-flex items-center gap-2 rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90"
              >
                Open Final Report
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          ) : nextQuestion ? (
            <div className="mt-6 space-y-5">
              <div className="rounded-[2rem] border border-white/10 bg-white/5 p-6">
                <div className="flex items-center gap-3">
                  <div className="rounded-2xl bg-teal/15 p-3 text-teal">
                    <BrainCircuit className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-display text-xl text-white">{nextQuestion.skill_name}</p>
                    <p className="text-sm text-mist/70">{nextQuestion.difficulty} question</p>
                  </div>
                </div>
                <p className="mt-5 text-lg leading-8 text-white">{nextQuestion.prompt}</p>
                <p className="mt-3 text-sm leading-6 text-mist/70">{nextQuestion.guidance}</p>
              </div>

              <form className="space-y-4" onSubmit={handleSubmit}>
                <textarea
                  value={answerText}
                  onChange={(event) => setAnswerText(event.target.value)}
                  placeholder="Answer with concrete project details, trade-offs, metrics, or implementation notes."
                  className="min-h-56 w-full rounded-[2rem] border border-white/10 bg-panel/90 px-5 py-5 text-white outline-none transition focus:border-teal/60"
                />
                <button
                  type="submit"
                  disabled={submitting || answerText.trim().length < 20}
                  className="rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {submitting ? "Scoring..." : "Submit Answer"}
                </button>
              </form>
            </div>
          ) : null}
        </SectionCard>
      </div>

      <SectionCard title="Assessment History" eyebrow="Live scoring">
        {answeredQuestions.length ? (
          <div className="space-y-4">
            {answeredQuestions.map((question) => (
              <div key={question.id} className="rounded-3xl border border-white/10 bg-white/5 p-5">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <Sparkles className="h-4 w-4 text-teal" />
                      <p className="font-display text-xl text-white">{question.skill_name}</p>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-mist/75">{question.prompt}</p>
                  </div>
                  <SkillPill label={`${question.answer?.score ?? 0}%`} tone="good" />
                </div>
                <div className="mt-4 rounded-2xl border border-white/10 bg-ink/30 p-4">
                  <p className="text-sm leading-6 text-mist/80">{question.answer?.response_text}</p>
                </div>
                <p className="mt-3 text-sm text-mist/70">{question.answer?.feedback}</p>
                <p className="mt-2 text-xs uppercase tracking-[0.18em] text-mist/50">{question.answer?.explainability}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm leading-6 text-mist/75">
            Answers will appear here with immediate scoring feedback after each question is submitted.
          </p>
        )}
      </SectionCard>
    </div>
  );
}
