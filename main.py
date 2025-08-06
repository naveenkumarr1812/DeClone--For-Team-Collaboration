from fastapi import FastAPI, UploadFile, File, HTTPException
from db import SessionLocal, FileHash
from utils import generate_file_hash
import os
import uuid

app = FastAPI()

# Folder where uploaded files will be saved
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read file contents
    contents = await file.read()
    file.file.seek(0)

    # Generate SHA-256 hash
    hash_value = generate_file_hash(file.file)

    # Connect to database
    db = SessionLocal()
    try:
        # Check if hash already exists in database
        existing = db.query(FileHash).filter_by(hash=hash_value).first()
        if existing:
            raise HTTPException(status_code=400, detail="⚠️ This file already exists.")

        # Safely create a unique filename
        original_filename = file.filename or "uploaded_file"
        safe_filename = f"{uuid.uuid4().hex}_{original_filename}"
        save_path = os.path.join(UPLOAD_DIR, safe_filename)

        # Save file
        with open(save_path, "wb") as f:
            f.write(contents)

        # Save hash and filename to database
        db.add(FileHash(hash=hash_value, filename=original_filename))
        db.commit()

        return {"message": "✅ File uploaded successfully."}
    finally:
        db.close()

if __name__ == "__main__":  
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    