import argparse
import json
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
  parser.add_argument('-o', '--output', action='store',
    dest='output', help='a file to save to',
    default="openapi.json")

  return parser.parse_args(args)

options = parse_args(sys.argv[1:])

################################################################
# Step 1: Get the current openapi json that defines all routes
################################################################

print(f"Grabbing openjson from {options.url}")

response = requests.get(f"{options.url}/openapi.json")
token = None
headers = None

openapi_json = response.json()

if response.status_code == 200:
  try:
    with open(options.output, 'w') as json_file:
      json.dump(openapi_json, json_file, indent=2)
    print(f"Data successfully saved to {options.output}")
  except IOError as e:
    print(f"Error saving file: {e}")
