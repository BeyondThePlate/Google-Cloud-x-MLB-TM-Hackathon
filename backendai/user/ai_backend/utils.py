from google.cloud.sql.connector import Connector
import sqlalchemy
import os
from google.cloud import storage
import random
import string
from ai_backend.uzak import baseball

generated_strings = set()



def getconn():
    connector = Connector()

    conn= connector.connect(
        "Connection name",
        "pymysql",
        user="Enter user",
        password="Enter your password",
        db="database instance"
    )
    return conn


def get_pool():
    pool = sqlalchemy.create_engine(
       "mysql+pymysql://",
        creator=getconn,
    )
    return pool

def create_video_entity(video_entity_data):
    pool = get_pool()

    print("Kod çalıştı")

    with pool.connect() as db_conn:
        insert_query = sqlalchemy.text("""
          INSERT INTO video_entities
        (play_id, pose_pitcher_graph_out, pose_catcher_graph_out, pose_hitter_graph_out, 
        map_out, out_out, pose_pitcher_3d_out, pose_hitter_3d_out, pose_catcher_3d_out, heatmap_out)
        VALUES
        (:play_id, :pose_pitcher_graph_out, :pose_catcher_graph_out, :pose_hitter_graph_out,
        :map_out, :out_out, :pose_pitcher_3d_out, :pose_hitter_3d_out, :pose_catcher_3d_out, :heatmap_out)
        """)
        try:
            result = db_conn.execute(insert_query, video_entity_data)
            db_conn.commit()
            return print("Başarılı")
        except Exception as e:
            print(e)
            return print("Hata alındı")

def removeDocs():

  # Dosya yolunu belirleyin
  dosya_yolları = ["HomeRun2.mp4","heatmap_video.mp4","map_video.mp4","output_video.mp4","pose_3d_catcher_video.mp4","pose_3d_hitter_video.mp4","pose_3d_pitcher_video.mp4",
                   "pose_graph_pitcher_video.mp4","pose_graph_hitter_video.mp4","pose_graph_catcher_video.mp4",
                   "HomeRun2_formatted.mp4","heatmap_video_formatted.mp4","map_video_formatted.mp4","output_video_formatted.mp4",
                   "pose_3d_catcher_video_formatted.mp4","pose_3d_hitter_video_formatted.mp4","pose_3d_pitcher_video_formatted.mp4",
                   "pose_graph_pitcher_video_formatted.mp4","pose_graph_hitter_video_formatted.mp4","pose_graph_catcher_video_formatted.mp4",
                   ]

  # Dosyayı silme

  for dosya_yolu in dosya_yolları:
    if os.path.exists(dosya_yolu):
        os.remove(dosya_yolu)
        print(f'{dosya_yolu} dosyası silindi.')
    else:
        print('Dosya bulunamadı.')

def format_videos():

  dosya_yolları = ["HomeRun1.mp4","heatmap_video.mp4","map_video.mp4","output_video.mp4","pose_3d_catcher_video.mp4","pose_3d_hitter_video.mp4",
                   "pose_3d_pitcher_video.mp4","pose_graph_pitcher_video.mp4","pose_graph_hitter_video.mp4","pose_graph_catcher_video.mp4"]


  for filename in dosya_yolları:
      filename_without_extension = filename[:-4]
      if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
          os.system(f"ffmpeg -i {filename} -c:v libx264 -c:a aac {filename_without_extension}_formatted.mp4")
      else:
          continue

