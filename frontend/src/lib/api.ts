import type {
  CatalogResponse,
  GenerateQuestionsResponse,
  JobDescription,
  QuestionsResponse,
  Resume,
  SessionDetail,
  SessionListItem,
  SubmitAnswerResponse,
} from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail || "The request failed.");
  }
  return response.json() as Promise<T>;
}

export const api = {
  getCatalog: () => apiFetch<CatalogResponse>("/catalog"),
  getSessions: () => apiFetch<{ items: SessionListItem[] }>("/sessions"),
  getSession: (sessionId: number) => apiFetch<SessionDetail>(`/sessions/${sessionId}`),
  getReport: (sessionId: number) => apiFetch<SessionDetail>(`/sessions/${sessionId}/report`),
  createJobDescription: (formData: FormData) =>
    apiFetch<JobDescription>("/job-descriptions", {
      method: "POST",
      body: formData,
    }),
  createResume: (formData: FormData) =>
    apiFetch<Resume>("/resumes", {
      method: "POST",
      body: formData,
    }),
  analyzeCandidate: (jobDescriptionId: number, resumeId: number, sessionName?: string | null) =>
    apiFetch<SessionDetail>("/sessions/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        job_description_id: jobDescriptionId,
        resume_id: resumeId,
        session_name: sessionName || null,
      }),
    }),
  generateQuestions: (sessionId: number) =>
    apiFetch<GenerateQuestionsResponse>(`/sessions/${sessionId}/questions/generate`, {
      method: "POST",
    }),
  getQuestions: (sessionId: number) => apiFetch<QuestionsResponse>(`/sessions/${sessionId}/questions`),
  submitAnswer: (sessionId: number, questionId: number, responseText: string) =>
    apiFetch<SubmitAnswerResponse>(`/sessions/${sessionId}/answers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question_id: questionId,
        response_text: responseText,
      }),
    }),
};
