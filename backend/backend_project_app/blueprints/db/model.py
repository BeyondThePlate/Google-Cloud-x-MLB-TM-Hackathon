from decimal import Decimal
from flask import Flask
import sqlalchemy
from backend_project_app.uzak import get_pool


previous_ids = set()

def get_db(query):
    pool = get_pool()


    with pool.connect() as db_conn:
        select_item = sqlalchemy.text(
            "SELECT * FROM home_run_data WHERE title LIKE :title"
        )

        res = db_conn.execute(select_item, parameters={"title": f"%{query}%"})
        rows = res.fetchall()
        
        columns = ["play_id", "title", "ExitVelocity", "HitDistance", "LaunchAngle", "video"]
    
        result_json = []
        for row in rows:
            row_dict = {columns[i]: float(value) if isinstance(value, Decimal) else value.strip() if isinstance(value, str) else value for i, value in enumerate(row)}
            result_json.append(row_dict)
            print(row)

    return result_json


def get_video_by_filter(query):
    pool = get_pool()
    with pool.connect() as db_conn:
        conditions = []
        parameters = {}

        if query.get("exit_velocity"):
            conditions.append("ExitVelocity >= :exit_velocity")
            parameters["exit_velocity"] = query.get("exit_velocity")

        if query.get("hit_distance"):
            conditions.append("HitDistance >= :hit_distance")
            parameters["hit_distance"] = query.get("hit_distance")

        if query.get("launch_angle"):
            conditions.append("LaunchAngle >= :launch_angle")
            parameters["launch_angle"] = query.get("launch_angle")


        if conditions:
            where_clause = " AND ".join(conditions)
        else:
            where_clause = "1=1"

        print(where_clause,"where_clause")
        select_item = sqlalchemy.text(
            f"SELECT * FROM home_run_data WHERE {where_clause} LIMIT 10"
        )


        res = db_conn.execute(select_item, parameters)
        rows = res.fetchall()
        
        columns = ["play_id", "title", "ExitVelocity", "HitDistance", "LaunchAngle", "video"]
    
        result_json = []
        for row in rows:
            row_dict = {columns[i]: float(value) if isinstance(value, Decimal) else value.strip() if isinstance(value, str) else value for i, value in enumerate(row)}
            result_json.append(row_dict)
            print(row)

    return result_json

def getItem(n):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text(f"""SELECT * 
                    FROM home_run_data
                    LIMIT 1 OFFSET {n};""")
        result = db_conn.execute(select_query)
        item = result.fetchone()
        return item



def get_random_data():
    pool = get_pool()

    #global previous_ids

    with pool.connect() as db_conn:

        select_item = sqlalchemy.text(
                "SELECT * FROM home_run_data LIMIT 20"
            )

        res = db_conn.execute(select_item)
        rows = res.fetchall()

        columns = ["play_id", "title", "ExitVelocity", "HitDistance", "LaunchAngle", "video"]
        
        result_json = []
        for row in rows:
            row_dict = {columns[i]: float(value) if isinstance(value, Decimal) else value.strip() if isinstance(value, str) else value for i, value in enumerate(row)}
            result_json.append(row_dict)
            print(row)

    return result_json



