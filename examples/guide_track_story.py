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
    description="Example of pulling track story via Koshee Protect REST API",
    add_help=True
  )
  parser.add_argument('--url', action='store',
    dest='url', help='the base url with port',
    default="http://127.0.0.1:8000")
  parser.add_argument('--cf', '--config', action='store',
    dest='config', help='the track config to reference',
    default="sample_tracking")
  parser.add_argument('-u', '--username', action='store',
    dest='username', help='the username for login',
    default="guides@koshee.ai")
  parser.add_argument('-p', '--password', action='store',
    dest='password', help='the password for login',
    default="secret")
  parser.add_argument('-o', '--output-dir', action='store',
    dest='output', help='output directory for zip files',
    default=f"{home_dir}/Downloads")
  parser.add_argument('-t', '--track-id', action='store',
    dest='track_id', help='the track id within the track config',
    default="poi_1")

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
# Step 2: retrieve track output configs
################################################################

if response.status_code == 200:
  token = login_json.get("access_token")
  headers = {
    "Authorization": f"Bearer {token}"
  }

  data = {}

  print(f"\nRetrieving track output list")

  tracks_response = requests.get(f"{options.url}/tracks",
    headers=headers, data=data)

  tracks_json = tracks_response.json()
  print(f"/tracks: Status Code: {tracks_response.status_code}")
  print(f"/tracks: Response Body: {tracks_json}")

  ########################################################################
  # Step 3: Retrieve dates and camera names within sample_tracking replay
  ########################################################################

  if tracks_response.status_code == 200:

    config_name = options.config

    if config_name in tracks_json:

      data = {}

      print(f"\nRetrieving {config_name} {options.track_id} story")
      track_story_response = requests.get(
        f"{options.url}/tracks/{config_name}/{options.track_id}/story",
        headers=headers, data=data)
      
      filename = f"{options.output}/track_{config_name}_{options.track_id}.zip"
      print(f"  Downloading {filename}")
      with open(filename, "wb") as zipfile:
        zipfile.write(track_story_response.content)
