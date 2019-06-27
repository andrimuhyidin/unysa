import json
import random
from itertools import permutations
from flask import request
from src.dictFunc import *
from src.webscrap import *
from src.googleSheet import *
from src.defaultLang import (
    AKREDITASI,GAGAL,
    UKT,UKT1,UKT_PENGANTAR,UKT_INFO, UKT_PEMBAYARAN, UKT_PENURUNAN,
    EXCEPTION_DEFAULT
)

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

    try:
        if intent in gsheet_entity_intent:
            gsheet_res = gsheet_all(entity_value,gsheet_entity_value,gsheet_list_answer)
            speech = gsheet_res

            # If user talk about only prodi
            entity_value_prodi = ''.join(set(entity_value).intersection(scrap_pdpt.prodi_split))
            if entity_value_prodi in scrap_pdpt.prodi_split:
                speech = f"Baik untuk {entity_value_prodi} jenjang apa?"
                entity_value_jenjang = ''.join(set(entity_value).intersection(scrap_pdpt.jenjang))
                # If user talk about jenjang
                if entity_value_jenjang in scrap_pdpt.jenjang:
                    speech = f"Baik, info apa yang anda butuhkan saat ini?"
                    # If user talk about akreditasi
                    if 'Akreditasi' in entity_value:
                        index = scrap_pdpt.prodi.index(entity_value_prodi)
                        speech = random.choice(AKREDITASI).format(
                            index = scrap_pdpt.prodi[index],
                            akreditasi = scrap_pdpt.akreditasi[index]
                        )
                    # If user talk about UKT
                    elif 'UKT' in entity_value:
                        speech = "UKT Secara umum"
                        # If user talk about UKT Number
                        entity_value_number = ''
                        for i in entity_value:
                            if i in range(1,8):
                                entity_value_number = i
                        if entity_value_number in entity_value:
                            speech = random.choice(UKT_INFO)
                            # If user give description about jenjang
                            if entity_value_jenjang == 'D3':
                                entity_value_jenjang = 'D4'
                            entity_value_prodijenjang = entity_value_prodi + " - " + entity_value_jenjang
                            if entity_value_prodijenjang in scrap_ukt.ukt_prodi_jenjang:
                                index = scrap_ukt.ukt_prodi_jenjang.index(entity_value_prodijenjang)
                                # Only for UKT 1
                                if entity_value_number == 1:
                                    speech = random.choice(UKT1).format(
                                        ukt = scrap_ukt.ukt_nilai[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = scrap_ukt.ukt_prodi_jenjang[index],
                                    )
                                # Others UKT
                                else:
                                    speech = random.choice(UKT).format(
                                        ukt = scrap_ukt.ukt_nilai[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = scrap_ukt.ukt_prodi_jenjang[index]
                                    )
            elif entity_value in gsheet_entity_value:
                speech = "INI BERHASIL UNTUK SINGLE ENTITY"
            elif 'UKT' in entity_value:
                speech = random.choice(UKT_INFO)
        else:
            speech = "GAGAL TIDAK ADA SEMUA"
    except:
        speech = random.choice(EXCEPTION_DEFAULT)
    res = results(speech)
    return res

# Post to Dialogflow
def results(speech):
    return {
        "fulfillmentText": speech,
        "source":"Webhook fullfilment source"
    }

