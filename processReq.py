import json
import random
from itertools import permutations
from flask import request
from src.df_response_lib import *
from src.dictFunc import *
from src.webscrap import *
from src.googleSheet import *
from src.defaultLang import *

ff_response = fulfillment_response()

def processRequest(req):
    # Get Dialogflow Intent and Entity
    req_dict = json.loads(request.data)
    intent = req_dict['queryResult']['intent']['displayName']
    entity_key = req_dict['queryResult']['parameters']
    entity_type = []
    entity_value = []
    entity_value_temp = []

    # Get entity type and value
    for key in entity_key:
        entity_type.append(key)
        entity_value_temp.append(entity_key[key])

    # Cleaning from blank space in entity value
    for element in entity_value_temp:
        if element != "":
            entity_value.append(element)

    # Intersect entity value and scrap value
    entity_value_prodi = ''.join(set(entity_value).intersection(scrap_pdpt.prodi_split))
    entity_value_jenjang = ''.join(set(entity_value).intersection(scrap_pdpt.jenjang))
    entity_value_number = ''
    for i in entity_value:
        if i in range(1,8):
            entity_value_number = i

    try:
        if intent.lower() in gsheet_entity_intent:
            gsheet_res = gsheet_all(convert_low(entity_value),gsheet_entity_value,gsheet_list_answer)
            speech = ff_response.fulfillment_text(gsheet_res)
        
        elif intent == "Program Studi":
            # If user talk about only prodi
            if entity_value_prodi in scrap_pdpt.prodi_split:
                speech = ff_response.fulfillment_text(random.choice(RES_PRODI))
            
                # If user talk about jenjang
                if entity_value_jenjang in scrap_pdpt.jenjang:
                    speech = ff_response.fulfillment_text(random.choice(RES_JENJANG))

                    entity_value_prodi_jenjang = f"{entity_value_prodi} - {entity_value_jenjang}"
                    # If user talk about akreditasi
                    if 'Akreditasi' in entity_value:
                        index = scrap_pdpt.prodi.index(entity_value_prodi_jenjang)
                        text = random.choice(AKREDITASI).format(
                            prodi = scrap_pdpt.prodi[index],
                            akreditasi = scrap_pdpt.akreditasi[index]
                        )
                        speech = ff_response.fulfillment_text(text)

                    elif 'Fakultas' in entity_value:
                        index = scrap_pdpt.prodi.index(entity_value_prodi_jenjang)
                        text = random.choice(FAKULTAS).format(
                            prodi = scrap_pdpt.prodi[index],
                            fakultas = scrap_pdpt.fakultas[index]
                        )
                        speech = ff_response.fulfillment_text(text)

                    # If user talk about UKT
                    elif 'UKT' in entity_value:
                        speech = ff_response.fulfillment_text(random.choice(UKT_PENGANTAR))

                        # If user talk about UKT Number
                        if entity_value_number in entity_value:
                            speech = ff_response.fulfillment_text(random.choice(UKT_INFO))
                            
                            # If user give description about jenjang
                            if entity_value_jenjang == 'D3':
                                entity_value_jenjang = 'D4'
                            entity_value_prodi_jenjang = entity_value_prodi + " - " + entity_value_jenjang

                            if entity_value_prodi_jenjang in scrap_ukt.ukt_prodi_jenjang:
                                index = scrap_ukt.ukt_prodi_jenjang.index(entity_value_prodi_jenjang)
                                # Only for UKT 1
                                if entity_value_number == 1:
                                    text = random.choice(UKT1).format(
                                        ukt = scrap_ukt.ukt_nilai[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = scrap_ukt.ukt_prodi_jenjang[index],
                                    )
                                    speech = ff_response.fulfillment_text(text)
                                # Others UKT
                                else:
                                    text = random.choice(UKT).format(
                                        ukt = scrap_ukt.ukt_nilai[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = scrap_ukt.ukt_prodi_jenjang[index]
                                    )
                                    speech = ff_response.fulfillment_text(text)
            else:
                speech = ff_response.fulfillment_text(random.choice(GAGAL))
        else:
            speech = ff_response.fulfillment_text(random.choice(GAGAL))
    except:
        speech = ff_response.fulfillment_text(random.choice(EXCEPTION_DEFAULT))
    return speech
