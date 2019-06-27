import json
import random
from itertools import permutations
from flask import request
from src.dictFunc import *
from src.webscrap import *
from src.googleSheet import *
from src.defaultLang import (
    AKREDITASI,GAGAL,
    UKT,UKT1,UKT_PENGANTAR,UKT_INFO, UKT_PEMBAYARAN, UKT_PENURUNAN
)

# Run Function
sc_pdpt = scrap_pdpt()
sc_ukt = scrap_ukt()
sc_beasiswa = scrap_beasiswa()

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

    # Convert intersection between param and database
    entity_value_prodi = ''.join(set(entity_value).intersection(sc_pdpt.prodi_split))
    entity_value_jenjang = ''.join(set(entity_value).intersection(sc_pdpt.jenjang))
    entity_value_number = ''
    for i in entity_value:
        if i in range(1,8):
            entity_value_number = i

    # Create respons for user who ask about 'akreditasi prodi'
    try:
        # Prodi Intent
        if intent == "Program Studi":
            # If user talk about only prodi
            if entity_value_prodi in sc_pdpt.prodi_split:
                speech = f"Baik untuk {entity_value_prodi} jenjang apa?"
                # If user talk about jenjang
                if entity_value_jenjang in sc_pdpt.jenjang:
                    speech = f"Baik, info apa yang anda butuhkan saat ini?"
                    # If user talk about akreditasi
                    if 'Akreditasi' in entity_value:
                        index = sc_pdpt.prodi.index(entity_value_prodi)
                        speech = random.choice(AKREDITASI).format(
                            index = sc_pdpt.prodi[index],
                            akreditasi = sc_pdpt.akreditasi[index]
                        )
                    # If user talk about Animo
                    elif ('Animo' or 'Daya Tampung' or 'Kelompok Ujian') in entity_value:
                        speech = 'Ini ada di website'
                    # If user talk about Profil
                    elif 'Profil' in entity_value:
                        speech = 'Ini profil'
                    # If user talk about fakultas
                    elif 'Fakultas' in entity_value:
                        speech = f"Untuk {entity_value_prodi} {entity_value_jenjang} berada di fakultas {sc_pdpt.akreditasi[index]}."
                    # If user talk about UKT
                    elif 'UKT' in entity_value:
                        speech = "UKT Secara umum"
                        # If user talk about UKT Number
                        if entity_value_number in entity_value:
                            speech = random.choice(UKT_INFO)
                            # If user give description about jenjang
                            if entity_value_jenjang == 'D3':
                                entity_value_jenjang = 'D4'
                            entity_value_prodijenjang = entity_value_prodi + " - " + entity_value_jenjang
                            if entity_value_prodijenjang in sc_ukt.ukt_prodi_jenjang:
                                index = sc_ukt.ukt_prodi_jenjang.index(entity_value_prodijenjang)
                                # Only for UKT 1
                                if entity_value_number == 1:
                                    speech = random.choice(UKT1).format(
                                        ukt = sc_ukt.ukt_nilai[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = sc_ukt.ukt_prodi_jenjang[index],
                                    )
                                # Others UKT
                                else:
                                    speech = random.choice(UKT).format(
                                        ukt = sc_ukt.ukt_nilai[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = sc_ukt.ukt_prodi_jenjang[index]
                                    )
                            # For pascasarjana
                            else:
                                speech = f"Untuk jenjang {entity_value_jenjang} dapat diakses di"
            # Only say UKT
            elif 'UKT' in entity_value:
                speech = random.choice(UKT_INFO)
            # Default Error
            else:
                speech = random.choice(GAGAL)
        
        # For normally answer
        elif intent.lower() in sheet_entity_intent:
            speech = gsheet_all(sheet_entity_value,'.',entity_value,sheet_answer)
        else:
            speech = random.choice(GAGAL)
    except:
        speech = "Mohon maaf, pertanyaan anda belum bisa saya pahami atau data tidak ada dalam sistem. Coba dengan pertanyaan lain"
    res = results(speech)
    return res

# Post to Dialogflow
def results(speech):
    return {
        "fulfillmentText": speech,
        "source":"Webhook fullfilment source"
    }

