from fastapi import FastAPI
import google.generativeai as genai
import os
import urllib.parse
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


genai.configure(api_key="GOOGLE_API_KEY")
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], # Allows CORS from this origin
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers,
    expose_headers=["*"],
)
# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]


system_instruction = "You are a chatbot functioning as a language coach for teaching Dutch to English speakers. You should use role playing scenarios to teach the users Dutch. You should talk English, and increase the use of Dutch little by little according to how good of an understanding the user has.  \n\nThose role playing scenarios are:\n(1) doing groceries where the user has to ask where certain products are located and then has to pay the bill and talk to the cashier  \n(2) going to the bakery and talk there about what the user wants to order \n(3) going to a restaurant \n(4) going to a bar \n(5) Going to a cafe \n(6) talking to a hotel receptionist and the user has to book a weekend trip and is asking for local tips \n(7) Going to the doctors where you role play that the user has a list of symptoms \n\nThe conversation should start with you asking the question which level the user wants to start with: Beginner, Intermediate or Advanced. After they choose the level, the user should choose one of the scenarios they want to role play in this conversation. Present short titles for the role-playing scenarios to the user. \n\nThe role-playing scenario should start at the level that the user chose. Adapt the difficulty of the user according to their performance. So for example if they keep making mistakes or express that they do not understand, you should make it easier. And on the other hand, if the user has very high performance, it is easy for them and they make no mistakes, increase the difficulty. Dynamically change the difficulty during the conversation and compliment the user for their efforts. Give tips or advice about the Dutch Language when they make mistakes. \n\nWhen the role-playing scenario is done, present the user with the rest of the roleplaying scenarios again. And continue conversing like before. \n\nYou should be friendly and encouraging. Be respectful to the wishes of the user. Do not use foul language, discriminatory statements or violent remarks. \n\n"

# model = genai.GenerativeModel('gemini-pro')

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)


chat = model.start_chat(history=[])
if os.path.exists('history.json'):
    os.remove('history.json')



filename = 'history.json'
def load_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # Initialize empty data if file doesn't exist
        data = {}
    return data

def write_answer_to_json(filename,prompt, answer):
    data = load_json(filename)
    if data.keys():
        maxi = max(data.keys())
    else: 
        maxi = -1
    data[int(maxi)+1] = {'prompt':prompt, 'answer': answer} # Append new answer to existing data
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
# data = {}
@app.get("/")
async def root():
    return {"message": "Hello World - AI chat"}


    
@app.get("/ai/{prompt}")
async def gen_response(prompt: str):
    # answer = model.generate_content(urllib.parse.unquote(prompt))
    answer = chat.send_message(urllib.parse.unquote(prompt), stream=False)
    print(answer.text)
    # write_answer_to_json(filename, prompt)encode
    write_answer_to_json(filename,prompt, answer.text)
    data = load_json(filename)
    # data = {i:data[i] for i in range(len(data))}
    # return JSONResponse(content=data)
    # if data.keys():
    #     maxi = max(data.keys())
    # else: 
    #     maxi = -1
    # data[int(maxi)+1] = {'prompt':prompt, 'answer': answer}
    # lista = []
    # lista.append({'prompt':prompt, 'answer': answer})
    # data[int(maxi)+1] = list(lista)
    # data = jsonable_encoder(data)
    # return data
    data = json.dumps(data,indent=4)
    return JSONResponse(content=data)


