# Demo Script (3-5 Minutes)

## 1. Open The App

- Start backend and frontend
- Open `http://localhost:5173`
- Explain that the app works offline-first and includes seeded demo data

## 2. Show The Home Page

Talk track:

- This agent compares job requirements with candidate claims
- It then validates important skills through a conversational assessment
- Finally it generates a personalised learning plan and PDF report

Action:

- Click `Open Seeded Demo`

## 3. Show Skill Gap Analysis

Talk track:

- The backend extracts required JD skills and claimed resume skills
- It calculates skill match and highlights matching, missing, and priority-gap skills
- Every skill has explainable scoring notes and evidence snippets

Action:

- Point to `Skill Match`
- Highlight `Matching skills`, `Missing skills`, and one `High` priority gap

## 4. Show Conversational Assessment

Action:

- Navigate to the assessment page if the session is not already completed
- Answer one question manually if you want a live scoring moment

Talk track:

- The system asks one focused question at a time
- Each answer is scored using technical depth, evidence, and clarity
- The score feeds back into final proficiency immediately

## 5. Show Final Report

Talk track:

- The final report blends resume match and assessment performance
- It exposes final proficiency per skill
- It also recommends what to learn next, how urgent it is, and how long it may take

Action:

- Show one or two learning plan cards
- Point out the scoring formula
- Click `Export PDF`

## 6. Close

Suggested close:

- This prototype can be used by recruiters, hiring managers, bootcamps, or internal L&D teams
- The current version runs locally with SQLite and an offline scoring engine, and can later switch to OpenAI without changing the UI flow
