import { ArrowRight, Upload } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { LoadingState } from "../components/LoadingState";
import { SectionCard } from "../components/SectionCard";
import { SkillPill } from "../components/SkillPill";
import { api } from "../lib/api";
import { useSessionStore } from "../lib/session-store";
import type { JobDescription, Resume } from "../types/api";

export function ResumePage() {
  const navigate = useNavigate();
  const { selectedJobId, selectedResumeId, setSelectedResumeId, setActiveSessionId } = useSessionStore();
  const [catalogResumes, setCatalogResumes] = useState<Resume[]>([]);
  const [catalogJobs, setCatalogJobs] = useState<JobDescription[]>([]);
  const [candidateName, setCandidateName] = useState("");
  const [headline, setHeadline] = useState("");
  const [rawText, setRawText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const catalog = await api.getCatalog();
        setCatalogResumes(catalog.resumes);
        setCatalogJobs(catalog.job_descriptions);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not load seeded resumes.");
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, []);

  const selectedJob = catalogJobs.find((job) => job.id === selectedJobId);

  async function runAnalysis(resumeId: number) {
    if (!selectedJobId) {
      setError("Pick a job description first so the assessment has a target role.");
      return;
    }
    const session = await api.analyzeCandidate(selectedJobId, resumeId);
    setSelectedResumeId(resumeId);
    setActiveSessionId(session.id);
    navigate("/analysis");
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      setSubmitting(true);
      setError("");
      const formData = new FormData();
      formData.append("candidate_name", candidateName);
      if (headline.trim()) {
        formData.append("headline", headline);
      }
      if (rawText.trim()) {
        formData.append("raw_text", rawText);
      }
      if (file) {
        formData.append("file", file);
      }
      const created = await api.createResume(formData);
      await runAnalysis(created.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save the resume.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <LoadingState label="Loading resume catalog..." />;
  }

  return (
    <div className="space-y-6">
      {!selectedJob ? (
        <SectionCard title="Select A Job Description First" eyebrow="Workflow guardrail">
          <p className="max-w-2xl text-mist/75">
            The resume needs to be assessed against a target role. Pick or upload a job description before creating the candidate record.
          </p>
          <Link
            to="/job-description"
            className="mt-5 inline-flex items-center gap-2 rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90"
          >
            Go To Job Description
            <ArrowRight className="h-4 w-4" />
          </Link>
        </SectionCard>
      ) : (
        <SectionCard title="Selected Job" eyebrow="Current target role">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="font-display text-2xl text-white">{selectedJob.title}</p>
              <p className="mt-1 text-mist/70">{selectedJob.company || "Independent brief"}</p>
            </div>
            <SkillPill label={`ID ${selectedJob.id}`} tone="good" />
          </div>
        </SectionCard>
      )}

      <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <SectionCard title="Add Candidate Resume" eyebrow="Step 2">
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="grid gap-4 md:grid-cols-2">
              <label className="space-y-2">
                <span className="text-sm text-mist/70">Candidate name</span>
                <input
                  value={candidateName}
                  onChange={(event) => setCandidateName(event.target.value)}
                  placeholder="Sarah Chen"
                  className="w-full rounded-2xl border border-white/10 bg-ink/40 px-4 py-3 text-white outline-none transition focus:border-teal/60"
                  required
                />
              </label>
              <label className="space-y-2">
                <span className="text-sm text-mist/70">Headline</span>
                <input
                  value={headline}
                  onChange={(event) => setHeadline(event.target.value)}
                  placeholder="Product-minded Full-Stack Engineer"
                  className="w-full rounded-2xl border border-white/10 bg-ink/40 px-4 py-3 text-white outline-none transition focus:border-teal/60"
                />
              </label>
            </div>

            <label className="space-y-2">
              <span className="text-sm text-mist/70">Paste the resume text</span>
              <textarea
                value={rawText}
                onChange={(event) => setRawText(event.target.value)}
                placeholder="Paste the resume if you are not uploading a file."
                className="min-h-64 w-full rounded-3xl border border-white/10 bg-ink/40 px-4 py-4 text-white outline-none transition focus:border-teal/60"
              />
            </label>

            <label className="flex cursor-pointer items-center justify-between rounded-3xl border border-dashed border-white/15 bg-white/5 px-4 py-5 transition hover:border-teal/40">
              <div>
                <p className="font-medium text-white">Upload PDF, DOCX, or TXT</p>
                <p className="text-sm text-mist/70">{file ? file.name : "Direct text input also works."}</p>
              </div>
              <Upload className="h-5 w-5 text-teal" />
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                className="hidden"
                onChange={(event) => setFile(event.target.files?.[0] ?? null)}
              />
            </label>

            {error ? <p className="rounded-2xl border border-coral/30 bg-coral/10 px-4 py-3 text-sm text-coral">{error}</p> : null}

            <button
              type="submit"
              disabled={submitting || !selectedJob}
              className="rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {submitting ? "Creating assessment..." : "Save Resume And Run Analysis"}
            </button>
          </form>
        </SectionCard>

        <SectionCard title="Seeded Resumes" eyebrow="Fast demo path">
          <div className="space-y-4">
            {catalogResumes.map((resume) => (
              <button
                key={resume.id}
                type="button"
                onClick={() => void runAnalysis(resume.id)}
                className={`w-full rounded-3xl border p-5 text-left transition ${
                  selectedResumeId === resume.id
                    ? "border-teal/40 bg-teal/10"
                    : "border-white/10 bg-white/5 hover:border-teal/30 hover:bg-white/10"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-display text-xl text-white">{resume.candidate_name}</p>
                    <p className="mt-1 text-sm text-mist/70">{resume.headline || "Candidate profile"}</p>
                  </div>
                  <SkillPill label={resume.source_type} tone="neutral" />
                </div>
                <p className="mt-4 text-sm leading-6 text-mist/75">{resume.preview}...</p>
              </button>
            ))}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}
