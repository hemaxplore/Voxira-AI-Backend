import whisper
from fastapi import APIRouter, File, UploadFile, Form
import os
from models.whisper_model import transcribe_audio
from utils.firebase import db
from datetime import datetime
import shutil

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def transcribe(file: UploadFile = File(...), user_id: str = Form(...)):

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # ---------- SAVE FILE ----------
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---------- TRANSCRIBE ----------
        transcript = transcribe_audio(file_location)

        timestamp = datetime.now().isoformat()

        history_data = {
            "file_name": file.filename,
            "transcript": transcript,
            "timestamp": timestamp,
            "translated_to": [],
        }

        # save history
        db.child("users").child(user_id).child("history").push(history_data)

        return {
            "transcript": transcript,
            "timestamp": timestamp
        }

    except Exception as e:
        return {"error": str(e)}

    # ✅ VERY IMPORTANT PART
    finally:
        # ---------- AUTO DELETE AUDIO ----------
        if os.path.exists(file_location):
            os.remove(file_location)
            print(f"Deleted temp file: {file_location}")
