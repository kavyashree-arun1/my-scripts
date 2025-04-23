import requests

ORG_URL = "https://freshsession.myfreshworks.dev"
CREATE_USER_ENDPOINT = "/api/v2/users"
ACTIVATION_LINK_SUFFIX = "/hashes/activation"
ACTIVATE_USER_TEMPLATE = "/api/v2/users/-/hashes/{hash_code}/activate"

CSRF_TOKEN = "78111ed1-d191-4430-92b3-0c22257a9ba3.KswneRRcqHna/O+TU4WGr0ALKWRPxS9fF3SBOdQBX1I="
ORG_TOKEN = "Bearer eyJraWQiOiI5MjU5NTcxMDIwNTk3MjY0MCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJhdWQiOiI4MzIwOTE1NjgxNzc2MDUwMzkiLCJzdWIiOiI4MzIwOTE2MTU3NzE5NDM2ODkiLCJvcmdhbmlzYXRpb25faWQiOiI4MzIwOTE2MDA1MjQ3MDk5MzYiLCJzY29wZSI6WyJST0xFX0NMSUVOVCIsIlJPTEVfVU5MT0NLX1VTRVIiLCJST0xFX1VQREFURV9QUk9GSUxFIiwiUk9MRV9IRUlNREFMTCJdLCJwcm9kdWN0X2lkIjoiODMyMDkxNTUzNDk1NzE0OTM0IiwiaXNzIjoiaHR0cHM6Ly9mcmVzaHNlc3Npb24ubXlmcmVzaHdvcmtzLmRldiIsIm9yZ2FuaXNhdGlvbl9kb21haW4iOiJmcmVzaHNlc3Npb24ubXlmcmVzaHdvcmtzLmRldiIsImV4cCI6Mjc0NDY4NjkwMCwiaWF0IjoxNzQ0Njg2OTAwLCJqdGkiOiI4MzIwOTE2MTU3NzE5NDM2OTAifQ.Q-Y3KNxl2E0QV8fS8mbY8zgsK6qSP0MffIuEb9muvPDLYKHNLL3jepwYfjQ_QbjkuxQkenhkD66hrIRjhLGNTdLkVE0L8M33aUby9YrXSMhvjsxSju7FPlyI9M3Z0Par8szHvJs2qQELO712Cz-cw-tU3CNuKBELrbVTtzR1sHQLExz1oO94OP5Xkm9BQlaO7D4yFWZ8TsKC_Y2vhM8lYRaoHlSf0UuBdy5KqP8fl3B8oIFCcPdtAaCdiw2W282j7HO-Fd09d47anXzLrAhkz3QUjMRAvNRa1PaEVWdVYQ7umEjWnxgwkHAB6hxmRqLeIuMHoHnP5hvbuAELaSu3ZA"

HEADERS = {
    "authorization": ORG_TOKEN,
    "x-xsrf-token": CSRF_TOKEN,
    "content-type": "application/json"
}
COOKIES = {"XSRF-TOKEN": CSRF_TOKEN}


def create_user(email: str):
    payload = {
        "user": {
            "first_name": "Kavyashree",
            "last_name": "Arun",
            "email": email,
            "password": "password",
            "state": "ACTIVATED"
        }
    }
    response = requests.post(ORG_URL + CREATE_USER_ENDPOINT, json=payload, headers=HEADERS, cookies=COOKIES)
    return response.json()


def create_activation_link(user_id: str):
    url = f"{ORG_URL}{CREATE_USER_ENDPOINT}/{user_id}{ACTIVATION_LINK_SUFFIX}"
    payload = {"redirect_uri": "https://support-51326.vahlok.freshworksapi.io/"}
    response = requests.post(url, json=payload, headers=HEADERS, cookies=COOKIES)
    return response.json()


def activate_user(hash_code: str):
    url = ORG_URL + ACTIVATE_USER_TEMPLATE.format(hash_code=hash_code)
    payload = {
        "password": "password",
        "first_name": "Kavyashree",
        "last_name": "Arun"
    }
    response = requests.patch(url, json=payload, headers=HEADERS, cookies=COOKIES)
    return response.json()


# Loop through user creation
for number in range(1, 10000):
    email = f"kavyashree.arun1+{number}@freshworks.com"
    print(f"\n➡️ Creating user: {email}")

    user_response = create_user(email)

    user_id = user_response.get("id")
    if not user_id:
        print("Failed to create user:", user_response)
        continue

    print("User created with ID:", user_id)

    activation_response = create_activation_link(user_id)
    hash_code = activation_response.get("hash_code")

    if not hash_code:
        print("Failed to get activation hash:", activation_response)
        continue

    print("Activation hash generated:", hash_code)

    activation_result = activate_user(hash_code)
    print("Activation response:", activation_result)
