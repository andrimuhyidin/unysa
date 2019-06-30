# Importing json module to req and post data
import json

# Importing random module to randomize the choice of answer
import random

# Import request module from flask to transfer json data
from flask import request

# Import all module from src folder
from src.df_response_lib import *
from src.dictFunc import *
from src.webscrap import *
from src.googleSheet import *
from src.defaultLang import *

"""
Define fullfilment response function as new name
How to use:
fullfilment_text(text)
"""
ff_response = fulfillment_response()

"""
Process Request Module
Hub of all logical process in this chatbot:
1. Processing data from web scraping
2. Processing data from google sheet
3. Processing from local module as default answer
"""
def processRequest(req):
    # Get Dialogflow Intent and Entity parameters
    req_dict = json.loads(request.data)
    intent = req_dict['queryResult']['intent']['displayName']
    entity_key = req_dict['queryResult']['parameters']

    # Get entity type and value
    entity_type = []
    entity_value = []
    entity_value_temp = []
    for key in entity_key:
        entity_type.append(key)
        entity_value_temp.append(entity_key[key])

    # Cleaning from blank space in entity value
    for element in entity_value_temp:
        if element != "":
            entity_value.append(element)

    # Intersect between entity and scrap value
    entity_value_prodi = ''.join(set(entity_value).intersection(scrap_pdpt.prodi_split))
    entity_value_jenjang = ''.join(set(entity_value).intersection(scrap_pdpt.jenjang))
    
    # Get number of UKT 
    entity_value_number = ''
    for i in entity_value:
        if i in range(1,8):
            entity_value_number = i

    # Protect if bot dont know what the respons with default exception respons
    try:
        """
        Syncronize the intent and entity value in dialogflow with google sheet value
        All value are convert to lowercase
        """
        if intent.lower() in gsheet_entity_intent:
            gsheet_res = gsheet_all(convert_low(entity_value),gsheet_entity_value,gsheet_list_answer)
            speech = ff_response.fulfillment_text(gsheet_res)
        
        # Only for Intent : Program Studi
        elif intent == "Program Studi":
            # If user talk about only prodi
            if entity_value_prodi in scrap_pdpt.prodi_split:
                # Get respons from defaultLang
                speech = ff_response.fulfillment_text(random.choice(RES_PRODI))
            
                # If user talk added value of jenjang
                if entity_value_jenjang in scrap_pdpt.jenjang:
                    speech = ff_response.fulfillment_text(random.choice(RES_JENJANG))

                    # Joining value of prodi and jenjang to validate in PDPT data source
                    entity_value_prodi_jenjang = f"{entity_value_prodi} - {entity_value_jenjang}"

                    # If user talk about akreditasi
                    if 'Akreditasi' in entity_value:
                        # Get index from PDPT
                        index = scrap_pdpt.prodi.index(entity_value_prodi_jenjang)
                        
                        # Get respons based on value of web scrapping
                        text = random.choice(AKREDITASI).format(
                            prodi = scrap_pdpt.prodi[index],
                            akreditasi = scrap_pdpt.akreditasi[index]
                        )

                        # Generate response
                        speech = ff_response.fulfillment_text(text)

                    # If user talk about Fakultas
                    elif 'Fakultas' in entity_value:
                        # Get index from PDPT data
                        index = scrap_pdpt.prodi.index(entity_value_prodi_jenjang)
                        
                        # Get respons based on web scrapping
                        text = random.choice(FAKULTAS).format(
                            prodi = scrap_pdpt.prodi[index],
                            fakultas = scrap_pdpt.fakultas[index]
                        )

                        # Generate respons
                        speech = ff_response.fulfillment_text(text)

                    # If user talk about UKT
                    elif 'UKT' in entity_value:
                        speech = ff_response.fulfillment_text(random.choice(UKT_PENGANTAR))

                        # If user talk about UKT Number
                        if entity_value_number in entity_value:
                            speech = ff_response.fulfillment_text(random.choice(UKT_INFO))
                            
                            # If user give description about jenjang convert value D3 to D4
                            if entity_value_jenjang == 'D3':
                                entity_value_jenjang = 'D4'
                            
                            # Reinisialitation of entity_value_prodi_jenjang because PDPT and PMB not same
                            entity_value_prodi_jenjang = entity_value_prodi + " - " + entity_value_jenjang

                            # Validate between entity value and source data PMB UNY (UKT)
                            if entity_value_prodi_jenjang in scrap_ukt.ukt_prodi_jenjang:
                                # Get Index from source data
                                index = scrap_ukt.ukt_prodi_jenjang.index(entity_value_prodi_jenjang)

                                # Only for UKT 1, because web scrapping result give different number (500.000 > 5000)
                                if entity_value_number == 1:
                                    text = random.choice(UKT1).format(
                                        ukt = scrap_ukt.ukt_nilai[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = scrap_ukt.ukt_prodi_jenjang[index],
                                    )
                                    speech = ff_response.fulfillment_text(text)

                                # Others UKT value
                                else:
                                    text = random.choice(UKT).format(
                                        ukt = scrap_ukt.ukt_nilai[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = scrap_ukt.ukt_prodi_jenjang[index]
                                    )
                                    speech = ff_response.fulfillment_text(text)
            
            # If user say about entity value number with others
            else:
                speech = ff_response.fulfillment_text(random.choice(GAGAL))
        
        # Default answer if bot dont know entity value
        else:
            speech = ff_response.fulfillment_text(random.choice(GAGAL))

    # Default answer if bot dont know about what user says
    except:
        speech = ff_response.fulfillment_text(random.choice(EXCEPTION_DEFAULT))

    # Return all value as speech
    return speech
