from backend_project_app.blueprints.db.model import get_pool
import sqlalchemy

def serialize_preference(pref):
    if pref is None:
        return None
    
    return {
        "preference_id": int(pref.preference_id),
        "user_id": str(pref.user_id),
        "favorite_team": str(pref.favorite_team),
        "favorite_player": str(pref.favorite_player),
        "favorite_part": str(pref.favorite_part),
        "watching_experience": str(pref.watching_experience),
        "preferred_position": str(pref.preferred_position),
        "dream_stadium": str(pref.dream_stadium)
    }

# Create (Tercih OluÅŸturma)
def create_preference(pref_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        insert_query = sqlalchemy.text("""
            INSERT INTO user_preferences 
            (user_id, favorite_team, favorite_player, favorite_part, 
             watching_experience, preferred_position, dream_stadium)
            VALUES 
            (:user_id, :favorite_team, :favorite_player, :favorite_part,
             :watching_experience, :preferred_position, :dream_stadium)
        """)
        try:
            result = db_conn.execute(insert_query, pref_data)
            db_conn.commit()
            return {"message": "Tercihler baÅŸarÄ±yla oluÅŸturuldu", "success": True}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}

# Read (Tercihleri Okuma)
def get_preference_by_id(preference_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT * FROM user_preferences WHERE preference_id = :preference_id
        """)
        result = db_conn.execute(select_query, {"preference_id": preference_id})
        pref = result.fetchone()
        return serialize_preference(pref)

def get_preferences_by_user_id(user_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT * FROM user_preferences WHERE user_id = :user_id
        """)
        result = db_conn.execute(select_query, {"user_id": user_id})
        prefs = result.fetchall()
        return [serialize_preference(pref) for pref in prefs]

def get_all_preferences():
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("SELECT * FROM user_preferences")
        result = db_conn.execute(select_query)
        prefs = result.fetchall()
        return [serialize_preference(pref) for pref in prefs]

# Update (Tercihleri GÃ¼ncelleme)
def update_preference(preference_id, update_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        update_query = sqlalchemy.text("""
            UPDATE user_preferences 
            SET favorite_team = :favorite_team,
                favorite_player = :favorite_player,
                favorite_part = :favorite_part,
                watching_experience = :watching_experience,
                preferred_position = :preferred_position,
                dream_stadium = :dream_stadium
            WHERE preference_id = :preference_id
        """)
        try:
            update_data["preference_id"] = preference_id
            result = db_conn.execute(update_query, update_data)
            db_conn.commit()
            if result.rowcount > 0:
                return {"message": "Tercihler baÅŸarÄ±yla gÃ¼ncellendi", "success": True}
            return {"message": "Tercih bulunamadÄ±", "success": False}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}

# Delete (Tercihleri Silme)
def delete_preference(preference_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        delete_query = sqlalchemy.text("""
            DELETE FROM user_preferences WHERE preference_id = :preference_id
        """)
        try:
            result = db_conn.execute(delete_query, {"preference_id": preference_id})
            db_conn.commit()
            if result.rowcount > 0:
                return {"message": "Tercih baÅŸarÄ±yla silindi", "success": True}
            return {"message": "Tercih bulunamadÄ±", "success": False}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}