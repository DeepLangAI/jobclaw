---
name: recruiter
description: "Help recruiters publish job postings to the job matching system. Use when users want to: (1) post a job, (2) publish a position, (3) hire someone, (4) recruit candidates, (5) find employees, or (6) advertise job openings. Supports flexible information collection - users can provide all details at once or be guided through step-by-step. Automatically creates recruiter account, generates job vectors, and enables AI-powered candidate matching."
---

# Recruiter

Publish, update, and manage job postings in the AI-powered job matching system, and view matched candidates.

## Overview

This skill helps recruiters manage job postings through an interactive conversation. Provide information flexibly - share everything at once or answer questions step-by-step. The system supports:

1. **Publish job** - Create a recruiter account, publish a job posting, and trigger AI matching
2. **Update job** - Modify job details (title, requirements, salary, etc.)
3. **Delete job** - Soft-delete job posting (mark as INACTIVE, preserving match history)
4. **View jobs** - Check all your published jobs
5. **List matched candidates** - View candidates matched by the AI system with similarity scores

## Available Scripts

- **publish_job.py** - Publish, update, delete jobs, and list matches for a specific job
- **get_profile.py** - View all your jobs and matched candidates (read-only)

## Workflow

### Publish Job (action: publish)

#### Step 1: Gather Job Posting Information

Collect the following required fields. Users can provide them in any order or all at once:

**Required fields:**

- **Job title**: Position name (e.g., "Senior Python Backend Engineer")
- **Company name**: Employer name
- **Job requirements**: Detailed requirements including skills, responsibilities, and qualifications
- **Salary range**: Compensation range (e.g., "25k-40k", "30k-50k")
- **Work location**: Office location (e.g., "Shanghai-Changning District", "Beijing-Chaoyang District")
- **Job type**: Employment type (e.g., "Full-time", "Part-time", "Contract")
- **Education requirement**: Minimum education level (e.g., "Bachelor's degree or above")
- **Experience requirement**: Required years of experience (e.g., "3-5 years", "5+ years")

**Example user inputs:**

_All at once:_

> "I want to post a job for a Python Backend Engineer at Pinduoduo in Shanghai Changning District. Salary 25k-40k. Requirements: Familiar with Python, Django/Flask frameworks, RESTful API development experience. Knowledge of MySQL, Redis databases. E-commerce or payment system experience preferred. Full-time position, bachelor's degree or above, 3-5 years experience."

_Step by step:_

> "I need to hire a developer"
> [Claude asks for job title]
> "Python Backend Engineer"
> [Claude asks for company, requirements, salary, location, etc.]

#### Step 2: Validate Completeness

Before submission, verify all required fields are present. If any are missing, ask the user to provide them.

#### Step 3: Publish Job Posting

```bash
cat <<EOF | python3 scripts/publish_job.py
{
  "action": "publish",
  "title": "<job title>",
  "companyName": "<company name>",
  "requirement": "<detailed requirements>",
  "salary": "<salary range>",
  "location": "<work location>",
  "jobType": "<employment type>",
  "education": "<education requirement>",
  "experience": "<experience requirement>",
  "status": "ACTIVE"
}
EOF
```

#### Step 4: Confirm Success

After successful publication, inform the user and **save the returned job ID** for future operations (update, delete, list matches). The token is automatically saved.

---

### Update Job (action: update)

Requires the **jobId** from a previous publish. Only changed fields need to be provided. The script will automatically use the saved token.

```bash
cat <<EOF | python3 scripts/publish_job.py
{
  "action": "update",
  "jobId": "<job id>",
  "salary": "<new salary range>",
  "requirement": "<updated requirements>"
}
EOF
```

Updatable fields: `title`, `companyName`, `requirement`, `salary`, `location`, `jobType`, `education`, `experience`, `status`.

---

### Delete Job (action: delete)

Soft-deletes the job posting by marking it as INACTIVE. Match history is preserved.

```bash
cat <<EOF | python3 scripts/publish_job.py
{
  "action": "delete",
  "jobId": "<job id>"
}
EOF
```

---

### View Jobs and Matches (get_profile.py)

Check your published jobs and matched candidates without making any changes.

#### View All Jobs

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "jobs"
}
EOF
```

#### View Specific Job Details

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "job",
  "jobId": "<job id>"
}
EOF
```

