import streamlit as st
import requests
from db import SessionLocal, FileHash

# Backend API endpoint
API_URL = "https://duplidrop.onrender.com/upload"

# Page configuration
st.set_page_config(page_title="🔐DupliDrop")
st.title("🔐DupliDrop - For Team Collaboration")
st.write("This app checks if the uploaded files are duplicates using SHA-256 content hashing.")

# File uploader widget
uploaded_files = st.file_uploader("Choose files to upload", type=None, accept_multiple_files=True)

# Upload button logic
if uploaded_files:
    if st.button("🚀 Upload"):
        with st.spinner("Uploading..."):
            try:
                files = []
                for f in uploaded_files:
                    file_bytes = f.read()
                    files.append(("file", (f.name, file_bytes, f.type)))
                    f.seek(0)

                response = requests.post(API_URL, files=files)

                if response.status_code == 200:
                    resp_json = response.json()
                    if "results" in resp_json:
                        for result in resp_json["results"]:
                            if result["status"] == "uploaded":
                                st.success(f"✅ {result['filename']}: {result['message']}")
                            elif result["status"] == "duplicate":
                                st.warning(f"⚠️ {result['filename']}: {result['message']}")
                    else:
                        st.success(resp_json.get("message", "✅ Files uploaded successfully."))
                else:
                    # Safe handling of non-JSON error responses
                    try:
                        error_detail = response.json().get("detail", "⚠️ Something went wrong.")
                    except ValueError:
                        error_detail = f"⚠️ Server returned status {response.status_code}: {response.text}"
                    st.warning(error_detail)
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to FastAPI backend. Make sure the server is running.")

# Display all file hashes directly (no dropdown)
st.subheader("🗂️ Files in Database")
try:
    db = SessionLocal()
    file_hashes = db.query(FileHash).all()
    if file_hashes:
        for fh in file_hashes:
            with st.container():
                cols = st.columns([4, 6, 1])

                # Filename
                cols[0].markdown(f"📄 **{fh.filename}**")

                # Hash code display
                cols[1].code(fh.hash, language="text")

                # Delete button
                delete_btn = cols[2].button("🗑️", key=f"delete_{fh.hash}", use_container_width=True)
                if delete_btn:
                    db.delete(fh)
                    db.commit()
                    st.success(f"Deleted `{fh.filename}`")
                    st.rerun()
    else:
        st.info("No files found in the database.")
finally:
    if 'db' in locals():
        db.close()
