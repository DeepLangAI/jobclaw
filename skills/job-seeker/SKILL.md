---
name: job-seeker
description: Help job seekers submit resumes to the job matching system. Use when users want to: (1) apply for jobs, (2) submit their resume, (3) find job opportunities, (4) look for positions, (5) search for work, or (6) express interest in job hunting. Supports flexible information collection - users can provide all details at once or be guided through step-by-step. Automatically creates user account, generates resume vectors, and triggers AI-powered job matching.
---

# Job Seeker

Submit resumes to the AI-powered job matching system and get matched with relevant positions.

## Overview

This skill helps job seekers submit their resumes through an interactive conversation. Provide information flexibly - share everything at once or answer questions step-by-step. The system will:

1. Collect all required resume information
2. Create a job seeker account automatically
3. Generate AI embeddings from the resume
4. Match with relevant job postings
5. Return matching results with similarity scores

## Workflow

### Step 1: Gather Resume Information

Collect the following required fields. Users can provide them in any order or all at once:

**Required fields:**

- **Resume text**: Detailed work experience, skills, education, and achievements
- **Name**: Full name
- **Email**: Contact email address
- **Phone**: Contact phone number
- **Job intention**: Desired position or role

**Example user inputs:**

_All at once:_

> "I want to apply for jobs. My name is Zhang Wei, email zhangwei@example.com, phone 13800138000. I'm a senior Python backend engineer with 4 years of experience. Proficient in Python, Django, Flask, RESTful API development. Familiar with MySQL, Redis, PostgreSQL. Worked on e-commerce payment and order systems. Looking for Python backend engineer positions."

_Step by step:_

> "Help me find a job"
> [Claude asks for resume]
> "I'm a Python developer with 4 years experience..."
> [Claude asks for name, email, phone, job intention]

### Step 2: Validate Completeness

Before submission, verify all required fields are present. If any are missing, ask the user to provide them:

- Missing resume text: "Please provide your resume content including work experience, skills, and education."
- Missing name: "What's your full name?"
- Missing email: "What's your email address?"
- Missing phone: "What's your phone number?"
- Missing job intention: "What type of position are you looking for?"

### Step 3: Submit Resume

Use the `scripts/submit_resume.py` script to submit the resume:

```bash
python3 scripts/submit_resume.py '{
  "resumeText": "<resume content>",
  "name": "<full name>",
  "email": "<email>",
  "phone": "<phone>",
  "jobIntention": "<desired position>"
}'
```

The script will:

- Create a new job seeker account automatically
- Submit the resume with all information
- Return the authentication token and submission result

### Step 4: Confirm Success

After successful submission, inform the user:

- Confirm the resume was submitted successfully
- Explain that AI matching is in progress (takes ~10 seconds)
- Mention they will receive job matches based on their resume
- Provide the authentication token for future reference (optional)

**Example response:**

> "Your resume has been submitted successfully! The AI matching system is analyzing your profile and will find relevant job opportunities. This typically takes about 10 seconds. You'll receive matches with similarity scores showing how well each position fits your background."

## Error Handling

If submission fails:

- Check if the API server is running
- Verify all required fields are provided
- Ensure the API endpoint is correct
- Review the error message and guide the user accordingly

## Resources

### scripts/submit_resume.py

Python script that handles:

- Creating new job seeker accounts
- Submitting resume data to the API
- Returning authentication tokens and results

The script uses Python's built-in `urllib` library (no external dependencies required).
