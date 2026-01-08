# Project Summary

An OpenAPI REST API definition for interacting with a Koshee Protect server

## Hello World with Authentication

The following shows a [python requests example](https://github.com/Koshee-AI/protect-api/blob/main/examples/guide_auth.py):

```

import requests

################################################################
# Step 1: authenticate the user and password into OATH2 token
################################################################

url = "http://127.0.0.1:80000"
username = "guides@koshee.ai"
password = "secret"

data = {
  "grant_type": "password",
  "username": username,
  "password": password,
}

print(f"Attempting to login to {url} with username={username}")

response = requests.post(f"{url}/token", data=data)
token = None
headers = None

login_json = response.json()

print(f"/token: Status Code: {response.status_code}")
print(f"/token: Response Body: {login_json}")

################################################################
# Step 2: make a query with your new OATH2 token
################################################################

if response.status_code == 200:
  token = login_json.get("access_token")
  headers = {
    "Authorization": f"Bearer {token}"
  }

  data = {}

  print(f"\nAttempting to get authenticated user db entry")

  me_response = requests.get(f"{url}/users/me", headers=headers, data=data)

  me_json = me_response.json()
  print(f"/users/me: Status Code: {me_response.status_code}")
  print(f"/users/me: Response Body: {me_json}")
```


## Other Guides

We provide guides on using the Koshee Protect API in the
[examples folder](https://github.com/Koshee-AI/protect-api/blob/main/examples)

- [Replay Guide](https://github.com/Koshee-AI/protect-api/blob/main/examples/guide_replay.py)
