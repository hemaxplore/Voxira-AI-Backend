# routes/history.py
from fastapi import APIRouter, Query
from utils.firebase import db
from fastapi import Form  

router = APIRouter()

# ---------- GET HISTORY ----------
@router.get("/")
def get_user_history(user_id: str = Query(...)):
    try:
        history = db.child("users").child(user_id).child("history").get().val()

        if not history:
            return {"transcripts": {}}

        formatted_history = {}

        # ⭐ ADD history_id into each record
        for key, entry in history.items():
            formatted_history[key] = {
                "history_id": key,
                "file_name": entry.get("file_name"),
                "transcript": entry.get("transcript"),
                "timestamp": entry.get("timestamp"),
                "title": entry.get("title")   # ⭐ REQUIRED
            }

        return {"transcripts": formatted_history}

    except Exception as e:
        return {"error": str(e)}

# ---------- DELETE HISTORY ----------
@router.delete("/delete")
def delete_history(user_id: str, history_id: str):
    try:
        # ✅ DELETE FROM history
        db.child("users") \
          .child(user_id) \
          .child("history") \
          .child(history_id) \
          .remove()

        return {"message": "Deleted successfully"}

    except Exception as e:
        return {"error": str(e)}
    
# ---------- TITLE AUTO GENERATOR -------------
@router.post("/history/set-title")
def set_history_title(
    user_id: str = Form(...),
    history_id: str = Form(...),
    title: str = Form(...)
):

    db.child("users")\
      .child(user_id)\
      .child("history")\
      .child(history_id)\
      .update({"title": title})

    return {"status": "ok"} 