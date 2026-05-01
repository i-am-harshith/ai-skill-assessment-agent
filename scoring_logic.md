# Scoring Logic

## Core Formula

```text
Final Skill Score = 40% Resume Match + 60% Assessment Score
```

This is applied per required skill.

## 1. Skill Match Score

Purpose:

- Measure how well the resume aligns with required JD skills before interviewing

How it is derived:

- JD skills are extracted and given an importance score from `1` to `5`
- Resume skills are extracted using evidence snippets and action-oriented language
- If a required skill appears in the resume with strong evidence, it receives a higher resume match score

Interpretation:

- `0`: no evidence in the resume
- `35-60`: weak or generic evidence
- `61-80`: credible evidence
- `81-100`: strong, implementation-oriented evidence

## 2. Assessment Score

Purpose:

- Measure actual demonstrated proficiency from the candidate's answers

Signals used:

- technical depth
- implementation detail
- decision-making and trade-offs
- measurable outcomes
- clarity and structure

Low-score signals:

- vague answers
- purely theoretical replies
- explicit lack of hands-on experience

## 3. Final Skill Score

Example:

- Resume Match = `70`
- Assessment Score = `80`

```text
Final Skill Score = (0.4 × 70) + (0.6 × 80)
                  = 28 + 48
                  = 76
```

## 4. Overall Skill Match Percentage

Purpose:

- Show role-level overlap between JD and resume

Method:

- Count matched required skills
- Weight them by JD importance
- Convert to a percentage

## 5. Overall Assessment Score

Purpose:

- Show the weighted average of answered assessment skills

Method:

- Average assessment scores across assessed skills
- Weight by JD importance

## 6. Overall Readiness Score

Purpose:

- Give a final role-fit view after resume analysis and assessment

Method:

- Weighted average of all final skill scores

## 7. Gap Priority

Gap priority rises when:

- the skill is very important in the JD
- the final skill score is low

Priority bands:

- `High`
- `Medium`
- `Low`

## 8. Learning Plan Logic

Skills with lower final scores are turned into learning tasks.

Each learning item includes:

- target skill
- priority
- focus area
- estimated hours
- timeline
- resource links

Estimated hours increase when:

- job importance is high
- current proficiency is low

## Example Skill Evaluation

### Python

- JD importance: `5/5`
- Resume Match: `82`
- Assessment Score: `74`

```text
Final Skill Score = (0.4 × 82) + (0.6 × 74)
                  = 32.8 + 44.4
                  = 77.2
```

Interpretation:

- Strong base fit
- Good candidate signal
- Some learning still required for advanced scenarios
