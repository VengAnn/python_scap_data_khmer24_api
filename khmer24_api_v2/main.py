from fastapi import FastAPI, Query, HTTPException
from scraper import Khmer24Scraper

app = FastAPI(
    title="Khmer24 Data API",
    description="A simple API to search and retrieve data from Khmer24",
    version="1.0.0"
)

scraper = Khmer24Scraper()

@app.get("/")
async def root():
    return {
        "message": "Khmer24 Data API is running",
        "endpoints": {
            "all_ads": "/api/all",
            "search": "/api/search?q={keyword}",
            "item_detail": "/api/item/{item_id}",
            "documentation": "/docs"
        }
    }

@app.get("/api/all")
async def api_all(
    limit: int = Query(30, description="Number of results to return", ge=1, le=5000),
    offset: int = Query(0, description="Offset for pagination", ge=0)
):
    """
    Retrieve the general feed of all ads from Khmer24.
    """
    response = scraper.search(keyword=None, limit=limit, offset=offset)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response)
        
    return response

@app.get("/api/search")
async def api_search(
    q: str = Query(..., description="The search keyword", min_length=1),
    limit: int = Query(30, description="Number of results to return", ge=1, le=5000),
    offset: int = Query(0, description="Offset for pagination", ge=0)
):
    """
    Search for items on Khmer24.
    Returns results and pagination info (total, offset, limit).
    """
    response = scraper.search(q, limit=limit, offset=offset)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response)
        
    return response

@app.get("/api/item/{item_id}")
async def get_item_detail(item_id: str):
    """
    Get full details for a specific item using its ID.
    Example: /api/item/12903262
    """
    response = scraper.get_details(item_id)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response)
        
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
