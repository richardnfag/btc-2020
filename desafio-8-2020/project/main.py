from json import loads, dumps
from os import environ

from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware


with open('dataset.json', 'r') as f:
        dataset = loads(f.read())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

def speech_to_text(audio: bytes) -> str:
    transcript = ''
    authenticator = IAMAuthenticator(environ['SPEECH_TO_TEXT_TOKEN'])
    
    speech_to_text = SpeechToTextV1(authenticator=authenticator)

    speech_to_text.set_service_url(environ['SPEECH_TO_TEXT_URL'])

    speech_recognition_results = loads(dumps(speech_to_text.recognize(
        audio=audio,
        content_type='audio/flac',
        model='pt-BR_BroadbandModel'
    ).get_result()))

    transcript = ''

    while bool(speech_recognition_results.get('results')):
        transcript = speech_recognition_results.get('results').pop().get('alternatives').pop().get('transcript') + transcript[:]

    return transcript

def nlu_analyze(text: str) -> dict:
    authenticator = IAMAuthenticator(environ['NLU_TOKEN'])

    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator)

    natural_language_understanding.set_service_url(environ['NLU_URL'])

    response = natural_language_understanding.analyze(
    text=text,
    features=Features(
        entities=EntitiesOptions(
            emotion=True,
            sentiment=True,            
            model='ba52d4bd-516e-4841-bfea-024d0e1c7aa8'
        ),

    )).get_result()

    return loads(dumps(response))

def priority(e: dict) -> dict:
    if e['entity'] == 'SEGURANCA':
        return 1
    if e['entity'] == 'CONSUMO':
        return 2
    if e['entity'] == 'DESEMPENHO':
        return 3
    if e['entity'] == 'MANUTENCAO':
        return 4
    if e['entity'] == 'CONFORTO':
        return 5
    if e['entity'] == 'DESIGN':
        return 6
    if e['entity'] == 'ACESSORIOS':
        return 7

def check_negative(entities: list) -> dict:
    
    negatives = list(filter(lambda x: x['sentiment'] < 0, entities))
 
    if negatives != []:
        min_value = min(list(map(lambda x: x['sentiment'], negatives)))

        n = [x for x in negatives if round(x['sentiment'], 2) == round(min_value, 2)]
        
        return sorted(list(n), key=priority)[0]
    else:
        return {}

def get_recommendation(entity: dict, name: str) -> str:
    
    if entity != {}:

        d = list(filter(lambda x: x['NOME'] == name, dataset))

        if d != []:
            
            r = list(filter(lambda x: x[entity['entity']] > d[0][entity['entity']], dataset))
            
            if r != []:
                # return r[0]['NOME']
                return sorted(r, key=lambda x: x[entity['entity']], reverse=True)[0]['NOME']
            else:
                return ""
        else:
            return sorted(dataset, key=lambda x: x[entity['entity']], reverse=True)[0]['NOME']
            
    else:
        return ""

@app.post("/api/recommend")
async def recommend(audio: bytes = File(None), text: str = Form(None), car: str = Form(...)):
    
    if audio:
        text = speech_to_text(audio)

    if text:
        text_analyzed = nlu_analyze(text)

    entities = []

    for entity in text_analyzed['entities']:
        entities.append({
            "entity": entity['type'],
            "sentiment": entity['sentiment']['score'],
            "mention": entity['text'],
        })


    return {
        "recommendation": get_recommendation(check_negative(entities), car.upper()),
        "entities": entities
    }
