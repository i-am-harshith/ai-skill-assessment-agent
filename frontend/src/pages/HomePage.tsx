import { ArrowRight, FileText, GraduationCap, MessageSquareText, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { MetricCard } from "../components/MetricCard";
import { SectionCard } from "../components/SectionCard";
import { SkillPill } from "../components/SkillPill";
import { LoadingState } from "../components/LoadingState";
import { api } from "../lib/api";
import { useSessionStore } from "../lib/session-store";
import type { CatalogResponse, SessionListItem } from "../types/api";

export function HomePage() {
  const navigate = useNavigate();
  const { setActiveSessionId } = useSessionStore();
  const [catalog, setCatalog] = useState<CatalogResponse | null>(null);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCatalog() {
      try {
        setLoading(true);
        setCatalog(await api.getCatalog());
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not load the demo catalog.");
      } finally {
        setLoading(false);
      }
    }

    void loadCatalog();
  }, []);

  const demoSession = catalog?.sessions.find((session) => session.name === "Seeded Demo Session") || catalog?.sessions[0];

  if (loading) {
    return <LoadingState label="Loading seeded demo data..." />;
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[2rem] border border-white/10 bg-panel/70 p-8 shadow-glow">
        <div className="grid gap-8 lg:grid-cols-[1.4fr_0.9fr]">
          <div>
            <p className="text-sm uppercase tracking-[0.28em] text-teal/80">Hackathon-ready prototype</p>
            <h1 className="mt-4 max-w-3xl font-display text-5xl leading-tight text-white sm:text-6xl">
              Turn a job description and a resume into a scored skill gap report with a learning plan.
            </h1>
            <p className="mt-5 max-w-2xl text-lg text-mist/75">
              The workflow extracts required skills, compares resume claims, runs a conversational assessment, explains scoring,
              and produces a polished PDF-ready report.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                to="/job-description"
                className="inline-flex items-center gap-2 rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90"
              >
                Start New Assessment
                <ArrowRight className="h-4 w-4" />
              </Link>
              {demoSession ? (
                <button
                  type="button"
                  onClick={() => {
                    setActiveSessionId(demoSession.id);
                    navigate(demoSession.status === "completed" ? "/report" : "/analysis");
                  }}
                  className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-5 py-3 font-semibold text-mist transition hover:bg-white/10 hover:text-white"
                >
                  Open Seeded Demo
                  <Sparkles className="h-4 w-4" />
                </button>
              ) : null}
            </div>
            <div className="mt-8 flex flex-wrap gap-2">
              <SkillPill label="Resume Parsing" tone="good" />
              <SkillPill label="Skill Gap Analysis" tone="good" />
              <SkillPill label="Conversational Assessment" tone="warn" />
              <SkillPill label="PDF Report Export" tone="neutral" />
            </div>
          </div>
          <div className="grid gap-4">
            <MetricCard
              label="Seeded Sessions"
              value={`${catalog?.sessions.length ?? 0}`}
              hint="Includes one completed demo session and reusable seeded records."
            />
            <MetricCard
              label="Job Descriptions"
              value={`${catalog?.job_descriptions.length ?? 0}`}
              hint="Use seeded records or upload/paste your own JD."
            />
            <MetricCard
              label="Resumes"
              value={`${catalog?.resumes.length ?? 0}`}
              hint="Supports PDF, DOCX, TXT, and direct text input."
            />
          </div>
        </div>
      </section>

      {error ? <p className="rounded-2xl border border-coral/30 bg-coral/10 px-4 py-3 text-sm text-coral">{error}</p> : null}

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <SectionCard title="What The Demo Covers" eyebrow="End-to-end flow">
          <div className="grid gap-4 sm:grid-cols-2">
            {[
              {
                icon: <FileText className="h-5 w-5" />,
                title: "Structured Intake",
                body: "Upload or paste a job description and resume, then persist them in SQLite for later review.",
              },
              {
                icon: <Sparkles className="h-5 w-5" />,
                title: "Explainable Scoring",
                body: "Each skill is scored with a transparent 40/60 formula combining resume evidence and assessment results.",
              },
              {
                icon: <MessageSquareText className="h-5 w-5" />,
                title: "Guided Assessment",
                body: "Candidates answer one focused question at a time in a demo-friendly conversational flow.",
              },
              {
                icon: <GraduationCap className="h-5 w-5" />,
                title: "Learning Plan",
                body: "Low-scoring skills turn into a targeted plan with resources, priority, and estimated hours.",
              },
            ].map((item) => (
              <div key={item.title} className="rounded-3xl border border-white/10 bg-white/5 p-5">
                <div className="mb-4 inline-flex rounded-2xl bg-teal/10 p-3 text-teal">{item.icon}</div>
                <h3 className="font-display text-xl text-white">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-mist/75">{item.body}</p>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Seeded Demo Sessions" eyebrow="Quick launch">
          <div className="space-y-4">
            {catalog?.sessions.map((session) => (
              <SeedSessionCard
                key={session.id}
                session={session}
                onOpen={() => {
                  setActiveSessionId(session.id);
                  navigate(session.status === "completed" ? "/report" : "/analysis");
                }}
              />
            ))}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

function SeedSessionCard({ session, onOpen }: { session: SessionListItem; onOpen: () => void }) {
  return (
    <button
      type="button"
      onClick={onOpen}
      className="w-full rounded-3xl border border-white/10 bg-white/5 p-5 text-left transition hover:border-teal/30 hover:bg-white/10"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="font-display text-xl text-white">{session.name}</p>
          <p className="mt-1 text-sm text-mist/70">
            {session.candidate_name} for {session.job_title}
          </p>
        </div>
        <SkillPill
          label={session.status === "completed" ? "Demo Ready" : session.status.replaceAll("_", " ")}
          tone={session.status === "completed" ? "good" : "warn"}
        />
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <MiniMetric label="Match" value={`${session.skill_match_percentage}%`} />
        <MiniMetric label="Readiness" value={`${session.overall_readiness_score}%`} />
        <MiniMetric label="Answered" value={`${session.progress.answered_questions}/${session.progress.total_questions}`} />
      </div>
    </button>
  );
}

function MiniMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-ink/30 p-3">
      <p className="text-xs uppercase tracking-[0.2em] text-mist/55">{label}</p>
      <p className="mt-2 text-xl font-semibold text-white">{value}</p>
    </div>
  );
}
