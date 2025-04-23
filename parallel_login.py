import requests
import json
from concurrent.futures import ThreadPoolExecutor

url = "https://freshsession.myfreshworks.dev/api/v2/login"

csrf_token = "78111ed1-d191-4430-92b3-0c22257a9ba3.KswneRRcqHna/O+TU4WGr0ALKWRPxS9fF3SBOdQBX1I="

headers = {
    "x-xsrf-token": csrf_token,
    "content-type": "application/json"
}

cookies = {"XSRF-TOKEN": csrf_token}


def send_login_request(email, attempt_num):
    payload = {
        "username": email,
        "password": "password"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, cookies=cookies, timeout=10)
        print(f"Authenticated {email} ({attempt_num}): Status {response.status_code}")
    except Exception as e:
        print(response.json())
        print(f"Error for {email} ({attempt_num}): {e}")


# Create list of tasks
tasks = []
for num in range(1000,1100):
    email = f"kavyashree.arun1+{num}@freshworks.com"
    for attempt in range(25):
        tasks.append((email, attempt))

# Run in parallel using threads
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(lambda p: send_login_request(*p), tasks)
