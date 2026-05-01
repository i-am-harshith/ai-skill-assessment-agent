import type { ReactNode } from "react";
import { createContext, useContext, useEffect, useState } from "react";

interface SessionStoreValue {
  selectedJobId: number | null;
  selectedResumeId: number | null;
  activeSessionId: number | null;
  setSelectedJobId: (value: number | null) => void;
  setSelectedResumeId: (value: number | null) => void;
  setActiveSessionId: (value: number | null) => void;
  resetWorkflow: () => void;
}

const SessionStoreContext = createContext<SessionStoreValue | undefined>(undefined);

const STORAGE_KEY = "ai-skill-assessment-store";

export function SessionStoreProvider({ children }: { children: ReactNode }) {
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null);
  const [selectedResumeId, setSelectedResumeId] = useState<number | null>(null);
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);

  useEffect(() => {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return;
    }
    try {
      const parsed = JSON.parse(raw) as {
        selectedJobId: number | null;
        selectedResumeId: number | null;
        activeSessionId: number | null;
      };
      setSelectedJobId(parsed.selectedJobId);
      setSelectedResumeId(parsed.selectedResumeId);
      setActiveSessionId(parsed.activeSessionId);
    } catch {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        selectedJobId,
        selectedResumeId,
        activeSessionId,
      }),
    );
  }, [selectedJobId, selectedResumeId, activeSessionId]);

  return (
    <SessionStoreContext.Provider
      value={{
        selectedJobId,
        selectedResumeId,
        activeSessionId,
        setSelectedJobId,
        setSelectedResumeId,
        setActiveSessionId,
        resetWorkflow: () => {
          setSelectedJobId(null);
          setSelectedResumeId(null);
          setActiveSessionId(null);
        },
      }}
    >
      {children}
    </SessionStoreContext.Provider>
  );
}

export function useSessionStore() {
  const context = useContext(SessionStoreContext);
  if (!context) {
    throw new Error("useSessionStore must be used inside SessionStoreProvider.");
  }
  return context;
}
