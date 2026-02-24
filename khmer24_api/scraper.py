from curl_cffi import requests
import json
import time

class Khmer24Scraper:
    def __init__(self):
        self.api_url = "https://api-posts.khmer24.com/feed"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.khmer24.com/",
            "Origin": "https://www.khmer24.com",
            "Display-Type": "desktop",
            "Accept": "application/json, text/plain, */*",
        }

    def search(self, keyword=None, limit=30, offset=0):
        """
        Search for items on Khmer24. 
        If limit > 30, it will automatically loop through pages to get all data in one go.
        If keyword is None, it fetches the general "All Ads" feed.
        """
        all_items = []
        current_offset = offset
        target_limit = limit
        total_found = 0
        
        # Khmer24 internal max is 30.
        internal_chunk_size = 30 
        
        while len(all_items) < target_limit:
            # Calculate how many to ask for in this specific chunk
            remaining = target_limit - len(all_items)
            chunk_limit = min(internal_chunk_size, remaining)
            
            params = {
                "lang": "en",
                "offset": str(current_offset),
                "limit": str(chunk_limit),
                "fields": "location,category,link,thumbnails"
            }
            if keyword:
                params["keyword"] = keyword

            try:
                response = requests.get(
                    self.api_url, 
                    params=params, 
                    headers=self.headers, 
                    impersonate="chrome110", 
                    timeout=15
                )
                
                if response.status_code == 200:
                    json_data = response.json()
                    raw_items = json_data.get('data', [])
                    
                    # Get total count from the very first response and keep it
                    if current_offset == offset:
                        total_found = json_data.get('total', 0)
                    
                    if not raw_items:
                        break
                        
                    cleaned = self._clean_data(raw_items)
                    all_items.extend(cleaned)
                    
                    # Stop if we reached the end of items actually returned
                    current_offset += len(raw_items)
                    
                    # If the server returned fewer items than requested, we reached the end
                    if len(raw_items) < chunk_limit:
                        break

                    # If we have reached or exceeded the total available on Khmer24
                    if total_found > 0 and current_offset >= total_found:
                        break
                    
                    # Small delay to keep it safe
                    if len(all_items) < target_limit:
                        time.sleep(0.3)
                else:
                    if all_items: break
                    return {"error": f"API Error {response.status_code}", "detail": response.text[:200]}
            except Exception as e:
                if all_items: break
                return {"error": "Scraper Exception", "detail": str(e)}

        return {
            "items": all_items[:target_limit],
            "total": total_found,
            "limit": target_limit,
            "offset": offset,
            "count": len(all_items[:target_limit])
        }

    def get_details(self, item_id):
        """
        Fetch full details for a specific item by its ID.
        """
        url = f"{self.api_url}/{item_id}"
        params = {
            "lang": "en",
            "fields": "user,phone,location,category,thumbnails,photos,description"
        }

        try:
            response = requests.get(url, params=params, headers=self.headers, impersonate="chrome110", timeout=15)
            
            if response.status_code == 200:
                json_data = response.json()
                raw_info = json_data.get('data', {})
                return self._clean_detail_data(raw_info)
            else:
                return {"error": f"API Error {response.status_code}", "detail": response.text[:200]}
        except Exception as e:
            return {"error": "Connection Failed", "detail": str(e)}

    def _clean_detail_data(self, info):
        """
        Cleans and structures the full item detail data.
        """
        # Extract images
        photos = info.get('photos', [])
        
        # User/Seller info
        user_info = info.get('user', {})\
            if isinstance(info.get('user'), dict) else {}
        seller = {
            "name": user_info.get("name"),
            "username": user_info.get("username"),
            "photo": user_info.get("photo", {}).get("url") if isinstance(user_info.get("photo"), dict) else None,
            "registered": user_info.get("registered_date"),
            "verified": user_info.get("is_verify", False)
        }

        # Location with lat/lng
        location_data = info.get("location", {}) or {}
        map_data = location_data.get("map", {}) or {}
        lat = map_data.get("x")   # x = latitude
        lng = map_data.get("y")   # y = longitude
        google_maps = f"https://maps.google.com/maps?q={lat},{lng}" if lat and lng else None

        return {
            "id": info.get("id"),
            "title": info.get("title"),
            "price": info.get("price", "Negotiable"),
            "description": info.get("description", ""),
            "location": location_data.get("long_location"),
            "latitude": lat,
            "longitude": lng,
            "google_maps": google_maps,
            "category": info.get("category", {}).get("en_name") if isinstance(info.get("category"), dict) else None,
            "seller": seller,
            "phone": info.get("phone", []),
            "images": photos,
            "link": info.get("link") or f"https://www.khmer24.com/post-adid-{info.get('id')}"
        }

    def _clean_data(self, raw_items):
        cleaned_results = []
        if not raw_items:
            return []
            
        for item in raw_items:
            # The actual content is nested in 'data'
            info = item.get('data', {})
            
            # Extract image (first thumbnail)
            thumbnails = info.get('thumbnails', [])
            image_url = ""
            if thumbnails and isinstance(thumbnails, list) and len(thumbnails) > 0:
                first_thumb = thumbnails[0]
                if isinstance(first_thumb, dict):
                    image_url = first_thumb.get('url', "")
                else:
                    image_url = str(first_thumb)

            cleaned_item = {
                "id": info.get("id"),
                "title": info.get("title"),
                "price": info.get("price", "Negotiable"),
                "location": info.get("location", {}).get("en_name2") or info.get("location", {}).get("en_name") or "N/A",
                "category": info.get("category", {}).get("en_name", "N/A"),
                "link": info.get("link") or f"https://www.khmer24.com/post-adid-{info.get('id')}",
                "image": image_url,
                "type": info.get("type", "normal")
            }
            cleaned_results.append(cleaned_item)
        return cleaned_results

# Check if running directly 
if __name__ == "__main__":
    scraper = Khmer24Scraper()
    print("start scraper...")
    result = scraper.search("iphone", limit=2)
    print(json.dumps(result, indent=2))
