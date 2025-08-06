import streamlit as st
import requests
from db import SessionLocal, FileHash

# FastAPI backend URL
API_URL = "http://localhost:8000/upload"

st.set_page_config(page_title="📁 File Uploader with Duplicate Detection")

st.title("📂 Upload File with Duplicate Detection")
st.write("This app checks if the uploaded file is a duplicate using content hash (SHA-256).")

uploaded_file = st.file_uploader("Choose a file to upload", type=None)

if uploaded_file:
    if st.button("🚀 Upload"):
        with st.spinner("Uploading..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(API_URL, files=files)

                if response.status_code == 200:
                    st.success(response.json().get("message", "✅ File uploaded successfully."))
                else:
                    st.warning(response.json().get("detail", "⚠️ Something went wrong."))

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to FastAPI backend. Make sure the server is running.")

# Show all file hashes from the database
st.subheader("🗂️ Files in Database")
try:
    db = SessionLocal()
    file_hashes = db.query(FileHash).all()
    if file_hashes:
        header_cols = st.columns([4, 6, 1])
        header_cols[0].markdown("**File Name**")
        header_cols[1].markdown("**Hash**")
        header_cols[2].markdown("")
        for fh in file_hashes:
            cols = st.columns([4, 6, 1])
            cols[0].write(fh.filename)
            cols[1].write(fh.hash)
            with cols[2]:
                with st.form(key=f"delete_{fh.hash}"):
                    delete = st.form_submit_button("🗑️", use_container_width=True)
                    if delete:
                        db.delete(fh)
                        db.commit()
                        st.success(f"Deleted {fh.hash}")
                        st.rerun()
    else:
        st.info("No files found in the database.")
finally:
    if 'db' in locals():
        db.close()
