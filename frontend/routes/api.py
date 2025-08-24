"""
API proxy routes for the ERP system frontend
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()

# Define the backend API base URL
BACKEND_URL = "http://localhost:8000/api/v1"

@router.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_api(request: Request, path: str):
    """Proxy API requests to the backend"""
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            # Construct the full backend URL
            url = f"{BACKEND_URL}/{path}"

            # Read request data
            data = await request.body()

            # Make the request to the backend API
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=data,
                params=request.query_params
            )

            # Return the response from the backend
            return JSONResponse(content=response.json(), status_code=response.status_code)

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while contacting the backend API: {e}")
