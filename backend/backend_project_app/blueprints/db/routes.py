from backend_project_app.uzak import get_pool
from flask import Flask,Blueprint,request
import sqlalchemy
from flask import jsonify
from decimal import Decimal
from backend_project_app.blueprints.db.model import get_db,get_random_data
from backend_project_app.blueprints.db.db_models.user_model import create_user, get_user_by_id, update_user, delete_user, get_all_users,get_user_by_email
from backend_project_app.blueprints.db.db_models.user_pref_model import create_preference, get_preferences_by_user_id, update_preference, delete_preference, get_all_preferences,get_preference_by_id
from backend_project_app.blueprints.db.db_models.video_model import create_video, get_video_by_id,get_videos_by_user_id, get_public_videos, increment_views, update_video, delete_video
from backend_project_app.blueprints.db.db_models.saved_videos import create_saved_video, get_saved_video_by_id, get_user_saved_videos_by_user_id, delete_save_video, delete_all_saved_videos
from backend_project_app.blueprints.db.db_models.video_entities import create_video_entity, get_video_entity, update_video_entity, delete_video_entity
dbRoute = Blueprint('dbRoute',__name__,template_folder='templates')

#If item includes that input in its title fetch all entries if thats true
@dbRoute.route('/get',methods=['POST'])
def getItem():

    query = request.get_json()

    print(query,"query")
    print(query.get('query'),"query")

    result = get_db(query.get('query'))
    
    print(result,"sonuc_json")

    return jsonify(result)


@dbRoute.route('/get_random')
def getRandom():
    result = get_random_data()
    print(result)

    return jsonify(result)


#Video Entities CRUD

@dbRoute.route('/create_video_entity', methods=['POST'])
def create_video_entity_route():
    video_entity_data = request.get_json()
    return jsonify(create_video_entity(video_entity_data))

@dbRoute.route('/get_video_entity/<play_id>', methods=['GET'])
def get_video_entity_route(play_id):
    return jsonify(get_video_entity(play_id))

@dbRoute.route('/update_video_entity/<play_id>', methods=['PUT'])
def update_video_entity_route(play_id):
    video_entity_data = request.get_json()
    return jsonify(update_video_entity(play_id, video_entity_data))

@dbRoute.route('/delete_video_entity/<play_id>', methods=['DELETE'])
def delete_video_entity_route(play_id):
    return jsonify(delete_video_entity(play_id))



#Videos CRUD - Uploaded

@dbRoute.route('/create_video', methods=['POST'])
def create_video_route():
    video_data = request.get_json()
    return jsonify(create_video(video_data))

@dbRoute.route('/get_video_by_id/<video_id>', methods=['GET'])
def get_video_by_id_route(video_id):
    return jsonify(get_video_by_id(video_id))

@dbRoute.route('/get_videos_by_user_id/<user_id>', methods=['GET'])
def get_videos_by_user_id_route(user_id):
    return jsonify(get_videos_by_user_id(user_id))

@dbRoute.route('/get_public_videos', methods=['GET'])
def get_public_videos_route():
    return jsonify(get_public_videos())

@dbRoute.route('/increment_views/<video_id>', methods=['PUT'])
def increment_views_route(video_id):
    return jsonify(increment_views(video_id))

@dbRoute.route('/update_video/<video_id>', methods=['PUT'])
def update_video_route(video_id):
    video_data = request.get_json()
    return jsonify(update_video(video_id, video_data))

@dbRoute.route('/delete_video/<video_id>', methods=['DELETE'])
def delete_video_route(video_id):
    return jsonify(delete_video(video_id))



#Saved Videos CRUD

@dbRoute.route('/create_saved_video', methods=['POST'])
def create_saved_video_route():
    save_data = request.get_json()
    return jsonify(create_saved_video(save_data))

@dbRoute.route('/get_saved_video_by_id/<saved_video_id>', methods=['GET'])
def get_saved_video_by_id_route(saved_video_id):
    return jsonify(get_saved_video_by_id(saved_video_id))

@dbRoute.route('/get_user_saved_videos_by_user_id/<user_id>', methods=['GET'])
def get_user_saved_videos_by_user_id_route(user_id):
    return jsonify(get_user_saved_videos_by_user_id(user_id))

@dbRoute.route('/delete_save_video/<user_id>/<play_id>', methods=['DELETE'])
def delete_save_video_route(user_id, play_id):
    return jsonify(delete_save_video(user_id, play_id)) 

@dbRoute.route('/delete_all_saved_videos/<user_id>', methods=['DELETE'])
def delete_all_saved_videos_route(user_id):
    return jsonify(delete_all_saved_videos(user_id))        


#User_Preferences CRUD

@dbRoute.route('/create_preference', methods=['POST'])
def create_preference_route():
    pref_data = request.get_json()
    return jsonify(create_preference(pref_data))

@dbRoute.route('/get_user_preferences/<user_id>', methods=['GET'])
def get_user_preferences_route(user_id):
    return jsonify(get_preferences_by_user_id(user_id))

@dbRoute.route('/update_preference/<pref_id>', methods=['PUT'])
def update_preference_route(pref_id):
    pref_data = request.get_json()
    return jsonify(update_preference(pref_id, pref_data))   

@dbRoute.route('/delete_preference/<pref_id>', methods=['DELETE'])
def delete_preference_route(pref_id):
    return jsonify(delete_preference(pref_id))

@dbRoute.route('/get_all_preferences', methods=['GET'])
def get_all_preferences_route():
    return jsonify(get_all_preferences())

@dbRoute.route('/get_preference_by_id/<preference_id>', methods=['GET'])
def get_preference_by_id_route(preference_id):
    return jsonify(get_preference_by_id(preference_id))



#User CRUD

@dbRoute.route('/create_user', methods=['POST'])
def create_user_route():
    user_data = request.get_json()
    return jsonify(create_user(user_data))

@dbRoute.route('/get_user_by_id/<user_id>', methods=['GET'])
def get_user_by_id_route(user_id):
    return jsonify(get_user_by_id(user_id))

@dbRoute.route('/get_user_by_email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    return jsonify(get_user_by_email(email))

@dbRoute.route('/update_user/<user_id>', methods=['PUT'])   
def update_user_route(user_id):
    user_data = request.get_json()
    return jsonify(update_user(user_id, user_data))

@dbRoute.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return jsonify(delete_user(user_id))

@dbRoute.route('/get_all_users', methods=['GET'])
def get_all_users_route():
    return jsonify(get_all_users())

