import { ArrowRight, CheckCircle2, Sparkle, Target, TriangleAlert } from "lucide-react";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { LoadingState } from "../components/LoadingState";
import { MetricCard } from "../components/MetricCard";
import { SectionCard } from "../components/SectionCard";
import { SkillPill } from "../components/SkillPill";
import { api } from "../lib/api";
import { useSessionStore } from "../lib/session-store";
import type { SessionDetail } from "../types/api";

export function AnalysisPage() {
  const navigate = useNavigate();
  const { activeSessionId, selectedJobId, selectedResumeId, setActiveSessionId } = useSessionStore();
  const [session, setSession] = useState<SessionDetail | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [generatingQuestions, setGeneratingQuestions] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError("");
        let resolvedSessionId = activeSessionId;
        if (!resolvedSessionId && selectedJobId && selectedResumeId) {
          const created = await api.analyzeCandidate(selectedJobId, selectedResumeId);
          resolvedSessionId = created.id;
          setActiveSessionId(created.id);
          setSession(created);
          return;
        }
        if (!resolvedSessionId) {
          setLoading(false);
          return;
        }
        setSession(await api.getSession(resolvedSessionId));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not load the analysis.");
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, [activeSessionId, selectedJobId, selectedResumeId, setActiveSessionId]);

  async function handleStartAssessment() {
    if (!session) {
      return;
    }
    try {
      setGeneratingQuestions(true);
      const response = await api.generateQuestions(session.id);
      setSession(response.session);
      navigate("/assessment");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not generate assessment questions.");
    } finally {
      setGeneratingQuestions(false);
    }
  }

  if (loading) {
    return <LoadingState label="Running skill gap analysis..." />;
  }

  if (!session) {
    return (
      <SectionCard title="No Active Session" eyebrow="Start intake first">
        <p className="text-mist/75">Create or open an assessment session to see the skill gap analysis.</p>
        <Link
          to="/job-description"
          className="mt-5 inline-flex items-center gap-2 rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90"
        >
          Start Intake
          <ArrowRight className="h-4 w-4" />
        </Link>
      </SectionCard>
    );
  }

  return (
    <div className="space-y-6">
      {error ? <p className="rounded-2xl border border-coral/30 bg-coral/10 px-4 py-3 text-sm text-coral">{error}</p> : null}

      <SectionCard
        title={session.name}
        eyebrow="Step 3"
        action={
          <button
            type="button"
            onClick={() => void handleStartAssessment()}
            disabled={generatingQuestions}
            className="rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {generatingQuestions ? "Generating..." : session.questions.length ? "Continue Assessment" : "Start Assessment"}
          </button>
        }
      >
        <div className="grid gap-4 lg:grid-cols-3">
          <MetricCard
            label="Skill Match"
            value={`${session.skill_match_percentage}%`}
            hint={`${session.summary.matched_skill_count}/${session.summary.total_required_skills} required skills appear in the resume.`}
          />
          <MetricCard
            label="Assessment"
            value={`${session.overall_assessment_score}%`}
            hint="This will update after the candidate answers the generated questions."
          />
          <MetricCard
            label="Readiness"
            value={`${session.overall_readiness_score}%`}
            hint="Weighted view of current fit against the target role."
          />
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          <SkillPill label={`Candidate: ${session.resume.candidate_name}`} tone="good" />
          <SkillPill label={`Role: ${session.job_description.title}`} tone="neutral" />
          <SkillPill label={session.summary.formula} tone="warn" />
        </div>
      </SectionCard>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <SectionCard title="Gap Summary" eyebrow="Key findings">
          <div className="space-y-4">
            <InsightBlock
              icon={<CheckCircle2 className="h-5 w-5" />}
              title="Matching skills"
              tone="good"
              items={session.summary.matching_skills}
            />
            <InsightBlock
              icon={<TriangleAlert className="h-5 w-5" />}
              title="Missing skills"
              tone="alert"
              items={session.summary.missing_skills}
            />
            <InsightBlock
              icon={<Target className="h-5 w-5" />}
              title="Priority gaps"
              tone="warn"
              items={session.summary.priority_gaps}
            />
            <InsightBlock
              icon={<Sparkle className="h-5 w-5" />}
              title="Strongest signals"
              tone="neutral"
              items={session.summary.strongest_skills}
            />
          </div>
        </SectionCard>

        <SectionCard title="Skill-Level Breakdown" eyebrow="Explainable scoring">
          <div className="space-y-4">
            {session.skills.map((skill) => (
              <div key={skill.id} className="rounded-3xl border border-white/10 bg-white/5 p-5">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="font-display text-xl text-white">{skill.skill_name}</p>
                      <SkillPill
                        label={skill.gap_priority}
                        tone={skill.gap_priority === "High" ? "alert" : skill.gap_priority === "Medium" ? "warn" : "good"}
                      />
                    </div>
                    <p className="mt-2 text-sm text-mist/70">
                      Category: {skill.category} | Importance: {skill.importance}/5
                    </p>
                  </div>
                  <div className="min-w-40 text-right">
                    <p className="text-sm text-mist/70">Final Score</p>
                    <p className="font-display text-3xl text-white">{skill.final_skill_score}%</p>
                  </div>
                </div>
                <div className="mt-4 grid gap-3 sm:grid-cols-3">
                  <ScoreChip label="Resume Match" value={skill.resume_match_score} />
                  <ScoreChip label="Assessment" value={skill.assessment_score} />
                  <ScoreChip label="Gap Priority Score" value={skill.gap_priority_score} />
                </div>
                <p className="mt-4 text-sm leading-6 text-mist/75">{skill.explainability}</p>
                <div className="mt-4 grid gap-4 lg:grid-cols-2">
                  <EvidenceList label="JD evidence" items={skill.evidence.job_snippets} />
                  <EvidenceList label="Resume evidence" items={skill.evidence.resume_snippets} />
                </div>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

function InsightBlock({
  icon,
  title,
  tone,
  items,
}: {
  icon: ReactNode;
  title: string;
  tone: "good" | "warn" | "alert" | "neutral";
  items: string[];
}) {
  const className =
    tone === "good"
      ? "border-teal/20 bg-teal/10 text-teal"
      : tone === "warn"
        ? "border-sand/20 bg-sand/10 text-sand"
        : tone === "alert"
          ? "border-coral/20 bg-coral/10 text-coral"
          : "border-white/10 bg-white/5 text-mist";

  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
      <div className="flex items-center gap-3">
        <div className={`rounded-2xl border p-2 ${className}`}>{icon}</div>
        <h3 className="font-display text-xl text-white">{title}</h3>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {items.length ? items.map((item) => <SkillPill key={item} label={item} tone={tone} />) : <SkillPill label="None detected" tone="neutral" />}
      </div>
    </div>
  );
}

function ScoreChip({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-ink/30 p-4">
      <p className="text-xs uppercase tracking-[0.2em] text-mist/55">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-white">{value}%</p>
    </div>
  );
}

function EvidenceList({ label, items }: { label: string; items: string[] }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-ink/30 p-4">
      <p className="text-xs uppercase tracking-[0.2em] text-mist/55">{label}</p>
      <div className="mt-3 space-y-2">
        {items.length ? (
          items.map((item) => (
            <p key={item} className="text-sm leading-6 text-mist/75">
              {item}
            </p>
          ))
        ) : (
          <p className="text-sm text-mist/55">No clear supporting snippet was detected.</p>
        )}
      </div>
    </div>
  );
}
