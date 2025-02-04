from backend_project_app.blueprints.db.model import get_pool
import sqlalchemy
from datetime import datetime

def serialize_video(video):
    if video is None:
        return None
    
    return {
        "play_id": str(video.play_id),
        "user_id": str(video.user_id),
        "title": str(video.title),
        "description": str(video.description),
        "video_url": str(video.video_url),
        "category": str(video.category),
        "visibility": str(video.visibility),
        "views": int(video.views),
        "created_at": video.created_at.isoformat() if video.created_at else None
    }

# Create (Video OluÅŸturma)
def create_video(video_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        insert_query = sqlalchemy.text("""
            INSERT INTO videos 
            (play_id, user_id, title, description, video_url, category, visibility)
            VALUES 
            (:play_id, :user_id, :title, :description, :video_url, :category, :visibility)
        """)
        try:
            result = db_conn.execute(insert_query, video_data)
            db_conn.commit()
            return {"message": "Video baÅŸarÄ±yla oluÅŸturuldu", "success": True}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}

# Read (Video Okuma)
def get_video_by_id(play_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT * FROM videos WHERE play_id = :play_id
        """)
        result = db_conn.execute(select_query, {"play_id": play_id})
        video = result.fetchone()
        return serialize_video(video)

def get_videos_by_user_id(user_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT * FROM videos WHERE user_id = :user_id
        """)
        result = db_conn.execute(select_query, {"user_id": user_id})
        videos = result.fetchall()
        return [serialize_video(video) for video in videos]

def get_public_videos():
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT * FROM videos WHERE visibility = 'public' ORDER BY created_at DESC
        """)
        result = db_conn.execute(select_query)
        videos = result.fetchall()
        return [serialize_video(video) for video in videos]

def increment_views(play_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        update_query = sqlalchemy.text("""
            UPDATE videos SET views = views + 1 WHERE play_id = :play_id
        """)
        try:
            db_conn.execute(update_query, {"play_id": play_id})
            db_conn.commit()
            return True
        except Exception:
            return False

# Update (Video GÃ¼ncelleme)
def update_video(play_id, update_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        update_query = sqlalchemy.text("""
            UPDATE videos 
            SET title = :title,
                description = :description,
                video_url = :video_url,
                category = :category,
                visibility = :visibility
            WHERE play_id = :play_id
        """)
        try:
            update_data["play_id"] = play_id
            result = db_conn.execute(update_query, update_data)
            db_conn.commit()
            if result.rowcount > 0:
                return {"message": "Video baÅŸarÄ±yla gÃ¼ncellendi", "success": True}
            return {"message": "Video bulunamadÄ±", "success": False}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}

# Delete (Video Silme)
def delete_video(play_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        delete_query = sqlalchemy.text("""
            DELETE FROM videos WHERE play_id = :play_id
        """)
        try:
            result = db_conn.execute(delete_query, {"play_id": play_id})
            db_conn.commit()
            if result.rowcount > 0:
                return {"message": "Video baÅŸarÄ±yla silindi", "success": True}
            return {"message": "Video bulunamadÄ±", "success": False}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}