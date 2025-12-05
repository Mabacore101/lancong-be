import os
import uvicorn

if __name__ == "__main__":
    # Get PORT from environment, default to 8000
    port = int(os.getenv("PORT", "8000"))
    
    # Run uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
