from backend_project_app.uzak import get_chat
from backend_project_app.blueprints.ai.model import getResponse
from flask import Flask,Blueprint,request

aiRoute = Blueprint('aiRoute',__name__,template_folder='templates')





@aiRoute.route('/ask',methods=['POST'])
def getAnswer():

    user_prompt = request.get_json()

    prompt = f"""System Prompt: You are an assistant for a website dedicated to baseball fans, offering a powerful Statcast tool as well as video content similar to YouTube.  
    Your primary role is to assist users by accurately addressing their questions and guiding them to the most relevant content or tools available on the website.  
    If the user is searching for Statcast-related data, provide insights or links to the requested statistics or analyses.  
    If the user is looking for videos, identify the relevant player, game, or event based on their description, query the database for related content, and return the best match. Ensure the video link is properly formatted by removing any unwanted characters like `\r` at the end.  
    Always aim to provide a seamless and enjoyable experience for users, tailored to their interests in baseball.  
    {user_prompt} """

    chat = get_chat()

    response = chat.send_message(prompt)

    answer = getResponse(response,chat)
 
    return str(answer)