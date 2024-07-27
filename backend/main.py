#uvicorn main:app  --> command to start the backend


#All the necessary imports
import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


#importing the neccessary functions 
from functions.geminiapi import convert_audio_to_text, get_gemini_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import convert_text_to_speech_gtts
from functions.Text_cleaning import clean_text_for_audio

#Initiliazation the fastapi object
app=FastAPI()


#This defines which all URLs can access the backend
origins=["http://localhost:5173",
         "http://localhost:5174",
         "http://localhost:4173",
         "http://localhost:4174",
         "http://localhost:3000"]


#Configuring the frontend URLs which can access the backend
app.add_middleware (
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


#To check whether the backend is running properly
@app.get("/health")
async def check_health():
    return {"message":"Healthy"}


#To reset the backend for an new interview
@app.get("/reset")
async def reset_msg():
    reset_messages()
    return{"Message":"Reset Done"}


# Post Interview bot response
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
       
    # Convert audio to text
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    message_decoded=convert_audio_to_text(audio_input)
    
    ##if not message_decoded:
        ##return HTTPException(status_code=400, detail="Failed to decode")

    if(message_decoded=="Cant recognize"):
        chat_response="could not recognize the text, please say clearly"

    else:    

        file_name = "stored_data.json"

        try:
            with open(file_name) as user_file:
                data=json.load(user_file)
            elements_number=len(data)
        except:
            elements_number=0
            pass           
        
        if(elements_number==0):
            
            if(message_decoded=="start"):
                chat_response="Please select the domain in which you want to be interviewed."
                store_messages(message_decoded,chat_response)
            else:
                chat_response="Please say start to begin the interview."

        elif(elements_number==2):
            if(message_decoded=="computer networks" or message_decoded== "computer network" or message_decoded=="machine learning"):
               chat_response=get_gemini_response(message_decoded,elements_number)
               store_messages(message_decoded,chat_response)
            else:
               chat_response="Please say a valid domain to start the interview"      

        else:            
            chat_response=get_gemini_response(message_decoded,elements_number)
            store_messages(message_decoded,chat_response)

        if not chat_response:
            return HTTPException(status_code=400, detail="Failed to get chat response")
    
    clean_chat_response=clean_text_for_audio(chat_response)

    audio_output = convert_text_to_speech_gtts(clean_chat_response)
    
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed to get audio output")
    
    def iterfile():
        yield from audio_output  # Use yield from to stream the BytesIO content
    
    return StreamingResponse(iterfile(), media_type="application/octet-stream")   
    
    

    

