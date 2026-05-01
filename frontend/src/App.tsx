import { BrowserRouter, Route, Routes } from "react-router-dom";

import { AppShell } from "./components/AppShell";
import { SessionStoreProvider } from "./lib/session-store";
import { AnalysisPage } from "./pages/AnalysisPage";
import { AssessmentPage } from "./pages/AssessmentPage";
import { HomePage } from "./pages/HomePage";
import { JobDescriptionPage } from "./pages/JobDescriptionPage";
import { ReportPage } from "./pages/ReportPage";
import { ResumePage } from "./pages/ResumePage";

export default function App() {
  return (
    <SessionStoreProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/job-description" element={<JobDescriptionPage />} />
            <Route path="/resume" element={<ResumePage />} />
            <Route path="/analysis" element={<AnalysisPage />} />
            <Route path="/assessment" element={<AssessmentPage />} />
            <Route path="/report" element={<ReportPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </SessionStoreProvider>
  );
}
