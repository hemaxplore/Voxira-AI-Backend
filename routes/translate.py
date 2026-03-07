from fastapi import APIRouter, Form
from googletrans import Translator
from utils.firebase import db
from datetime import datetime

router = APIRouter()
translator = Translator()


# -------- TEXT SPLITTER ----------
def split_text(text, max_chars=4000):
    parts = []
    while len(text) > max_chars:
        split_at = text.rfind(" ", 0, max_chars)
        if split_at == -1:
            split_at = max_chars
        parts.append(text[:split_at])
        text = text[split_at:]
    parts.append(text)
    return parts


@router.post("/")
def translate_text(
    user_id: str = Form(...),
    text: str = Form(...),
    target_lang: str = Form(...)
):
    try:

        chunks = split_text(text)
        translated_full = ""

        # translate piece by piece
        for chunk in chunks:
            result = translator.translate(chunk, dest=target_lang)
            translated_full += result.text + " "

        translated_full = translated_full.strip()

        translation_data = {
            "translated_to": target_lang,
            "translated_text": translated_full,
            "timestamp": datetime.now().isoformat()
        }

        db.child("users").child(user_id)\
          .child("translations").push(translation_data)

        return {"translated": translated_full}

    except Exception as e:
        return {"error": str(e)}