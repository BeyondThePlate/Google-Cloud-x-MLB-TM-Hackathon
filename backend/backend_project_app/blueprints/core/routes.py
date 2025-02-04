from flask import Blueprint,jsonify, request
import os
import google.cloud.storage as storage
import requests

core = Blueprint('core',__name__,template_folder='templates')


bucket_name = 'bucket name'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud_admin_key.json"

storage_client = storage.Client.from_service_account_json('cloud_admin_key.json')


@core.route('/')
def index():
    return "That a index endpoint"


@core.route('/get_signed_url',methods=['POST'])
def get_signed_url():
    # Request body'den filename'i al
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({"error": "filename gerekli"}), 400
        
    filename = data['filename']
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    # Signed URL'yi al
    url = blob.generate_signed_url(
        version="v4",
        method="PUT",
        expiration=15 * 60,  # 15 dakika geçerli
        content_type="application/octet-stream",
    )

    return jsonify({"url": url, "fileName": filename})


@core.route('/vm_stimulate', methods=['POST'])
def vm_stimulate():
    try:
        # Request body'den gelen verileri al
        data = request.get_json()

        print("Data başarı ile alındı!")
        
        # VM'in IP adresi (bunu kendi IP adresinizle değiştirin)
        VM_URL = "VM URL"
        
        # VM'e POST isteği gönder
        response = requests.post(
            VM_URL,
            json={
                "frame": data.get("frame", 250),
                "fileName": data.get("fileName", "HomeRun2.mp4"),
                "play_id": data.get("play_id", "video5"),
                "ball_box": data.get("ball_box", False),
                "ball_line": data.get("ball_line", False),
                "ball_slowmotion": data.get("ball_slowmotion", False),
                "bat_box": data.get("bat_box", False),
                "bat_line": data.get("bat_line", False),
                "glove_box": data.get("glove_box", False),
                "glove_line": data.get("glove_line", False),
                "pitcher_box": data.get("pitcher_box", True),
                "pitcher_pose": data.get("pitcher_pose", False),
                "catcher_box": data.get("catcher_box", False),
                "catcher_pose": data.get("catcher_pose", False),
                "hitter_box": data.get("hitter_box", True),
                "hitter_pose": data.get("hitter_pose", False),
                "hitter_3d": data.get("hitter_3d", False),
                "catcher_3d": data.get("catcher_3d", False),
                "pitcher_3d": data.get("pitcher_3d", False),
                "pitcher_graph": data.get("pitcher_graph", True),
                "hitter_graph": data.get("hitter_graph", True),
                "catcher_graph": data.get("catcher_graph", True),
                "map_button": data.get("map_button", False),
                "heatmap": data.get("heatmap", False)
            }
        )
        
        # VM'den gelen yanıtı kontrol et
        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "message": "Video işleme talebi gönderildi",
                "data": response.json()
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "VM'den hata yanıtı alındı",
                "error": response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