def download_from_bucket(bucket_name, source_blob_name, destination_file_name):
    """
    GCS Bucket'tan bir dosyayı indirir.
    :param bucket_name: Bucket adı.
    :param source_blob_name: İndirilecek dosyanın adı.
    :param destination_file_name: İndirilen dosyanın kaydedileceği yerel yol.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f"Dosya {source_blob_name}, {bucket_name} bucket'ından {destination_file_name} olarak indirildi.")

def upload_to_bucket_public(bucket_name, source_file_name, destination_blob_name):
    """
    GCS Bucket'a bir dosya yükler ve public olarak erişilebilir hale getirir.
    """
    if not os.path.exists(source_file_name):
        print(f"Dosya yolu '{source_file_name}' sistemde bulunamadı. Hiçbir işlem yapılmadı.")
        return

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Dosyayı yükle
    blob.upload_from_filename(source_file_name)

    # Public hale getir
    blob.make_public()

    print(f"Dosya {source_file_name}, {bucket_name} bucket'ına {destination_blob_name} ismiyle yüklendi.")
    print(f"Public URL: {blob.public_url}")

    return blob.public_url

def generate_unique_string():
    """Rastgele 8 karakterli benzersiz bir string üretir."""
    while True:
        new_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if new_string not in generated_strings:
            generated_strings.add(new_string)
            return new_string
        
def handleApi(
    frame_toplam =250,
    fileName="HomeRun2.mp4",
    play_id="video5",
    ball_box=False,
    ball_line=False,
    ball_slowmotion=False,
    bat_box=False,
    bat_line=False,
    glove_box=False,
    glove_line=False,
    pitcher_box=True,
    pitcher_pose=False,
    catcher_box=False,
    catcher_pose=False,
    hitter_box=True,
    hitter_pose=False,
    hitter_3d=False,
    catcher_3d=False,
    pitcher_3d=False,
    pitcher_graph=True,
    hitter_graph=True,
    catcher_graph=True,
    map_button=False,
    heatmap=False
):
    download_from_bucket("videostore1", fileName, "HomeRun2.mp4")

    baseball(
        frame_toplam=frame_toplam,
        ball_box=ball_box,
        ball_line=ball_line,
        ball_slowmotion=ball_slowmotion,
        bat_box=bat_box,
        bat_line=bat_line,
        glove_box=glove_box,
        glove_line=glove_line,
        pitcher_box=pitcher_box,
        pitcher_pose=pitcher_pose,
        catcher_box=catcher_box,
        catcher_pose=catcher_pose,
        hitter_box=hitter_box,
        hitter_pose=hitter_pose,
        hitter_3d=hitter_3d,
        catcher_3d=catcher_3d,
        pitcher_3d=pitcher_3d,
        pitcher_graph=pitcher_graph,
        hitter_graph=hitter_graph,
        catcher_graph=catcher_graph,
        map_button=map_button,
        heatmap=heatmap
    )


    print("-" * 50)
    print("HandleApi Fonksiyonu Parametreleri:")
    print(f"fileName: {fileName}")
    print(f"play_id: {play_id}")
    print(f"ball_box: {ball_box}")
    print(f"ball_line: {ball_line}")
    print(f"ball_slowmotion: {ball_slowmotion}")
    print(f"bat_box: {bat_box}")
    print(f"bat_line: {bat_line}")
    print(f"glove_box: {glove_box}")
    print(f"glove_line: {glove_line}")
    print(f"pitcher_box: {pitcher_box}")
    print(f"pitcher_pose: {pitcher_pose}")
    print(f"catcher_box: {catcher_box}")
    print(f"catcher_pose: {catcher_pose}")
    print(f"hitter_box: {hitter_box}")
    print(f"hitter_pose: {hitter_pose}")
    print(f"hitter_3d: {hitter_3d}")
    print(f"catcher_3d: {catcher_3d}")
    print(f"pitcher_3d: {pitcher_3d}")
    print(f"pitcher_graph: {pitcher_graph}")
    print(f"hitter_graph: {hitter_graph}")
    print(f"catcher_graph: {catcher_graph}")
    print(f"map_button: {map_button}")
    print(f"heatmap: {heatmap}")
    print("-" * 50)

    name1 = generate_unique_string()+ ".mp4"
    name2 = generate_unique_string()+ ".mp4"
    name3 = generate_unique_string()+ ".mp4"
    name4 = generate_unique_string()+ ".mp4"
    name5 = generate_unique_string()+ ".mp4"
    name6 = generate_unique_string()+ ".mp4"
    name7 = generate_unique_string()+ ".mp4"
    name8 = generate_unique_string()+ ".mp4"
    name9 = generate_unique_string()+ ".mp4"

    format_videos()

    link1 = upload_to_bucket_public("videostore1","heatmap_video_formatted.mp4",name1)
    link2 = upload_to_bucket_public("videostore1","map_video_formatted.mp4",name2)
    link3 = upload_to_bucket_public("videostore1","output_video_formatted.mp4",name3)
    link4 = upload_to_bucket_public("videostore1","pose_3d_catcher_video_formatted.mp4",name4)
    link5 = upload_to_bucket_public("videostore1","pose_3d_hitter_video_formatted.mp4",name5)
    link6 = upload_to_bucket_public("videostore1","pose_3d_pitcher_video_formatted.mp4",name6)
    link7 = upload_to_bucket_public("videostore1","pose_graph_pitcher_video_formatted.mp4",name7)
    link8 = upload_to_bucket_public("videostore1","pose_graph_hitter_video_formatted.mp4",name8)
    link9 = upload_to_bucket_public("videostore1","pose_graph_catcher_video_formatted.mp4",name9)

    print(link1)
    print(link2)
    print(link3)
    print(link4)
    print(link5)
    print(link6)
    print(link7)
    print(link8)
    print(link9)

    data = {
    "play_id": play_id,
    "heatmap_out": link1,
    "map_out": link2,
    "out_out": link3,
    "pose_catcher_3d_out": link4,
    "pose_hitter_3d_out": link5,
    "pose_pitcher_3d_out": link6,
    "pose_pitcher_graph_out": link7,
    "pose_hitter_graph_out": link8,
    "pose_catcher_graph_out": link9,
    }

    create_video_entity(data)

    removeDocs()


