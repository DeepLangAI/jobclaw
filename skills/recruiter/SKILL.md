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
4. **List matched candidates** - View candidates matched by the AI system with similarity scores

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

*All at once:*
> "I want to post a job for a Python Backend Engineer at Pinduoduo in Shanghai Changning District. Salary 25k-40k. Requirements: Familiar with Python, Django/Flask frameworks, RESTful API development experience. Knowledge of MySQL, Redis databases. E-commerce or payment system experience preferred. Full-time position, bachelor's degree or above, 3-5 years experience."

*Step by step:*
> "I need to hire a developer"
> [Claude asks for job title]
> "Python Backend Engineer"
> [Claude asks for company, requirements, salary, location, etc.]

#### Step 2: Validate Completeness

Before submission, verify all required fields are present. If any are missing, ask the user to provide them.

#### Step 3: Publish Job Posting

```bash
python3 scripts/publish_job.py '{
  "apiUrl": "http://localhost:8989",
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
}'
```

#### Step 4: Confirm Success

After successful publication, inform the user and **save the returned token and job ID** for future operations (update, delete, list matches).

---

### Update Job (action: update)

Requires the **token** and **jobId** from a previous publish. Only changed fields need to be provided.

```bash
python3 scripts/publish_job.py '{
  "apiUrl": "http://localhost:8989",
  "action": "update",
  "token": "<saved token>",
  "jobId": "<job id>",
  "salary": "<new salary range>",
  "requirement": "<updated requirements>"
}'
```

Updatable fields: `title`, `companyName`, `requirement`, `salary`, `location`, `jobType`, `education`, `experience`, `status`.

---

### Delete Job (action: delete)

Soft-deletes the job posting by marking it as INACTIVE. Match history is preserved.

```bash
python3 scripts/publish_job.py '{
  "apiUrl": "http://localhost:8989",
  "action": "delete",
  "token": "<saved token>",
  "jobId": "<job id>"
}'
```

---

### List Matched Candidates (action: matches)

Retrieve candidates matched by the AI system for a specific job posting.

```bash
python3 scripts/publish_job.py '{
  "apiUrl": "http://localhost:8989",
  "action": "matches",
  "token": "<saved token>",
  "jobId": "<job id>"
}'
```

Returns a list of matched candidates with similarity scores.

---

## API Configuration

Default API endpoint: `http://localhost:8989`

To use a different endpoint, modify the `apiUrl` parameter when calling the script.

## Error Handling

If any operation fails:
- Check if the API server is running
- Verify all required fields are provided
- Ensure the API endpoint is correct
- For update/delete/matches: ensure a valid **token** and **jobId** are provided
- Review the error message and guide the user accordingly

## Resources

### scripts/publish_job.py

Python script supporting four actions (`publish`, `update`, `delete`, `matches`):
- Creating new recruiter accounts (auto-created on publish)
- Publishing and updating job postings
- Soft-deleting job postings (mark INACTIVE)
- Listing AI-matched candidates

The script uses Python's built-in `urllib` library (no external dependencies required).
