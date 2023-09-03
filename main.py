import os
from dotenv import load_dotenv
import pandas as pd
import requests
import json
import openai

load_dotenv()

openai.api_key =  os.getenv('OPENAI')

API_URL = 'https://sdw-2023-prd.up.railway.app'

data_frame = pd.read_csv('SDW2023.csv')
users = data_frame['UserID'].unique()

responses = []



##EXTRACT

def get_user(user):
    response = requests.get(str(API_URL + '/users/' + str(user)))     
    
    if response.status_code != 200:
        return None
    
    return response.json()


##TRANSFORM

def genarate_text_ia(data):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {data['name']}, que é um usuário do banco Santander, sobre a importância dos investimentos (máximo de 100 caracteres) (adicione um emoji que faça sentido com a mensagem no ultimo caractere da mensagem):"
      }
    ]
  )
    
    return completion.choices[0].message.content.strip('\"')



##LOAD

def update_user(data_user):
    response = requests.put(str(API_URL + '/users/' + str(data_user['id'])), json=data_user)
    
    return response.status_code



##RUN
for user in users:
    response = get_user(user)

    if response is not None:
        text = genarate_text_ia(response)## Chama chat gpt

        print(text) 
        
        response['news'].append({
            "icon": text[-1],
            "description": text
        }) 

        print(response)

        verify = update_user(response)

        print(verify)

        
