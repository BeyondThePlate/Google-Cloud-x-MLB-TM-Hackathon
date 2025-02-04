from backend_project_app.blueprints.db.model import get_pool
import sqlalchemy
from datetime import datetime

def serialize_saved_video(saved):
    if saved is None:
        return None
    
    return {
        "save_id": int(saved.save_id),
        "user_id": str(saved.user_id),
        "play_id": str(saved.play_id),
        "saved_at": saved.saved_at.isoformat() if saved.saved_at else None
    }

# Create (Video Kaydetme)
def create_saved_video(save_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        insert_query = sqlalchemy.text("""
            INSERT INTO saved_videos (user_id, play_id)
            VALUES (:user_id, :play_id)
        """)
        try:
            result = db_conn.execute(insert_query, save_data)
            db_conn.commit()
            return {"message": "Video baÅŸarÄ±yla kaydedildi", "success": True}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}

# Read (Kaydedilen VideolarÄ± Okuma)
def get_saved_video_by_id(save_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT * FROM saved_videos WHERE save_id = :save_id
        """)
        result = db_conn.execute(select_query, {"save_id": save_id})
        saved = result.fetchone()
        return serialize_saved_video(saved)

def get_user_saved_videos_by_user_id(user_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT sv.*, v.title, v.description, v.video_url, v.category, v.visibility
            FROM saved_videos sv
            JOIN videos v ON sv.play_id = v.play_id
            WHERE sv.user_id = :user_id
            ORDER BY sv.saved_at DESC
        """)
        result = db_conn.execute(select_query, {"user_id": user_id})
        saved_videos = result.fetchall()
        return [{
            **serialize_saved_video(video),
            "title": str(video.title),
            "description": str(video.description),
            "video_url": str(video.video_url),
            "category": str(video.category),
            "visibility": str(video.visibility)
        } for video in saved_videos]



# Delete (Kaydedilen Videoyu Silme)
def delete_save_video(user_id, play_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        delete_query = sqlalchemy.text("""
            DELETE FROM saved_videos 
            WHERE user_id = :user_id AND play_id = :play_id
        """)
        try:
            result = db_conn.execute(delete_query, {
                "user_id": user_id,
                "play_id": play_id
            })
            db_conn.commit()
            if result.rowcount > 0:
                return {"message": "Video kaydÄ± baÅŸarÄ±yla kaldÄ±rÄ±ldÄ±", "success": True}
            return {"message": "KayÄ±tlÄ± video bulunamadÄ±", "success": False}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}

def delete_all_saved_videos(user_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        delete_query = sqlalchemy.text("""
            DELETE FROM saved_videos WHERE user_id = :user_id
        """)
        try:
            result = db_conn.execute(delete_query, {"user_id": user_id})
            db_conn.commit()
            return {"message": "TÃ¼m kayÄ±tlÄ± videolar silindi", "success": True}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}