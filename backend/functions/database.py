import os
import json
import random

# Save messages for retrieval later on
def get_recent_messages():

  # Define the file name
  file_name = "stored_data.json"
  
  # Initialize messages
  messages = []
  
  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      
      # Append last 5 rows of data
      if data:
        for item in data:
          messages.append(item)
          
  except:
    pass
 
  # Return messages
  return messages


# Save messages for retrieval later on
def store_messages(request_message, response_message):

  # Define the file name
  file_name = "stored_data.json"

  # Get recent messages
  messages = get_recent_messages()

  # Add messages to data
  user_message = {"role": "user", "parts": [request_message]}
  assistant_message = {"role": "model", "parts": [response_message]}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the updated file
  with open(file_name, "w") as f:
    json.dump(messages, f)


# Save messages for retrieval later on
def reset_messages():

  # Define the file name
  file_name = "stored_data.json"

  # Write an empty file
  with open(file_name, "w") as f:
    json.dump([],f)

  file_name1="max_questions.json"
  
  with open(file_name1, "w") as f1:
    json.dump([2*random.randint(5,8)],f1)    


