import mariadb
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# --- Database Connection ---
# It's recommended to use a more robust connection management system for production.
# This simple setup is for demonstration purposes.

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "cybernexus")

def get_db_connection():
    try:
        conn = mariadb.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=True  # Automatically commit transactions
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        # In a real app, you'd have more robust error handling or a retry mechanism.
        raise HTTPException(status_code=500, detail="Database connection failed")

# --- Table Initialization ---
def create_threats_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                indicator VARCHAR(255) NOT NULL,
                type VARCHAR(50) NOT NULL,
                source VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
        """)
        print("Table 'threats' created or already exists.")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threat_audit (
                id INT AUTO_INCREMENT PRIMARY KEY,
                threat_id INT,
                action VARCHAR(50) NOT NULL,
                action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (threat_id) REFERENCES threats(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """)
        print("Table 'threat_audit' created or already exists.")
    except mariadb.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

# --- Pydantic Models ---
class Threat(BaseModel):
    indicator: str  # e.g., IP, URL, file hash
    type: str       # e.g., phishing, malware, ddos
    source: str     # e.g., "internal-honeypot", "user-report"

class AuditEntry(BaseModel):
    id: int
    threat_id: int
    action: str
    action_timestamp: datetime

# --- FastAPI App ---
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_threats_table()

@app.post("/threats/")
def create_threat(threat: Threat):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert the new threat
        cursor.execute(
            "INSERT INTO threats (indicator, type, source) VALUES (?, ?, ?)",
            (threat.indicator, threat.type, threat.source)
        )
        threat_id = cursor.lastrowid

        # Create an audit log entry
        cursor.execute(
            "INSERT INTO threat_audit (threat_id, action) VALUES (?, ?)",
            (threat_id, "CREATED")
        )
        
        return {"id": threat_id, **threat.dict()}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.get("/threats/", response_model=List[Threat])
def get_threats(indicator: str = None, type: str = None, source: str = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT indicator, type, source FROM threats"
    conditions = []
    params = []
    
    if indicator:
        conditions.append("indicator = ?")
        params.append(indicator)
    if type:
        conditions.append("type = ?")
        params.append(type)
    if source:
        conditions.append("source = ?")
        params.append(source)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY created_at DESC"

    try:
        cursor.execute(query, tuple(params))
        threats = cursor.fetchall()
        return threats
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.get("/threats/{threat_id}/audit", response_model=List[AuditEntry])
def get_threat_audit_trail(threat_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, threat_id, action, action_timestamp FROM threat_audit WHERE threat_id = ? ORDER BY action_timestamp DESC",
            (threat_id,)
        )
        audit_trail = cursor.fetchall()
        if not audit_trail:
            # This is not an error, it just means no history. Return empty list.
            return []
        return audit_trail
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.get("/")
def read_root():
    return {"message": "CyberNexus API is running and connected to MariaDB."}
