import argparse
import requests
import sys

def parse_args(args):
  """
  parses command line arguments

  Args:
    args (list): list of arguments
  Returns:
    dict: a map of arguments as defined by the parser
  """
  parser = argparse.ArgumentParser(
    description="Example of authenticating with Koshee Protect REST API",
    add_help=True
  )
  parser.add_argument('--url', action='store',
    dest='url', help='the base url with port',
    default="http://127.0.0.1:8000")
  parser.add_argument('-u', '--username', action='store',
    dest='username', help='the username for login',
    default="guides@koshee.ai")
  parser.add_argument('-p', '--password', action='store',
    dest='password', help='the password for login',
    default="secret")

  return parser.parse_args(args)

options = parse_args(sys.argv[1:])

################################################################
# Step 1: authenticate the user and password into an OATH2 token
################################################################

data = {
  "grant_type": "password",
  "username": options.username,
  "password": options.password,
}

print(f"Attempting to login to {options.url} with username={options.username}")

response = requests.post(f"{options.url}/token", data=data)
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

  me_response = requests.get(f"{options.url}/users/me", headers=headers, data=data)

  me_json = me_response.json()
  print(f"/users/me: Status Code: {me_response.status_code}")
  print(f"/users/me: Response Body: {me_json}")
