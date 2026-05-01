import { Download, Gauge, GraduationCap, Sparkles, Target } from "lucide-react";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { LoadingState } from "../components/LoadingState";
import { MetricCard } from "../components/MetricCard";
import { SectionCard } from "../components/SectionCard";
import { SkillPill } from "../components/SkillPill";
import { api } from "../lib/api";
import { exportElementToPdf } from "../lib/pdf";
import { useSessionStore } from "../lib/session-store";
import type { LearningPlanItem, SessionDetail, SkillAssessment } from "../types/api";

export function ReportPage() {
  const { activeSessionId, setActiveSessionId } = useSessionStore();
  const [session, setSession] = useState<SessionDetail | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    async function load() {
      if (!activeSessionId) {
        try {
          setLoading(true);
          const catalog = await api.getCatalog();
          const seededDemo = catalog.sessions.find((item) => item.name === "Seeded Demo Session") || catalog.sessions[0];
          if (!seededDemo) {
            setLoading(false);
            return;
          }
          setActiveSessionId(seededDemo.id);
          setSession(await api.getReport(seededDemo.id));
          return;
        } catch (err) {
          setError(err instanceof Error ? err.message : "Could not load the demo report.");
          setLoading(false);
          return;
        }
      }

      try {
        setLoading(true);
        setSession(await api.getReport(activeSessionId));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not load the report.");
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, [activeSessionId, setActiveSessionId]);

  async function handleExport() {
    if (!session) {
      return;
    }
    try {
      setExporting(true);
      await exportElementToPdf("report-root", `${session.resume.candidate_name.replaceAll(" ", "_")}_skill_report.pdf`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not export the PDF.");
    } finally {
      setExporting(false);
    }
  }

  if (loading) {
    return <LoadingState label="Building final report..." />;
  }

  if (!session) {
    return (
      <SectionCard title="No Report Available" eyebrow="Run the workflow first">
        <p className="text-mist/75">Complete an assessment or open the seeded demo report from the home page.</p>
        <Link
          to="/"
          className="mt-5 inline-flex items-center gap-2 rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90"
        >
          Go Home
        </Link>
      </SectionCard>
    );
  }

  const totalLearningHours = session.learning_plan.reduce((sum, item) => sum + item.estimated_hours, 0);

  return (
    <div className="space-y-6">
      {error ? <p className="rounded-2xl border border-coral/30 bg-coral/10 px-4 py-3 text-sm text-coral">{error}</p> : null}

      <SectionCard
        title="Final Assessment Report"
        eyebrow="Step 5"
        action={
          <button
            type="button"
            onClick={() => void handleExport()}
            disabled={exporting}
            className="inline-flex items-center gap-2 rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Download className="h-4 w-4" />
            {exporting ? "Exporting..." : "Export PDF"}
          </button>
        }
      >
        <div className="grid gap-4 lg:grid-cols-4">
          <MetricCard label="Skill Match" value={`${session.skill_match_percentage}%`} hint="Overlap between JD skills and resume evidence." />
          <MetricCard label="Assessment Score" value={`${session.overall_assessment_score}%`} hint="Average of scored answers across assessed skills." />
          <MetricCard label="Final Readiness" value={`${session.overall_readiness_score}%`} hint="Weighted combination of resume match and assessment performance." />
          <MetricCard label="Learning Time" value={`${totalLearningHours}h`} hint="Estimated time to close the main capability gaps." />
        </div>
      </SectionCard>

      <div id="report-root" className="space-y-6 rounded-[2rem] border border-white/10 bg-panel/60 p-4 sm:p-6">
        <SectionCard title={`${session.resume.candidate_name} x ${session.job_description.title}`} eyebrow="Report summary">
          <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
            <div className="rounded-[2rem] border border-white/10 bg-white/5 p-6">
              <p className="text-sm uppercase tracking-[0.22em] text-teal/80">Candidate snapshot</p>
              <h3 className="mt-3 font-display text-3xl text-white">{session.resume.candidate_name}</h3>
              <p className="mt-2 text-mist/70">{session.resume.headline || "Candidate profile"}</p>
              <div className="mt-5 flex flex-wrap gap-2">
                {session.summary.strongest_skills.map((skill) => (
                  <SkillPill key={skill} label={skill} tone="good" />
                ))}
              </div>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <SummaryStack icon={<Gauge className="h-5 w-5" />} title="Scoring Formula" body={session.summary.formula} />
              <SummaryStack
                icon={<Target className="h-5 w-5" />}
                title="Priority gaps"
                body={session.summary.priority_gaps.length ? session.summary.priority_gaps.join(", ") : "No critical gaps surfaced."}
              />
              <SummaryStack
                icon={<Sparkles className="h-5 w-5" />}
                title="Matching skills"
                body={session.summary.matching_skills.length ? session.summary.matching_skills.join(", ") : "No direct overlaps yet."}
              />
              <SummaryStack
                icon={<GraduationCap className="h-5 w-5" />}
                title="Missing skills"
                body={session.summary.missing_skills.length ? session.summary.missing_skills.join(", ") : "No missing skills detected."}
              />
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Per-Skill Proficiency" eyebrow="Detailed scores">
          <div className="space-y-4">
            {session.skills.map((skill) => (
              <SkillScoreRow key={skill.id} skill={skill} />
            ))}
          </div>
        </SectionCard>

        <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <SectionCard title="Gap Analysis" eyebrow="Why each score landed there">
            <div className="space-y-4">
              {session.skills
                .filter((skill) => skill.gap_priority !== "Low" || skill.final_skill_score < 80)
                .map((skill) => (
                  <div key={skill.id} className="rounded-3xl border border-white/10 bg-white/5 p-5">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <p className="font-display text-xl text-white">{skill.skill_name}</p>
                        <p className="mt-1 text-sm text-mist/70">{skill.explainability}</p>
                      </div>
                      <SkillPill
                        label={skill.gap_priority}
                        tone={skill.gap_priority === "High" ? "alert" : skill.gap_priority === "Medium" ? "warn" : "good"}
                      />
                    </div>
                  </div>
                ))}
            </div>
          </SectionCard>

          <SectionCard title="Personalised Learning Plan" eyebrow="Action plan">
            <div className="space-y-4">
              {session.learning_plan.map((item) => (
                <LearningPlanCard key={item.id} item={item} />
              ))}
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}

function SummaryStack({ icon, title, body }: { icon: ReactNode; title: string; body: string }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
      <div className="inline-flex rounded-2xl bg-teal/10 p-3 text-teal">{icon}</div>
      <p className="mt-4 font-display text-xl text-white">{title}</p>
      <p className="mt-2 text-sm leading-6 text-mist/75">{body}</p>
    </div>
  );
}

function SkillScoreRow({ skill }: { skill: SkillAssessment }) {
  const scoreTone =
    skill.final_skill_score >= 80 ? "bg-teal" : skill.final_skill_score >= 60 ? "bg-sand" : "bg-coral";

  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <p className="font-display text-xl text-white">{skill.skill_name}</p>
            <SkillPill label={skill.category} tone="neutral" />
          </div>
          <p className="mt-2 text-sm text-mist/70">
            Resume Match {skill.resume_match_score}% | Assessment {skill.assessment_score}% | Importance {skill.importance}/5
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-mist/70">Final score</p>
          <p className="font-display text-3xl text-white">{skill.final_skill_score}%</p>
        </div>
      </div>
      <div className="mt-4 h-3 overflow-hidden rounded-full bg-white/10">
        <div className={`h-full rounded-full ${scoreTone}`} style={{ width: `${Math.min(skill.final_skill_score, 100)}%` }} />
      </div>
    </div>
  );
}

function LearningPlanCard({ item }: { item: LearningPlanItem }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="font-display text-xl text-white">{item.skill_name}</p>
          <p className="mt-1 text-sm text-mist/70">
            {item.timeline} | {item.estimated_hours} hours
          </p>
        </div>
        <SkillPill label={item.priority} tone={item.priority === "High" ? "alert" : item.priority === "Medium" ? "warn" : "good"} />
      </div>
      <p className="mt-4 text-sm leading-6 text-mist/80">{item.focus_area}</p>
      <p className="mt-3 text-sm leading-6 text-mist/65">{item.reason}</p>
      <div className="mt-4 grid gap-3">
        {item.resources.map((resource) => (
          <a
            key={resource.url}
            href={resource.url}
            target="_blank"
            rel="noreferrer"
            className="rounded-2xl border border-white/10 bg-ink/30 px-4 py-3 text-sm text-mist transition hover:border-teal/30 hover:text-white"
          >
            {resource.title}
          </a>
        ))}
      </div>
    </div>
  );
}
