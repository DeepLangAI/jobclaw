#!/usr/bin/env python3
"""
Submit job seeker resume to the job matching API.
"""
import sys
import json
import urllib.request
import urllib.error

def submit_resume(api_url, resume_data):
    """
    Submit resume to the API.

    Args:
        api_url: Base URL of the API (e.g., https://api.jobclaw.ai)
        resume_data: Dictionary containing:
            - token: Authentication token (optional, will create new user if not provided)
            - resumeText: Resume content (required)
            - name: Full name (required)
            - email: Email address (required)
            - phone: Phone number (required)
            - jobIntention: Desired job position (required)

    Returns:
        Dictionary with API response
    """
    # Create new user if no token provided
    token = resume_data.get('token')
    if not token:
        create_url = f"{api_url}/auth/token"
        create_data = json.dumps({"userType": "JOB_SEEKER"}).encode('utf-8')
        create_req = urllib.request.Request(
            create_url,
            data=create_data,
            headers={'Content-Type': 'application/json'}
        )

        try:
            with urllib.request.urlopen(create_req) as response:
                result = json.loads(response.read().decode('utf-8'))
                token = result['result']['token']
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return {'success': False, 'error': f'Failed to create user: {error_body}'}

    # Submit resume
    submit_url = f"{api_url}/job-seekers/resume"
    submit_data = json.dumps({
        'resumeText': resume_data['resumeText'],
        'name': resume_data['name'],
        'email': resume_data['email'],
        'phone': resume_data['phone'],
        'jobIntention': resume_data['jobIntention']
    }).encode('utf-8')

    submit_req = urllib.request.Request(
        submit_url,
        data=submit_data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )

    try:
        with urllib.request.urlopen(submit_req) as response:
            result = json.loads(response.read().decode('utf-8'))
            result['token'] = token
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {'success': False, 'error': f'Failed to submit resume: {error_body}'}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': 'Usage: submit_resume.py <json_data>'}))
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
        api_url = data.get('apiUrl', 'https://api.jobclaw.ai')
        result = submit_resume(api_url, data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))
        sys.exit(1)
