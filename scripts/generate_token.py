#!/usr/bin/env python 
import os
import time 
import jwt 
import requests
def main():
  # Retrieve GitHub App credentials from environment variables 
  APP_ID = os.environ.get("GH_APPLICATION_ID") 
  INSTALLATION_ID = os.environ.get("GH_APPLICATION_INSTALLATION_ID") 
  PRIVATE_KEY = os.environ.get("GH_APP_PRIVATE_KEY") 
  if not (APP_ID and INSTALLATION_ID and PRIVATE_KEY): 
      print("Error: Missing one or more required environment variables (GH_APPLICATION_ID, GH_APPLICATION_INSTALLATION_ID, GH_APP_PRIVATE_KEY)") 
      exit(1) 
  # Create a JWT for authentication with GitHub App API 
  now = int(time.time()) 
  payload = { 
      "iat": now - 60, 
      "exp": now + (10 * 60), 
      "iss": APP_ID 
  } 
  jwt_token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256") 
  # Request an installation access token using the JWT 
  url = f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens" 
  headers = { 
      "Authorization": f"Bearer {jwt_token}", 
      "Accept": "application/vnd.github+json" 
  } 
  response = requests.post(url, headers=headers) 
  if response.status_code == 201: 
      github_app_token = response.json()["token"] 
      with open(os.environ["GITHUB_OUTPUT"], "a") as f: 
          f.write(f"github_app_token={github_app_token}\n") 
  else: 
      print("Error retrieving token:", response.status_code, response.text) 
      exit(1) 


if __name__ == "__main__": 
    main()