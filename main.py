from fastapi import FastAPI, UploadFile, File, HTTPException
from db import SessionLocal, FileHash
from utils import generate_file_hash
import os
import uuid

app = FastAPI()

# Folder where uploaded files will be saved
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

from typing import List

@app.post("/upload")
async def upload_files(file: List[UploadFile] = File(...)):
    db = SessionLocal()
    results = []
    try:
        for f in file:
            contents = await f.read()
            f.file.seek(0)
            hash_value = generate_file_hash(f.file)
            existing = db.query(FileHash).filter_by(hash=hash_value).first()
            if existing:
                results.append({"filename": f.filename, "status": "duplicate", "message": "⚠️ File already exists."})
                continue
            original_filename = f.filename or "uploaded_file"
            safe_filename = f"{uuid.uuid4().hex}_{original_filename}"
            save_path = os.path.join(UPLOAD_DIR, safe_filename)
            with open(save_path, "wb") as out_f:
                out_f.write(contents)
            db.add(FileHash(hash=hash_value, filename=original_filename))
            db.commit()
            results.append({"filename": original_filename, "status": "uploaded", "message": "✅ Uploaded successfully."})
        return {"results": results}
    finally:
        db.close()

if __name__ == "__main__":  
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    