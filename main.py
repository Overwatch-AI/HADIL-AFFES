import uvicorn
from src.api import app

if __name__ == "__main__":
    # The host="0.0.0.0" makes the API accessible from other devices on the same network
    uvicorn.run(app, host="0.0.0.0", port=8000)