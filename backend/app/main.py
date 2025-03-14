from fastapi import FastAPI, HTTPException, Depends
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models

# ✅ Create tables in the database
Base.metadata.create_all(bind=engine)
print("✅ Tables created in PostgreSQL")


app = FastAPI(title="Transportation Emissions API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow specific origins (your frontend URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Include API routes
app.include_router(router)

# Ensure this block exists to run the server when `python -m app.main` is used
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Transportation Emissions API"}
