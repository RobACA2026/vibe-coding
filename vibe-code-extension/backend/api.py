import sqlite3
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = "backend/app.db"

app = FastAPI(title="Vibe Extension Entitlement API")

# Enable CORS so the browser extension content/background scripts can communicate with the local server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LicenseRequest(BaseModel):
    license_key: str

class LicenseResponse(BaseModel):
    active: bool
    tier: str
    email: str

def verify_license_db(key: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_email, tier, is_active FROM licenses WHERE license_key = ?",
        (key,)
    )
    result = cursor.fetchone()
    conn.close()
    return result

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/v1/validate-license", response_model=LicenseResponse)
def validate_license(payload: LicenseRequest):
    record = verify_license_db(payload.license_key)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License key not found"
        )
    
    email, tier, is_active = record
    if is_active != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="License key has been revoked"
        )
        
    return LicenseResponse(
        active=True,
        tier=tier,
        email=email
    )