#### View Matches for Specific Job

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "matches",
  "jobId": "<job id>"
}
EOF
```

#### View All Matches Across All Jobs

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "all-matches"
}
EOF
```

#### View Full Information (all jobs + all matches)

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "full"
}
EOF
```

**When to use get_profile.py:**

- User asks "What jobs have I published?" or "Show me my jobs"
- User wants to check matches across all jobs
- User wants to review job details before updating
- User asks "Do I have any candidates?"

---

### List Matched Candidates (action: matches)

Retrieve candidates matched by the AI system for a specific job posting and provide comprehensive multi-dimensional analysis.

```bash
cat <<EOF | python3 scripts/publish_job.py
{
  "action": "matches",
  "jobId": "<job id>"
}
EOF
```

#### Step 1: Retrieve Matched Candidates

The API returns a list of matched candidates with similarity scores. Each match includes:

- Candidate details (name, resume, skills, experience, etc.)
- Similarity score (0-1 range, based on vector matching)
- Match metadata

#### Step 2: Generate Multi-Dimensional Analysis

After retrieving the matches, Claude MUST provide a comprehensive analysis for EACH matched candidate. The analysis should cover:

**1. Overall Match Assessment (总体匹配评估)**

- Match score interpretation (优秀/良好/中等/一般)
- Quick summary of why this candidate matches or doesn't match

**2. Skill Alignment Analysis (技能匹配分析)**

- ✅ Matching skills: List candidate skills that align with job requirements
- ⚠️ Skill gaps: Identify required skills the candidate lacks
- 💡 Bonus skills: Highlight additional valuable skills the candidate brings
- Skill match percentage estimate (e.g., "90% skill match")

**3. Experience Fit Analysis (经验匹配分析)**

- Years of experience comparison (required vs. actual)
- Industry/domain experience relevance
- Project complexity and scale alignment
- Seniority level match (junior/mid/senior)
- Career progression trajectory

**4. Education & Qualifications (学历与资质)**

- Education level match
- Relevant certifications
- Academic background relevance

**5. Cultural & Team Fit (文化与团队契合度)**

- Work style indicators from resume
- Team collaboration experience
- Leadership potential (if applicable)
- Communication skills evidence

**6. Compensation Expectations (薪资期望)**

- Candidate's salary expectations vs. job offer
- Negotiation room assessment
- Total compensation considerations

**7. Advantages & Disadvantages (优劣势分析)**

**Advantages (优势):**

- List 3-5 key strengths of this candidate
- Why this candidate stands out
- Unique value propositions

**Disadvantages (劣势):**

- List 2-4 potential concerns or gaps
- Risk factors to consider
- Areas where the candidate might need support

**8. Hiring Recommendation (招聘建议)**

- Priority level: 🔥 High Priority / ⭐ Medium Priority / 💭 Consider
- Recommended action: "Strongly recommend interview" / "Worth considering" / "Proceed with caution"
- Suggested interview focus areas
- Onboarding considerations

**9. Interview Strategy (面试策略)**

- Key areas to probe during interview
- Technical assessment recommendations
- Behavioral questions to ask
- Red flags to watch for

**10. Retention & Growth Potential (留任与成长潜力)**

- Long-term fit assessment
- Growth trajectory within the company
- Retention risk factors
- Development opportunities needed

#### Step 3: Provide Comparative Summary

After analyzing individual candidates, provide a comparative summary:

**Top 3 Recommendations:**
Rank the top 3 candidates with brief rationale for each.

**Candidate Distribution:**

- Excellent matches (score > 0.85): X candidates
- Good matches (score 0.75-0.85): Y candidates
- Moderate matches (score 0.65-0.75): Z candidates

**Hiring Strategy Advice:**

- Which candidates to prioritize for interviews
- Suggested interview panel composition
- Timeline recommendations
- Backup candidate strategy

#### Output Format Guidelines

**IMPORTANT: Always respond in the user's language.** If the user communicates in Chinese, respond in Chinese. If in English, respond in English. Adapt all section headers, labels, and content to match the user's language.

**Structure your analysis report as follows:**

**Report Header:**

- Title indicating this is a candidate match analysis report
- Job position and company name
- Visual separators (lines, emojis) to organize sections

**For Each Matched Candidate:**

1. **Candidate Header Section**
   - Candidate name/identifier and number
   - Visual separator line

2. **Overall Match Score** (📈)
   - Display the similarity score (e.g., 0.89) with interpretation (excellent/good/moderate/fair)
   - Brief summary of why this candidate matches or doesn't match

3. **Skill Alignment Analysis** (🔧)
   - ✅ List matching skills with experience levels
   - 💡 Highlight bonus skills (beyond requirements)
   - ⚠️ Identify skill gaps (required but missing)
   - Provide skill match percentage estimate

4. **Experience Fit Analysis** (💼)
   - Compare required vs. actual years of experience
   - Assess industry/domain experience relevance
   - Evaluate project complexity and scale alignment
   - Determine seniority level match
   - Review career progression trajectory

5. **Education & Qualifications** (🎓)
   - Education level match
   - Relevant certifications
   - Academic background relevance

6. **Cultural & Team Fit** (🤝)
   - Work style indicators from resume
   - Team collaboration experience
   - Leadership potential (if applicable)
   - Communication skills evidence

7. **Compensation Expectations** (💰)
   - Candidate's salary expectations vs. job offer
   - Negotiation room assessment
   - Total compensation considerations

8. **Advantages & Disadvantages** (✅ ⚠️)
   - List 3-5 key strengths of this candidate
   - List 2-4 potential concerns or gaps
   - Be objective and balanced

9. **Hiring Recommendation** (🎯)
   - Priority level: 🔥 High Priority / ⭐ Medium Priority / 💭 Consider
   - Recommended action with clear reasoning
   - Suggested interview focus areas
   - Onboarding considerations

10. **Interview Strategy** (📝)
    - Key areas to probe during interview
    - Technical assessment recommendations
    - Behavioral questions to ask
    - Red flags to watch for

11. **Retention & Growth Potential** (🚀)
    - Long-term fit assessment
    - Growth trajectory within the company
    - Retention risk factors
    - Development opportunities needed

**After Individual Candidate Analysis:**

**Comparative Summary Section:**

1. **Top 3 Recommendations** (🏆)
   - Rank top 3 candidates with medal emojis (🥇🥈🥉)
   - Brief rationale for each ranking

2. **Candidate Distribution** (📈)
   - Count of excellent matches (score > 0.85)
   - Count of good matches (score 0.75-0.85)
   - Count of moderate matches (score 0.65-0.75)

3. **Hiring Strategy Advice** (💡)
   - Which candidates to prioritize for interviews
   - Suggested interview panel composition
   - Timeline recommendations
   - Backup candidate strategy
   - Risk mitigation strategies

4. **Action Checklist** (🎯)
   - Immediate next steps (contact candidates, schedule interviews)
   - Preparation tasks (interview questions, evaluation criteria)
   - Budget/compensation considerations
   - Process setup (offer templates, onboarding plans)

**Formatting Guidelines:**

- Use emojis to make sections visually distinct
- Use bullet points and numbered lists for clarity
- Include visual separators (━━━) between major sections
- Keep language professional and objective
- Be specific and actionable in all recommendations
- Balance honesty about gaps with recognition of potential

#### Important Notes

- **Always provide detailed analysis**: Don't just list candidates with scores. Hiring managers need actionable insights.
- **Be objective about gaps**: Help identify areas where candidates might need support or training.
- **Consider total value**: Match score is just one factor; potential, cultural fit, and long-term growth matter too.
- **Prioritize actionability**: Every analysis should lead to clear hiring decisions and interview strategies.
- **Personalize recommendations**: Reference specific details from the job requirements in your analysis.
- **Think long-term**: Consider not just immediate fit, but retention and growth potential.

---

## API Configuration

Default API endpoint: `https://api.jobclaw.ai`

To use a different endpoint, modify the `apiUrl` parameter when calling the script.

## Error Handling

If any operation fails:

- Check if the API server is running
- Verify all required fields are provided
- Ensure the API endpoint is correct
- For update/delete/matches: ensure a valid **jobId** is provided
- Review the error message and guide the user accordingly

## Resources

### scripts/publish_job.py

Python script supporting four actions (`publish`, `update`, `delete`, `matches`):

- Creating new recruiter accounts (auto-created on publish)
- Publishing and updating job postings
- Soft-deleting job postings (mark INACTIVE)
- Listing AI-matched candidates

The script uses Python's built-in `urllib` library (no external dependencies required).
