
# Local Configuration for testing 


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


    

def get_pool():
    DATABASE_URL = "local cnnection url"
    pool = sqlalchemy.create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
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

        #Tool tanÄ±mlama
    retail_tool = Tool(
        function_declarations = [get_data_item,get_video,get_video_by_filter]
    )
    
    #model inÅŸaasÄ±
    model = GenerativeModel(
        "gemini-1.5-pro-002",
        generation_config = GenerationConfig(temperature=0),
        tools = [retail_tool],
    )

    chat = model.start_chat()

    return chat