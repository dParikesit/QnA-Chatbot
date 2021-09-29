import requests
from decouple import config

# All models are taken from hugging-face hub
API_TOKEN = config('API_TOKEN')
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# deepset/roberta-base-squad2 as question answering model
QnA_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

# Helsinki-NLP for translation between Bahasa Indonesia and English
IdToEn_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-id-en"
EnToId_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-id"

def getAnswer(question):
    response = requests.post(
        QnA_URL,
        headers=headers,
        json={
            "inputs": {
                "question":
                question,
                "context":
                "Prosa.AI is a company that wants to bring NLP and AI for Indonesia language",
            }
        })
    return response.json()

def translateToEn(text):
    response = requests.post(IdToEn_URL, headers=headers, json={"inputs": text})
    return response.json()

def translateToId(text):
    response = requests.post(EnToId_URL,headers=headers,json={"inputs": text})
    return response.json()