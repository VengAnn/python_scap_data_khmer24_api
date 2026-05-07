# Khmer24 Data API

A clean, high-performance API wrapper for searching Khmer24 data. This API bypasses Cloudflare security and returns structured JSON data.

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install fastapi uvicorn curl_cffi
```

### 2. Run the API

````bash
source .venv/bin/activate
python3 main.py
```

The server will start at `http://localhost:8000`.

### Why This API?

This API uses **curl_cffi**, a special library that "impersonates" a real Chrome browser at the network level. It tricks Cloudflare into thinking requests are coming from a real person using a real computer.

### How to Use

Keep the Python code running and use **Postman** to call your local API at `http://localhost:8000/api/search`.

---

## 📡 API Endpoints

### **Get All Ads (General Feed)**

Retrieve the latest ads from Khmer24 without any specific keyword search.

- **URL:** `/api/all`
- **Method:** `GET`
- **Query Params:**
  - `offset`: Starting point (increment by 30 for each "page")
  - `limit`: Results per call (default 30)

**Example Request:**

```bash
curl "http://localhost:8000/api/all?limit=50"
````

---

### **Get Item Details**

Retrieve full details (description, phone number, seller info, images) for a specific item.

- **URL:** `/api/item/{item_id}`
- **Method:** `GET`

**Example Request:**

```bash
curl "http://localhost:8000/api/item/12903262"
```

---

### **Search Items (with Scrolling/Pagination)**

To "scroll" and get more data, use the `offset` parameter. By default, each request returns 30 items. To get the next 30, set `offset=30`, then `60`, and so on.

- **URL:** `/api/search`
- **Method:** `GET`
- **Query Params:**
  - `q`: Keyword (e.g. `iphone`)
  - `offset`: Starting point (increment by 30 for each "page")
  - `limit`: Results per call (default 30)

**Example Response:**

```json
{
  "total": 6077,
  "limit": 5,
  "offset": 0,
  "items": [
    {
      "id": "12345678",
      "title": "Toyota Prius 2010 Option 4",
      "price": "14500.00",
      "location": "Phnom Penh",
      "category": "Cars",
      "link": "https://www.khmer24.com/post-12345678",
      "image": "https://images.khmer24.co/..."
    }
  ]
}
```

---

### **🧪 How to Test in Postman**

Since the API handles the Cloudflare bypass internally, you **do not** need to add any special headers in Postman. Just treat it like a normal, local API.

1.  Open Postman.
2.  Click **"New" > "HTTP Request"**.
3.  Set the method to **`GET`**.
4.  Enter the URL: `http://localhost:8000/api/search`
5.  Go to the **"Params"** tab and add:
    - **Key:** `q` | **Value:** `iphone`
    - **Key:** `limit` | **Value:** `5`
    - **Key:** `offset` | **Value:** `0` (Change this to `30`, `60`, etc. to load more pages)
6.  Click **"Send"** to get your JSON data.

**Response Metadata:** The API returns a `total` field showing how many items exist for that keyword, so you know when to stop scrolling.

## 🛠 Features

- **Cloudflare Bypass:** Uses `curl_cffi` to mimic real browser TLS fingerprints.
- **Structured JSON:** Removes unnecessary meta-data and returns only what you need.
- **Auto-Documentation:** Visit `http://localhost:8000/docs` for the interactive Swagger UI.

## ⚠️ Notes

- This API is a proxy for the internal Khmer24 feed.
- Aggressive requests might still result in temporary IP bans. Use responsibly with delays.

## 🚀 Deploy to Vercel (Free)

You can host this API for free on Vercel.

### 1. Prepare for Deployment

Ensure you have the following files in your project folder:

- `main.py`
- `scraper.py`
- `requirements.txt`
- `vercel.json` (I have already created this for you)

### 2. Deploy using Vercel CLI

1.  **Install Vercel CLI**:
    ```bash
    npm install -g vercel
    ```
2.  **Login to Vercel**:
    ```bash
    vercel login
    ```
3.  **Deploy**:
    Run this command inside the `khmer24` folder:
    ```bash
    vercel --prod
    ```

### ⚠️ Important Vercel Limitations:

- **Timeout**: Vercel Free tier has a **10-second timeout**. If you set a very high `limit` (like 1000+), the request might take longer than 10 seconds and Vercel will return a "504 Gateway Timeout" error. For Vercel, it is better to use smaller limits (e.g., 100) and use `offset` to get more data.
- **IP Blocking**: Since Vercel uses shared IP addresses, Cloudflare might sometimes show a captcha. If your deployment gets blocked, you may need to add a Proxy service to the `scraper.py`.
