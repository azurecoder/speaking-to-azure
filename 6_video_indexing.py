import yaml 
import argparse
import time
import os

import requests

def get_video_id(location, account_id, access_token):
    base_url = f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos"
    params = {
        'accessToken': access_token,
        'pageSize': 25,
    }

    headers = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': access_token
    }
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            return data["results"][0]["id"]
        else:
            return None
    else:
        print(f"Failed to retrieve videos: {response.status_code}, {response.text}")
        return None
    
def get_video_summary(location, account_id, access_token, video_id, language="en-GB"):
    base_url = f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos/{video_id}/Captions"
    params = {
        'accessToken': access_token,
        'format': 'srt',
        'language': language
    }

    headers = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': access_token
    }
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(f"Failed to retrieve videos: {response.status_code}, {response.text}")
        return None

def load_yaml(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    parser = argparse.ArgumentParser(description="Load region and speech_key from a YAML file.")
    parser.add_argument('config_file', type=str, help="The path to the YAML configuration file.")
    parser.add_argument('--language', type=str, help="The language to convert the video to")
    args = parser.parse_args()

    config = load_yaml(args.config_file)
    region = config['azure']['region']
    video_key = config['azure']['video_key']
    account_id = config['azure']['video_account_id']
    print(f"Region: {region}")
    print(f"Video Key: ****")
    print(f"Video Account ID: ****")
    video_id = get_video_id(region, account_id, video_key)
    language = args.language if args.language else "en-GB"
    if video_id:
        print(f"Video ID: {video_id}")
        summary = get_video_summary(region, account_id, video_key, video_id, language)
        if summary:
            print(summary)
    print("Done!")

if __name__ == '__main__':
    main()
# python3 6_video_indexing.py richard.yaml --language en-ES
