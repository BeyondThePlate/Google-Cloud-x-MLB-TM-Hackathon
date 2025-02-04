from backend_project_app.blueprints.db.routes import get_db
from vertexai.generative_models import (
    Part
)
import backend_project_app.blueprints.db.db_models.video_model as video_model
import backend_project_app.blueprints.db.db_models.video_entities as video_entities
from backend_project_app.blueprints.db.model import get_video_by_filter,getItem
from backend_project_app.uzak import get_model_embeddings_candidadates
from abc import ABC,abstractmethod
 


class ResponseHandler(ABC):
  @abstractmethod
  def handle(self, response, chat):
    pass


class DefaultResponseHandler(ResponseHandler):
  def handle(self, response, chat):
    return response.text
  
class DataItemResponseHandler(ResponseHandler):
  def handle(self, response, chat):
    query = response.candidates[0].content.parts[0].function_call.args['title']
    result = get_db(query)

    response = chat.send_message(
    Part.from_function_response(
       name = "get_data_item",
       response = {
           "content": str(result)
       }
     )
    )
    return response.text


class VectorSearchHandler(ResponseHandler):
  def handle(self, response,  chat):
 
    
    query = response.candidates[0].content.parts[0].function_call.args

    print(query,"query")
    print(query['user_prompt'],"query")


    _,embeddings,candidates_endpoint = get_model_embeddings_candidadates([query['user_prompt']])
 


    

    DEPLOYED_INDEX_ID = f"deployed index id"

    response = candidates_endpoint.find_neighbors(
      deployed_index_id=DEPLOYED_INDEX_ID,
      queries=embeddings,
      num_neighbors=5,
    )

    list_of_items = []

    for item in response[0]:
      list_of_items.append(getItem(item.id))

    response = chat.send_message(
            Part.from_function_response(
                name="get_item_vector_search",
                response={"content": str(list_of_items)}
        )
    )


    return response.text



class VideoResponseHandler(ResponseHandler):
    def handle(self, response, chat):
        result = video_entities.get_all_out_out_values()
        response = chat.send_message(
            Part.from_function_response(
                name="get_video",
                response={"content": str(result)}
            )
        )
        return response.text

class VideoByFilterResponseHandler(ResponseHandler):
    def handle(self, response, chat):
      query = response.candidates[0].content.parts[0].function_call.args
      print(query,"query")

      result = get_video_by_filter(query)
      print(result,"result")


      response = chat.send_message(
        Part.from_function_response(
            name="get_video_by_filter",
            response={"content": str(result)}
        )
      )

      return response.text




class ResponseHandlerFactory:
  @staticmethod
  def create_handler(response):
    if response.candidates[0].content.parts[0].function_call is None:
      return DefaultResponseHandler()
    
    function_name = response.candidates[0].content.parts[0].function_call.name
    handlers = {
        "get_data_item": DataItemResponseHandler(),
        "get_video": VideoResponseHandler(),
        "get_video_by_filter": VideoByFilterResponseHandler(),
        "get_item_vector_search": VectorSearchHandler()
    }
    return handlers.get(function_name, DefaultResponseHandler())
  

  
def getResponse(response,chat):
  handler = ResponseHandlerFactory.create_handler(response)
  return handler.handle(response, chat)