import google.generativeai as genai
import speech_recognition as sr
from pydub import AudioSegment
import random
import json
import os


from functions.database import get_recent_messages

GOOGLE_API_KEY="AIzaSyAx39_4AZPywTe69xb3mmz5Ch8zUrzuTw0"
genai.configure(api_key=GOOGLE_API_KEY)

generation_config={"temperature":0.7}

model = genai.GenerativeModel('gemini-1.5-flash',generation_config=generation_config)


# Function to convert audio to text
def convert_audio_to_text(audio_file):
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    audio = AudioSegment.from_file(audio_file)
    audio.export("converted.wav", format="wav")
    
    with sr.AudioFile("converted.wav") as source:
        audio_data = recognizer.record(source)
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            print(text)
            return text
        except Exception as e:
            print(e)
            return("Cant recognize")
        

def get_gemini_response(message_input,elements_number):


    file_name_maxquestion = "max_questions.json"

    try:
      with open(file_name_maxquestion) as f2:
        number_question = json.load(f2) 

        if number_question:
           max_question=number_question[0]
    except: 
      max_question=14

    if(elements_number==2):
        topic=message_input 
        print(topic)   
 
    else:
        try:
            with open("stored_data.json") as f3:
               data=json.load(f3)
            if data:
               topic=data[2]['parts'][0]
        except Exception as e:
            print(e)
                           

    if(elements_number>=max_question):

        if(message_input=="result"):

            feedback=""
            for i in range(1,int(max_question/2)):

                question_eval=data[2*i+1]['parts'][0]
                answer_eval=data[2*i+2]['parts'][0]

                prompt=" Evaluate the following answer and provide short, constructive feedback in 3-4 lines. Provide helpful suggestions for improvement. The answer is: " +answer_eval+ ". for the question: "+ question_eval
                response = model.generate_content(prompt)

                feedback=feedback+ "The feedback for Question "+ str(i) +" is " + response.text 

            return(feedback)  
          
        else:

            return("Interview over, say result to get the result of the interview")
    
    if(topic=="computer networks" or topic=="computer network"):

        try:
            with open("compnetwork_ques.json") as user_file:
                questions = json.load(user_file)

            random_number = random.randint(0, 96)

            prompt= "You are an interviewer, ask the question to the user as in real interview : " + questions[random_number] +" This will be the question number "+str(int(elements_number/2))+" of the interview. " + "Do not say ask clarifying questions"
            response = model.generate_content(prompt)

            return(response.text)            
        
        except Exception as e:

            print(e)
            return


    if(topic=="machine learning"):

        try:
            with open("ml_questions.json",encoding='utf-8') as f4:
                questions1=json.load(f4)

            random_number1=random.randint(0,99)

            prompt="You are an interviewer, ask the question to the user as in real interview : " + questions1[random_number1] +" This will be the question number "+str(int(elements_number/2))+" of the interview."   
            response = model.generate_content(prompt)

            return(response.text)
        
        except Exception as e:

            print(e)
            return

    


  
