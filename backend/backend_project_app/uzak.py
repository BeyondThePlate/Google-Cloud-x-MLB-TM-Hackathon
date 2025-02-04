from google.cloud.sql.connector import Connector
import sqlalchemy
import vertexai
from vertexai.generative_models import GenerativeModel
import requests
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)
from google.cloud import aiplatform
from vertexai.preview.language_models import TextEmbeddingModel
import tqdm,time
#initialize database

def get_model_embeddings_candidadates(texts,batch_size=5):
    PROJECT_ID = "Enter Project ID"
    LOCATION = "Enter Location"
    aiplatform.init(project=PROJECT_ID,location=LOCATION)
    model = TextEmbeddingModel.from_pretrained("text-embedding-005")    

    candidates_endpoint = aiplatform.MatchingEngineIndexEndpoint("Enter index endpoint")


    embeddings = []
    for i in tqdm.tqdm(range(0, len(texts), batch_size)):
        time.sleep(1)
        batch_texts = texts[i:i+batch_size]
        batch_embeddings = model.get_embeddings(batch_texts)
        embeddings.extend([embedding.values for embedding in batch_embeddings])
    return model,embeddings,candidates_endpoint



def getconn():
    connector = Connector()

    conn= connector.connect(
        "Enter connection id",
        "Enter connection type",
        user="Enter User",
        password="Enter password",
        db="Enter db"
    )
    return conn
    




def get_pool():
    pool = sqlalchemy.create_engine(
       "mysql+pymysql://",
        creator=getconn,
    )
    return pool

    #initiliza ai model ad chat

def get_chat():
    vertexai.init(project="project id" , location="project location")
    model = GenerativeModel("gemini-1.5-pro-002")

    #function declaration
    get_data_item = FunctionDeclaration(
    name="get_data_item",
    description = "gives items according to input title",
    parameters = {
            "type":"object",
            "properties":{"title": {"type":"string","description":"Title Of Entry"}}
        }
    )

    get_video = FunctionDeclaration(
    name="get_video",
    description = "gives video randomly",
    parameters = {
            "type":"object",
            "properties":{"random": {"type":"string","description":"Unimportant entry don't worry about it"}}
        }
    )


    # get_video_by_filter = FunctionDeclaration(
    # name="get_video_by_filter",
    # description = "gives video according to filter parameters",
    # parameters = {
    #         "type":"object",
    #         "properties":{
    #             "play_id": {"type":"string","description":"id of video"},
    #             "user_id": {"type":"string","description":"id of user who owns the video"},
    #             "title": {"type":"string","description":"title of video"},
    #             "description": {"type":"string","description":"description of video"},
    #             "category": {"type":"string","description":"category of video"},
    #             "timestamp": {"type":"string","description":"date of video"},
    #             }
    #     }
    # ) Yeni versiyon iÃ§in gelecek 


    get_video_by_filter = FunctionDeclaration(
    name="get_video_by_filter",
    description = "gives video according to filter parameters",
    parameters = {
            "type":"object",
            "properties":{
                "exit_velocity": {"type":"string","description":"exit velocity of video"},
                "hit_distance": {"type":"string","description":"hit distance of video"},
                "launch_angle": {"type":"string","description":"launch angle of video"},
                }
        }
    )

    get_item_vector_search = FunctionDeclaration(
    name="get_item_vector_search",
    description = "gives items according to user prompt with vector search",
    parameters = {
            "type":"object",
            "properties":{"user_prompt": {"type":"string","description":"User Prompt"}}
        }
    )



        #Tool tanÄ±mlama
    retail_tool = Tool(
        function_declarations = [get_data_item,get_video,get_video_by_filter,get_item_vector_search]
    )

    
    #model inÅŸaasÄ±
    model = GenerativeModel(
        "gemini-1.5-pro-002",
        generation_config = GenerationConfig(temperature=0),
        tools = [retail_tool],
    )

    chat = model.start_chat()

    return chat