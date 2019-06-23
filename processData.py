from flask import request
from scrapData import *
from answerData import (
    AKREDITASI,GAGAL,
    UKT,UKT1,UKT_PENGANTAR, UKT_ONLYNUMB
    )
import random, json

def processRequest(req):
    # Get Dialogflow Intent and Entity
    req_dict = json.loads(request.data)
    intent = req_dict['queryResult']['intent']['displayName']
    entity_key = req_dict['queryResult']['parameters']
    entity_type = []
    entity_value = []

    for key in entity_key:
        entity_type.append(key)
        entity_value.append(entity_key[key])

    # Create respons for user who ask about 'akreditasi prodi' 
    if intent == "Program Studi":
        if "program_studi" in entity_type:
            scrapAkreditasi()
            for entity_value_item in entity_value:
                if entity_value_item in prodiData:
                    index = prodiData.index(entity_value_item)
                    speech = random.choice(AKREDITASI).format(
                        index=prodiData[index],
                        akreditasi=akreditasiData[index]
                    )
                else:
                    speech = random.choice(GAGAL)

    elif intent == "UKT":
        # Run scrapUKT
        scrapUKT()
        # Get Prodi entity
        entity_value_prodi = ''
        for entity_value_item in entity_value:
            entity_value_split = str(entity_value_item).split(' -')[0]
            if entity_value_split in prodiUKT:
                entity_value_prodi = entity_value_split
        # Get Number
        entity_value_number = ''
        for entity_value_item in entity_value:
            if entity_value_item in range(1,8):
                entity_value_number = entity_value_item
        
        # Only UKT but error
        if 'biaya' in entity_type:
            if 'UKT' in entity_value:
                speech = random.choice(UKT_PENGANTAR)
                # With Number
                if entity_value_number in entity_value:
                    speech = random.choice(UKT_ONLYNUMB)
                    # With prodi
                    if entity_value_prodi in prodiUKT:
                        index = prodiUKT.index(entity_value_prodi)
                        # UKT 1
                        if entity_value_number == 1:
                            speech = random.choice(UKT1).format(
                                ukt=uktData[entity_value_number][index],
                                uktIndex=int(entity_value_number),
                                prodi=prodiUKT[index]
                                )
                        # Except UKT 1
                        else:
                            speech = random.choice(UKT).format(
                                ukt=uktData[entity_value_number][index],
                                uktIndex=int(entity_value_number),
                                prodi=prodiUKT[index]
                                )
    else:
        speech = random.choice(GAGAL)
    res = results(speech)
    return res

# Post to Dialogflow
def results(speech):
    return {
        "fulfillmentText": speech,
        "source":"Webhook fullfilment source"
        }