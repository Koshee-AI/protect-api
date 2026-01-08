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
    description="Example of authenticating with Koshee Protect REST API",
    add_help=True
  )
  parser.add_argument('--url', action='store',
    dest='url', help='the base url with port',
    default="http://127.0.0.1:8000")
  parser.add_argument('--cf', '--config', action='store',
    dest='config', help='the replay config to reference',
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
# Step 2: retrieve replay output configs
################################################################

if response.status_code == 200:
  token = login_json.get("access_token")
  headers = {
    "Authorization": f"Bearer {token}"
  }

  data = {}

  print(f"\nRetrieving replay list")

  replays_response = requests.get(f"{options.url}/replays", headers=headers, data=data)

  replays_json = replays_response.json()
  print(f"/replays: Status Code: {replays_response.status_code}")
  print(f"/replays: Response Body: {replays_json}")

  ########################################################################
  # Step 3: Retrieve dates and camera names within sample_tracking replay
  ########################################################################

  if replays_response.status_code == 200:

    config_name = options.config

    if config_name in replays_json:

      data = {}

      print(f"\nRetrieving sample_tracking replay dates")
      dates_response = requests.get(f"{options.url}/replays/{config_name}/dates",
        headers=headers, data=data)
      
      print(f"Retrieving sample_tracking replay cameras")
      cameras_response = requests.get(f"{options.url}/replays/{config_name}/cameras",
        headers=headers, data=data)
      
      if dates_response.status_code == 200:
        dates = dates_response.json()
        cameras = cameras_response.json()

        print(f"/replays/{config_name}/dates: {dates}")
        print(f"/replays/{config_name}/cameras: {cameras}")
  
        ########################################################################
        # Step 5: Retrieve metadata for first date in list
        ########################################################################

        if len(dates) > 0:
          date = dates[0]
          print(f"\nSelecting replay date {date}")
          print(f"\nRetrieving metadata for all cameras on {date}")

          # build a simple database to hold metadata files for config/date/camera
          metadata_lookup = {
            config_name : {
              date : {

              }
            }
          }

          # iterate through cameras and get metadata for each combination
          for camera in cameras:
            metadata_response = requests.get(
              f"{options.url}/replays/{config_name}/{camera}/{date}/metadata",
              headers=headers, data=data)

            filename = f"{options.output}/{config_name}_{camera}_{date}.zip"
            print(f"  Downloading {filename}")
            with open(filename, "wb") as zipfile:
              zipfile.write(metadata_response.content)





