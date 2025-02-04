from backend_project_app.blueprints.db.model import get_pool
import sqlalchemy


def serialize_video_entity(video_entity):
    if video_entity is None:
        return None
    return {
        "id": int(video_entity.id),
        "play_id": str(video_entity.play_id),
        "pose_pitcher_graph_out": str(video_entity.pose_pitcher_graph_out),
        "pose_catcher_graph_out": str(video_entity.pose_catcher_graph_out),
        "pose_hitter_graph_out": str(video_entity.pose_hitter_graph_out),
        "map_out": str(video_entity.map_out),
        "out_out": str(video_entity.out_out),
        "pose_pitcher_3d_out": str(video_entity.pose_pitcher_3d_out),
        "pose_hitter_3d_out": str(video_entity.pose_hitter_3d_out),
        "pose_catcher_3d_out": str(video_entity.pose_catcher_3d_out),
        "heatmap_out": str(video_entity.heatmap_out)
    }

def create_video_entity(video_entity_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        insert_query = sqlalchemy.text("""
            INSERT INTO video_entities 
            (play_id, pose_pitcher_graph_out, pose_catcher_graph_out, pose_hitter_graph_out, map_out, out_out, 
            pose_pitcher_3d_out, pose_hitter_3d_out, pose_catcher_3d_out, heatmap_out)
            VALUES 
            (:play_id, :pose_pitcher_graph_out, :pose_catcher_graph_out, :pose_hitter_graph_out, :map_out, :out_out,
            :pose_pitcher_3d_out, :pose_hitter_3d_out, :pose_catcher_3d_out, :heatmap_out)
        """)
        try:
            result = db_conn.execute(insert_query, video_entity_data)
            db_conn.commit()
            return {"message": "Video entity başarıyla oluşturuldu", "success": True}
        except Exception as e:
            return {"message": f"Hata: {str(e)}", "success": False}


def get_video_entity(play_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("SELECT * FROM video_entities WHERE play_id = :play_id")
        result = db_conn.execute(select_query, {"play_id": play_id}).fetchone()
        return serialize_video_entity(result)
    

def update_video_entity(play_id, video_entity_data):
    pool = get_pool()
    with pool.connect() as db_conn:
        update_query = sqlalchemy.text("""UPDATE video_entities 
                                     SET pose_pitcher_graph_out = :pose_pitcher_graph_out,
                                     pose_catcher_graph_out = :pose_catcher_graph_out,
                                     pose_hitter_graph_out = :pose_hitter_graph_out,
                                     map_out = :map_out, out_out = :out_out,
                                     pose_pitcher_3d_out = :pose_pitcher_3d_out,
                                     pose_hitter_3d_out = :pose_hitter_3d_out,
                                     pose_catcher_3d_out = :pose_catcher_3d_out,
                                     heatmap_out = :heatmap_out 
                                     WHERE play_id = :play_id""")
        db_conn.execute(update_query, {"play_id": play_id, **video_entity_data})
        db_conn.commit()
        return {"message": "Video entity başarıyla güncellendi", "success": True}
    


def delete_video_entity(play_id):
    pool = get_pool()
    with pool.connect() as db_conn:
        delete_query = sqlalchemy.text("DELETE FROM video_entities WHERE play_id = :play_id")
        db_conn.execute(delete_query, {"play_id": play_id})
        db_conn.commit()
        return {"message": "Video entity başarıyla silindi", "success": True}


def get_all_video_entities():
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("SELECT * FROM video_entities")
        results = db_conn.execute(select_query).fetchall()
        return [serialize_video_entity(result) for result in results]

def get_all_out_out_values():
    pool = get_pool()
    with pool.connect() as db_conn:
        select_query = sqlalchemy.text("SELECT play_id, out_out FROM video_entities")
        results = db_conn.execute(select_query).fetchall()
        return [{"play_id": result.play_id, "out_out": str(result.out_out)} for result in results]

