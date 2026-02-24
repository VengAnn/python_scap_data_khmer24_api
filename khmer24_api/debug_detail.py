from curl_cffi import requests
import json

def get_full_detail(post_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.khmer24.com/",
        "Origin": "https://www.khmer24.com",
        "Display-Type": "desktop",
    }
    url = f"https://api-posts.khmer24.com/feed/{post_id}"
    response = requests.get(url, headers=headers, impersonate="chrome110")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}")

if __name__ == "__main__":
    get_full_detail("12903262")
