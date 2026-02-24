from curl_cffi import requests
import json

def probe_detail(post_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.khmer24.com/",
        "Origin": "https://www.khmer24.com",
        "Display-Type": "desktop",
        "Accept": "application/json, text/plain, */*",
    }
    
    # Try different patterns
    patterns = [
        f"https://api-posts.khmer24.com/post/{post_id}",
        f"https://api-posts.khmer24.com/posts/{post_id}",
        f"https://api-posts.khmer24.com/post-detail?id={post_id}",
        f"https://api-posts.khmer24.com/feed/{post_id}",
        f"https://api.khmer24.com/post/{post_id}",
        f"https://api-posts.khmer24.com/get-post?id={post_id}"
    ]
    
    for url in patterns:
        print(f"Probing: {url}")
        try:
            response = requests.get(url, headers=headers, impersonate="chrome110", timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("Found match!")
                print(json.dumps(response.json(), indent=2)[:1000])
                return url
        except Exception as e:
            print(f"Error: {e}")
    return None

if __name__ == "__main__":
    probe_detail("12903262")
