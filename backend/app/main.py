from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Transportation Emissions API")

# Include API routes
app.include_router(router)

# Ensure this block exists to run the server when `python -m app.main` is used
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Transportation Emissions API"}
