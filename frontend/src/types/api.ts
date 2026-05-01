export interface JobDescription {
  id: number;
  title: string;
  company: string | null;
  source_type: string;
  file_name: string | null;
  created_at: string;
  raw_text?: string;
  preview: string;
}

export interface Resume {
  id: number;
  candidate_name: string;
  headline: string | null;
  source_type: string;
  file_name: string | null;
  created_at: string;
  raw_text?: string;
  preview: string;
}

export interface Answer {
  id: number;
  question_id: number;
  response_text: string;
  score: number;
  feedback: string;
  explainability: string;
  created_at: string;
}

export interface Question {
  id: number;
  skill_assessment_id: number;
  skill_name: string;
  prompt: string;
  guidance: string;
  difficulty: string;
  order_index: number;
  answered: boolean;
  answer: Answer | null;
}

export interface SkillAssessment {
  id: number;
  skill_name: string;
  category: string;
  importance: number;
  required: boolean;
  claimed: boolean;
  resume_match_score: number;
  assessment_score: number;
  final_skill_score: number;
  gap_priority: string;
  gap_priority_score: number;
  explainability: string;
  evidence: {
    job_snippets: string[];
    resume_snippets: string[];
  };
}

export interface LearningPlanItem {
  id: number;
  skill_name: string;
  priority: string;
  focus_area: string;
  estimated_hours: number;
  timeline: string;
  reason: string;
  resources: Array<{
    title: string;
    url: string;
  }>;
}

export interface SessionDetail {
  id: number;
  name: string;
  status: string;
  skill_match_percentage: number;
  overall_assessment_score: number;
  overall_readiness_score: number;
  created_at: string;
  updated_at: string;
  job_description: JobDescription;
  resume: Resume;
  summary: {
    matching_skills: string[];
    missing_skills: string[];
    priority_gaps: string[];
    strongest_skills: string[];
    formula: string;
    total_required_skills: number;
    matched_skill_count: number;
  };
  skills: SkillAssessment[];
  questions: Question[];
  learning_plan: LearningPlanItem[];
  progress: {
    answered_questions: number;
    total_questions: number;
    completion_percentage: number;
  };
}

export interface SessionListItem {
  id: number;
  name: string;
  status: string;
  skill_match_percentage: number;
  overall_assessment_score: number;
  overall_readiness_score: number;
  job_title: string;
  candidate_name: string;
  created_at: string;
  progress: {
    answered_questions: number;
    total_questions: number;
    completion_percentage: number;
  };
}

export interface CatalogResponse {
  job_descriptions: JobDescription[];
  resumes: Resume[];
  sessions: SessionListItem[];
}

export interface QuestionsResponse {
  items: Question[];
  next_question: Question | null;
}

export interface GenerateQuestionsResponse {
  session: SessionDetail;
  next_question: Question | null;
}

export interface SubmitAnswerResponse {
  submitted: Answer;
  session: SessionDetail;
  next_question: Question | null;
}
