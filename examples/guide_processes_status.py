import argparse
import requests
import sys
from pathlib import Path

home_dir = Path.home()

def parse_args(args):
  """
  parses command line arguments

  Args:
    args (list): list of arguments
  Returns:
    dict: a map of arguments as defined by the parser
  """
  parser = argparse.ArgumentParser(
    description="Example of retrieving Protect process info via Koshee Protect REST API",
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

print(f"Logging into {options.url} with username={options.username}")

response = requests.post(f"{options.url}/token", data=data)
token = None
headers = None

login_json = response.json()

print(f"/token: Status Code: {response.status_code}")
print(f"/token: Response Body: {login_json}")

################################################################
# Step 2: get running process information (if any)
################################################################

if response.status_code == 200:
  token = login_json.get("access_token")
  headers = {
    "Authorization": f"Bearer {token}"
  }

  params = {
  }

  print(f"\nRetrieving running Protect process information")

  process_status = requests.get(f"{options.url}/processes/running",
    headers=headers, params=params)

  status_json = process_status.json()
  print(f"/detect: Status Code: {process_status.status_code}")
  print(f"/detect: Response Body: {status_json}")
