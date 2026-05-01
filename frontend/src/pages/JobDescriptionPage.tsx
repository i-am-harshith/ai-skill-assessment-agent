import { Upload } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { LoadingState } from "../components/LoadingState";
import { SectionCard } from "../components/SectionCard";
import { SkillPill } from "../components/SkillPill";
import { api } from "../lib/api";
import { useSessionStore } from "../lib/session-store";
import type { JobDescription } from "../types/api";

export function JobDescriptionPage() {
  const navigate = useNavigate();
  const { selectedJobId, setSelectedJobId, setActiveSessionId } = useSessionStore();
  const [catalogJobs, setCatalogJobs] = useState<JobDescription[]>([]);
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
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
        setCatalogJobs(catalog.job_descriptions);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not load job descriptions.");
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, []);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      setSubmitting(true);
      setError("");
      const formData = new FormData();
      formData.append("title", title);
      if (company.trim()) {
        formData.append("company", company);
      }
      if (rawText.trim()) {
        formData.append("raw_text", rawText);
      }
      if (file) {
        formData.append("file", file);
      }
      const created = await api.createJobDescription(formData);
      setSelectedJobId(created.id);
      setActiveSessionId(null);
      navigate("/resume");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save the job description.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <LoadingState label="Loading job description catalog..." />;
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
      <SectionCard title="Add A Job Description" eyebrow="Step 1">
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="grid gap-4 md:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm text-mist/70">Role title</span>
              <input
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="Senior AI Product Engineer"
                className="w-full rounded-2xl border border-white/10 bg-ink/40 px-4 py-3 text-white outline-none transition focus:border-teal/60"
                required
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm text-mist/70">Company</span>
              <input
                value={company}
                onChange={(event) => setCompany(event.target.value)}
                placeholder="Northstar Labs"
                className="w-full rounded-2xl border border-white/10 bg-ink/40 px-4 py-3 text-white outline-none transition focus:border-teal/60"
              />
            </label>
          </div>

          <label className="space-y-2">
            <span className="text-sm text-mist/70">Paste the job description</span>
            <textarea
              value={rawText}
              onChange={(event) => setRawText(event.target.value)}
              placeholder="Paste the full JD here if you are not uploading a file."
              className="min-h-64 w-full rounded-3xl border border-white/10 bg-ink/40 px-4 py-4 text-white outline-none transition focus:border-teal/60"
            />
          </label>

          <label className="flex cursor-pointer items-center justify-between rounded-3xl border border-dashed border-white/15 bg-white/5 px-4 py-5 transition hover:border-teal/40">
            <div>
              <p className="font-medium text-white">Upload PDF, DOCX, or TXT</p>
              <p className="text-sm text-mist/70">{file ? file.name : "Manual text input is supported if you prefer."}</p>
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
            disabled={submitting}
            className="rounded-full bg-teal px-5 py-3 font-semibold text-ink transition hover:bg-teal/90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? "Saving..." : "Save Job Description"}
          </button>
        </form>
      </SectionCard>

      <SectionCard title="Seeded Job Descriptions" eyebrow="For demo">
        <div className="space-y-4">
          {catalogJobs.map((job) => (
            <button
              key={job.id}
              type="button"
              onClick={() => {
                setSelectedJobId(job.id);
                setActiveSessionId(null);
                navigate("/resume");
              }}
              className={`w-full rounded-3xl border p-5 text-left transition ${
                selectedJobId === job.id
                  ? "border-teal/40 bg-teal/10"
                  : "border-white/10 bg-white/5 hover:border-teal/30 hover:bg-white/10"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-display text-xl text-white">{job.title}</p>
                  <p className="mt-1 text-sm text-mist/70">{job.company || "Independent brief"}</p>
                </div>
                <SkillPill label={job.source_type} tone="neutral" />
              </div>
              <p className="mt-4 text-sm leading-6 text-mist/75">{job.preview}...</p>
            </button>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
