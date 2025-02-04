from backend_project_app.blueprints.db.model import get_pool
import sqlalchemy
from datetime import datetime

# Create (KullanÄ±cÄ± OluÅŸturma)
def create_user(user_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        insert_query = sqlalchemy.text("""
            INSERT INTO users (user_id, first_name, last_name, username, email, country)
            VALUES (:user_id, :first_name, :last_name, :username, :email, :country)
        """)
        try:
            result = db_conn.execute(insert_query, user_data)
            db_conn.commit()
            return {"message": "KullanÄ±cÄ± baÅŸarÄ±yla oluÅŸturuldu", "success": True}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}

# Read (KullanÄ±cÄ± Okuma)
def serialize_user(user):
    if user is None:
        return None
    
    return {
        "user_id": str(user.user_id),
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "username": str(user.username),
        "email": str(user.email),
        "country": str(user.country),
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

def get_user_by_id(user_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT * FROM users WHERE user_id = :user_id
        """)
        result = db_conn.execute(select_query, {"user_id": user_id})
        user = result.fetchone()
        return serialize_user(user)

def get_user_by_email(email):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("""
            SELECT * FROM users WHERE email = :email
        """)
        result = db_conn.execute(select_query, {"email": email})
        user = result.fetchone()
        return serialize_user(user)

def get_all_users():
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("SELECT * FROM users")
        result = db_conn.execute(select_query)
        users = result.fetchall()
        return [serialize_user(user) for user in users]

# Update (KullanÄ±cÄ± GÃ¼ncelleme)
def update_user(user_id, update_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        update_query = sqlalchemy.text("""
            UPDATE users 
            SET first_name = :first_name,
                last_name = :last_name,
                username = :username,
                email = :email,
                country = :country
            WHERE user_id = :user_id
        """)
        try:
            update_data["user_id"] = user_id
            result = db_conn.execute(update_query, update_data)
            db_conn.commit()
            if result.rowcount > 0:
                return {"message": "KullanÄ±cÄ± baÅŸarÄ±yla gÃ¼ncellendi", "success": True}
            return {"message": "KullanÄ±cÄ± bulunamadÄ±", "success": False}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}

# Delete (KullanÄ±cÄ± Silme)
def delete_user(user_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        delete_query = sqlalchemy.text("""
            DELETE FROM users WHERE user_id = :user_id
        """)
        try:
            result = db_conn.execute(delete_query, {"user_id": user_id})
            db_conn.commit()
            if result.rowcount > 0:
                return {"message": "KullanÄ±cÄ± baÅŸarÄ±yla silindi", "success": True}
            return {"message": "KullanÄ±cÄ± bulunamadÄ±", "success": False}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}



