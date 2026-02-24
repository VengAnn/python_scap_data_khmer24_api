import requests
import json
import time

def export_all_khmer24(keyword):
    """
    This script automatically loops through the API until ALL items are downloaded.
    It saves everything to a file called 'khmer24_all_data.json'.
    """
    base_url = "http://localhost:8000/api/search"
    all_items = []
    offset = 0
    limit = 100 # Requesting 100 at a time is safer and more reliable
    
    print(f"Starting export for: {keyword}")
    
    while True:
        try:
            params = {"q": keyword, "limit": limit, "offset": offset}
            response = requests.get(base_url, params=params)
            
            if response.status_code != 200:
                print(f"Error calling API: {response.text}")
                break
                
            data = response.json()
            items = data.get("items", [])
            total = data.get("total", 0)
            
            if not items:
                break
                
            all_items.extend(items)
            print(f"Downloaded: {len(all_items)} / {total}")
            
            # Check if we have everything
            if len(all_items) >= total:
                break
            
            # Increment offset for next page
            offset += len(items)
            
            # small delay to be polite
            time.sleep(0.5) 
            
        except Exception as e:
            print(f"Connection error: {e}")
            break

    # Save to file
    with open("khmer24_all_data.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
        
    print(f"\n✅ DONE!")
    print(f"Total items saved: {len(all_items)}")
    print("File saved as: khmer24_all_data.json")

if __name__ == "__main__":
    export_all_khmer24("Ford")
