from fastapi import FastAPI, UploadFile, File
from db import SessionLocal, FileHash
from utils import generate_file_hash
from fastapi.responses import JSONResponse
from typing import List
import os
import uuid
from io import BytesIO

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_files(file: List[UploadFile] = File(...)):
    db = SessionLocal()
    results = []
    try:
        for f in file:
            try:
                contents = await f.read()

                # FIX: Avoid reading twice by using BytesIO
                hash_value = generate_file_hash(BytesIO(contents))

                # Check for duplicates
                existing = db.query(FileHash).filter_by(hash=hash_value).first()
                if existing:
                    results.append({
                        "filename": f.filename,
                        "status": "duplicate",
                        "message": "⚠️ File already exists."
                    })
                    continue

                # Save file to disk
                original_filename = f.filename or "uploaded_file"
                safe_filename = f"{uuid.uuid4().hex}_{original_filename}"
                save_path = os.path.join(UPLOAD_DIR, safe_filename)
                with open(save_path, "wb") as out_f:
                    out_f.write(contents)

                # Save file info to DB
                db.add(FileHash(hash=hash_value, filename=original_filename))
                db.commit()

                results.append({
                    "filename": original_filename,
                    "status": "uploaded",
                    "message": "✅ Uploaded successfully."
                })

            except Exception as e:
                results.append({
                    "filename": getattr(f, 'filename', 'unknown'),
                    "status": "error",
                    "message": f"❌ Error: {str(e)}"
                })

        return JSONResponse(content={"results": results})

    except Exception as e:
        return JSONResponse(
            content={"detail": f"❌ Internal server error: {str(e)}"},
            status_code=500
        )

    finally:
        db.close()

if __name__ == "__main__":  
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
