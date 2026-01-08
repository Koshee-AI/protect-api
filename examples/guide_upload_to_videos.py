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
    description="Example of uploading a video to the user's Videos directory via Koshee Protect REST API",
    add_help=True
  )
  parser.add_argument('--url', action='store',
    dest='url', help='the base url with port',
    default="http://127.0.0.1:8000")
  parser.add_argument('-f', '--filename', '--target-filename', action='store',
    dest='filename', help='a new name for the file on the server, if needed')
  parser.add_argument('-v', '--video', action='store',
    dest='video', help='the video to detect')
  parser.add_argument('-d', '--target-dir', action='store',
    dest='target_dir', help='a directory to place the video in within Videos, if needed')
  parser.add_argument('-u', '--username', action='store',
    dest='username', help='the username for login',
    default="guides@koshee.ai")
  parser.add_argument('-p', '--password', action='store',
    dest='password', help='the password for login',
    default="secret")

  return parser.parse_args(args)

options = parse_args(sys.argv[1:])

if options.video is None:
  print(f"To run this example, you must provide an video with -v or --video")
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
# Step 2: upload the video to Videos
##################################################################

if response.status_code == 200:
  token = login_json.get("access_token")
  headers = {
    "Authorization": f"Bearer {token}"
  }

  params = {}

  if options.filename is not None:
    params["target_filename"] = options.filename
  if options.target_dir is not None:
    params["target_dir"] = options.target_dir

  files = {
    "file": open(options.video, "rb")
  }

  print(f"\nUploading video to Videos")

  detect_response = requests.post(f"{options.url}/videos/upload",
    headers=headers, params=params, files=files)

  detect_json = detect_response.json()
  print(f"/detect: Status Code: {detect_response.status_code}")
  print(f"/detect: Response Body: {detect_json}")

