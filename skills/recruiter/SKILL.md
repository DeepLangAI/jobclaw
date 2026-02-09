---
name: recruiter
description: Help recruiters publish job postings to the job matching system. Use when users want to: (1) post a job, (2) publish a position, (3) hire someone, (4) recruit candidates, (5) find employees, or (6) advertise job openings. Supports flexible information collection - users can provide all details at once or be guided through step-by-step. Automatically creates recruiter account, generates job vectors, and enables AI-powered candidate matching.
---

# Recruiter

Publish job postings to the AI-powered job matching system and get matched with qualified candidates.

## Overview

This skill helps recruiters publish job postings through an interactive conversation. Provide information flexibly - share everything at once or answer questions step-by-step. The system will:

1. Collect all required job posting information
2. Create a recruiter account automatically
3. Generate AI embeddings from the job description
4. Match with qualified job seekers
5. Return matching candidates with similarity scores

## Workflow

### Step 1: Gather Job Posting Information

Collect the following required fields. Users can provide them in any order or all at once:

**Required fields:**
- **Job title**: Position name (e.g., "Senior Python Backend Engineer")
- **Company name**: Employer name
- **Job requirements**: Detailed requirements including skills, responsibilities, and qualifications
- **Salary range**: Compensation range (e.g., "25k-40k", "30k-50k")
- **Work location**: Office location (e.g., "Shanghai·Changning District", "Beijing·Chaoyang District")
- **Job type**: Employment type (e.g., "Full-time", "Part-time", "Contract")
- **Education requirement**: Minimum education level (e.g., "Bachelor's degree or above", "Master's degree preferred")
- **Experience requirement**: Required years of experience (e.g., "3-5 years", "5+ years")

**Example user inputs:**

*All at once:*
> "I want to post a job for a Python Backend Engineer at Pinduoduo in Shanghai Changning District. Salary 25k-40k. Requirements: Familiar with Python, Django/Flask frameworks, RESTful API development experience. Knowledge of MySQL, Redis databases. E-commerce or payment system experience preferred. Full-time position, bachelor's degree or above, 3-5 years experience."

*Step by step:*
> "I need to hire a developer"
> [Claude asks for job title]
> "Python Backend Engineer"
> [Claude asks for company, requirements, salary, location, etc.]

### Step 2: Validate Completeness

Before submission, verify all required fields are present. If any are missing, ask the user to provide them:

- Missing title: "What's the job title for this position?"
- Missing company: "What's the company name?"
- Missing requirements: "Please describe the job requirements, including required skills and responsibilities."
- Missing salary: "What's the salary range for this position?"
- Missing location: "Where is the work location?"
- Missing job type: "What's the employment type? (e.g., Full-time, Part-time, Contract)"
- Missing education: "What's the minimum education requirement?"
- Missing experience: "How many years of experience are required?"

### Step 3: Publish Job Posting

Use the `scripts/publish_job.py` script to publish the job:

```bash
python3 scripts/publish_job.py '{
  "apiUrl": "https://www.jobclaw.ai",
  "title": "<job title>",
  "companyName": "<company name>",
  "requirement": "<detailed requirements>",
  "salary": "<salary range>",
  "location": "<work location>",
  "jobType": "<employment type>",
  "education": "<education requirement>",
  "experience": "<experience requirement>",
  "status": "ACTIVE"
}'
```

The script will:
- Create a new recruiter account automatically
- Publish the job posting with all information
- Return the authentication token and job ID

### Step 4: Confirm Success

After successful publication, inform the user:

- Confirm the job was published successfully
- Provide the job ID for reference
- Explain that AI matching is in progress (takes ~5 seconds)
- Mention they will receive candidate matches based on the job requirements
- Provide the authentication token for future reference (optional)

**Example response:**
> "Your job posting has been published successfully! Job ID: 7. The AI matching system is analyzing your requirements and will find qualified candidates. This typically takes about 5 seconds. You'll receive candidate matches with similarity scores showing how well each applicant fits your requirements."

## API Configuration

Default API endpoint: `https://www.jobclaw.ai`

To use a different endpoint, modify the `apiUrl` parameter when calling the script.

## Error Handling

If publication fails:
- Check if the API server is running
- Verify all required fields are provided
- Ensure the API endpoint is correct
- Review the error message and guide the user accordingly

## Resources

### scripts/publish_job.py

Python script that handles:
- Creating new recruiter accounts
- Publishing job postings to the API
- Returning authentication tokens and job IDs

The script uses Python's built-in `urllib` library (no external dependencies required).
