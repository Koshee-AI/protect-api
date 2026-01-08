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
    description="Example of running Detect on single image via Koshee Protect REST API",
    add_help=True
  )
  parser.add_argument('--url', action='store',
    dest='url', help='the base url with port',
    default="http://127.0.0.1:8000")
  parser.add_argument('-d', '--detector', action='store',
    dest='detector', help='the detector config name to use',
    default="detect_person")
  parser.add_argument('-i', '--image', action='store',
    dest='image', help='the image to detect')
  parser.add_argument('-u', '--username', action='store',
    dest='username', help='the username for login',
    default="guides@koshee.ai")
  parser.add_argument('-p', '--password', action='store',
    dest='password', help='the password for login',
    default="secret")

  return parser.parse_args(args)

options = parse_args(sys.argv[1:])

if options.image is None:
  print(f"To run this example, you must provide an image with -i or --image")
  parse_args(["-h"])

################################################################
# Step 1: authenticate the user and password into an OATH2 token
################################################################

params = {
  "grant_type": "password",
  "username": options.username,
  "password": options.password,
}

print(f"Logging into {options.url} with username={options.username}")

response = requests.post(f"{options.url}/token", data=params)
token = None
headers = None

login_json = response.json()

print(f"/token: Status Code: {response.status_code}")
print(f"/token: Response Body: {login_json}")

##################################################################
# Step 2: run detect with the provided image and detector options
##################################################################

if response.status_code == 200:
  token = login_json.get("access_token")
  headers = {
    "Authorization": f"Bearer {token}"
  }

  params = {
    "detector": options.detector,
  }

  files = {
    "file": open(options.image, "rb")
  }

  print(f"\nRunning detector {options.detector} on {options.image}")

  detect_response = requests.post(f"{options.url}/detect/image",
    headers=headers, params=params, files=files)

  detect_json = detect_response.json()
  print(f"/detect: Status Code: {detect_response.status_code}")
  print(f"/detect: Response Body: {detect_json}")
