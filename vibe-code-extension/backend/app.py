import os
import sqlite3
import secrets
import datetime
import streamlit as st

# Dynamically set the database path relative to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            license_key TEXT UNIQUE NOT NULL,
            tier TEXT NOT NULL DEFAULT 'business',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def generate_key(email: str, tier: str = "business") -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    new_key = f"VIBE-{secrets.token_hex(8).upper()}"
    now = datetime.datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO licenses (user_email, license_key, tier, is_active, created_at) VALUES (?, ?, ?, 1, ?)",
        (email, new_key, tier, now)
    )
    conn.commit()
    conn.close()
    return new_key

def fetch_all_licenses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_email, license_key, tier, is_active, created_at FROM licenses")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize database schema on startup
init_db()

st.set_page_config(page_title="Vibe Extension License Portal", layout="wide")
st.title("Vibe Extension Management Portal")

tab1, tab2 = st.tabs(["Key Generator", "License Registry"])

with tab1:
    st.header("Generate Business License")
    email_input = st.text_input("User or Company Email", placeholder="client@company.com")
    selected_tier = st.selectbox("Tier", ["business", "enterprise"])
    
    if st.button("Generate License Key"):
        if email_input:
            key = generate_key(email_input, selected_tier)
            st.success("License Key Created Successfully!")
            st.code(key, language="text")
        else:
            st.error("Please provide a valid email address.")

with tab2:
    st.header("Active Registrations")
    records = fetch_all_licenses()
    if records:
        data = [
            {
                "Email": r[0],
                "License Key": r[1],
                "Tier": r[2],
                "Status": "Active" if r[3] == 1 else "Revoked",
                "Created At": r[4]
            }
            for r in records
        ]
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No licenses generated yet.")
