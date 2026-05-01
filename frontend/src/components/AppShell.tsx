import { ArrowRight, BrainCircuit, RefreshCcw } from "lucide-react";
import { Link, Outlet, useNavigate } from "react-router-dom";

import { StepNav } from "./StepNav";
import { useSessionStore } from "../lib/session-store";

export function AppShell() {
  const navigate = useNavigate();
  const { resetWorkflow } = useSessionStore();

  return (
    <div className="min-h-screen bg-ink text-white">
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute left-[-10%] top-[-5%] h-80 w-80 rounded-full bg-teal/15 blur-3xl" />
        <div className="absolute bottom-[-10%] right-[-5%] h-96 w-96 rounded-full bg-coral/15 blur-3xl" />
      </div>
      <div className="relative mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
        <header className="rounded-[2rem] border border-white/10 bg-panel/80 px-6 py-5 backdrop-blur">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-3xl">
              <Link to="/" className="inline-flex items-center gap-3 text-white">
                <span className="rounded-2xl bg-teal/20 p-2 text-teal">
                  <BrainCircuit className="h-5 w-5" />
                </span>
                <div>
                  <p className="font-display text-xl">AI-Powered Skill Assessment Agent</p>
                  <p className="text-sm text-mist/70">Offline-first resume screening, assessment, scoring, and learning plans.</p>
                </div>
              </Link>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={() => {
                  resetWorkflow();
                  navigate("/job-description");
                }}
                className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-mist/80 transition hover:bg-white/10 hover:text-white"
              >
                <RefreshCcw className="h-4 w-4" />
                New Workflow
              </button>
              <Link
                to="/report"
                className="inline-flex items-center gap-2 rounded-full bg-teal px-4 py-2 text-sm font-semibold text-ink transition hover:bg-teal/90"
              >
                Demo Report
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
          <div className="mt-6">
            <StepNav />
          </div>
        </header>
        <main className="mt-6 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
