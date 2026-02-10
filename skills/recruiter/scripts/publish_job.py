#!/usr/bin/env python3
"""
Publish job posting to the job matching API.
"""
import sys
import json
import urllib.request
import urllib.error

def publish_job(job_data):
    """
    Publish a job posting to the API.

    Args:
        job_data: Dictionary containing:
            - token: Authentication token (optional, will create new user if not provided)
            - title: Job title (required)
            - companyName: Company name (required)
            - requirement: Job requirements (required)
            - salary: Salary range (required)
            - location: Work location (required)
            - jobType: Employment type (required)
            - education: Education requirement (required)
            - experience: Experience requirement (required)
            - status: Job status (optional, defaults to "ACTIVE")

    Returns:
        Dictionary with API response
    """
    # Create new user if no token provided
    api_url = "https://api.jobclaw.ai"
    token = job_data.get('token')
    if not token:
        create_url = f"{api_url}/auth/token"
        create_data = json.dumps({"userType": "RECRUITER"}).encode('utf-8')
        create_req = urllib.request.Request(
            create_url,
            data=create_data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )

        try:
            with urllib.request.urlopen(create_req) as response:
                result = json.loads(response.read().decode('utf-8'))
                token = result['result']['token']
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return {'success': False, 'error': f'Failed to create user (Status {e.code}): {error_body}'}

    # Publish job
    publish_url = f"{api_url}/jobs"
    publish_data = json.dumps({
        'title': job_data['title'],
        'companyName': job_data['companyName'],
        'requirement': job_data['requirement'],
        'salary': job_data['salary'],
        'location': job_data['location'],
        'jobType': job_data['jobType'],
        'education': job_data['education'],
        'experience': job_data['experience'],
        'status': job_data.get('status', 'ACTIVE')
    }).encode('utf-8')

    publish_req = urllib.request.Request(
        publish_url,
        data=publish_data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )

    try:
        with urllib.request.urlopen(publish_req) as response:
            result = json.loads(response.read().decode('utf-8'))
            result['token'] = token
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {'success': False, 'error': f'Failed to publish job (Status {e.code}): {error_body}'}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': 'Usage: publish_job.py <json_data>'}))
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
        result = publish_job(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))
        sys.exit(1)
