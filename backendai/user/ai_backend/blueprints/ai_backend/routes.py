from flask import Blueprint, request, jsonify
from ai_backend.utils import handleApi

aiBack = Blueprint('aiBack',__name__,template_folder='templates')

@aiBack.route('/', methods=['POST'])
def handleVideo():
    try:
        data = request.get_json()
        
        # Değerleri yazdır
        print("frame_toplam:",data.get("frame",250))
        print("fileName:", data.get("fileName", "HomeRun2.mp4"))
        print("play_id:", data.get("play_id", "video5"))
        print("ball_box:", data.get("ball_box", False))
        print("ball_line:", data.get("ball_line", False))
        print("ball_slowmotion:", data.get("ball_slowmotion", False))
        print("bat_box:", data.get("bat_box", False))
        print("bat_line:", data.get("bat_line", False))
        print("glove_box:", data.get("glove_box", False))
        print("glove_line:", data.get("glove_line", False))
        print("pitcher_box:", data.get("pitcher_box", True))
        print("pitcher_pose:", data.get("pitcher_pose", False))
        print("catcher_box:", data.get("catcher_box", False))
        print("catcher_pose:", data.get("catcher_pose", False))
        print("hitter_box:", data.get("hitter_box", True))
        print("hitter_pose:", data.get("hitter_pose", False))
        print("hitter_3d:", data.get("hitter_3d", False))
        print("catcher_3d:", data.get("catcher_3d", False))
        print("pitcher_3d:", data.get("pitcher_3d", False))
        print("pitcher_graph:", data.get("pitcher_graph", True))
        print("hitter_graph:", data.get("hitter_graph", True))
        print("catcher_graph:", data.get("catcher_graph", True))
        print("map_button:", data.get("map_button", False))
        print("heatmap:", data.get("heatmap", False))
        
        # Diğer parametreleri al
        handleApi(
        frame_toplam=data.get("frame",250),
        fileName=data.get("fileName", "HomeRun2.mp4"),
        play_id=data.get("play_id", "video5"),
        ball_box=data.get("ball_box", False),
        ball_line=data.get("ball_line", False),
        ball_slowmotion=data.get("ball_slowmotion", False),
        bat_box=data.get("bat_box", False),
        bat_line=data.get("bat_line", False),
        glove_box=data.get("glove_box", False),
        glove_line=data.get("glove_line", False),
        pitcher_box=data.get("pitcher_box", True),
        pitcher_pose=data.get("pitcher_pose", False),
        catcher_box=data.get("catcher_box", False),
        catcher_pose=data.get("catcher_pose", False),
        hitter_box=data.get("hitter_box", True),
        hitter_pose=data.get("hitter_pose", False),
        hitter_3d=data.get("hitter_3d", False),
        catcher_3d=data.get("catcher_3d", False),
        pitcher_3d=data.get("pitcher_3d", False),
        pitcher_graph=data.get("pitcher_graph", True),
        hitter_graph=data.get("hitter_graph", True),
        catcher_graph=data.get("catcher_graph", True),
        map_button=data.get("map_button", False),
        heatmap=data.get("heatmap", False)
        )
        
        return jsonify({
            "status": "success",
            "message": "Video işleme tamamlandı",
            "data": "Döndü"
        }), 200
        
    except Exception as e:
        print(f"\nHATA OLUŞTU: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500