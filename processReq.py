import json
import random
from itertools import permutations
from flask import request
from srcData.srcScrap import *
from srcData.srcGsheet import *
from srcData.srcLocal import (
    AKREDITASI,GAGAL,
    UKT,UKT1,UKT_PENGANTAR,UKT_INFO, UKT_PEMBAYARAN, UKT_PENURUNAN
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

    # Convert intersection between param and database
    entity_value_prodi = ''.join(set(entity_value).intersection(prodiSplit))
    entity_value_jenjang = ''.join(set(entity_value).intersection(jenjang))
    entity_value_number = ''
    for i in entity_value:
        if i in range(1,8):
            entity_value_number = i

    # Create respons for user who ask about 'akreditasi prodi'
    try:
        # Prodi Intent
        if intent == "Program Studi":
            # If user talk about only prodi
            if entity_value_prodi in prodiSplit:
                speech = f"Baik untuk {entity_value_prodi} jenjang apa?"
                # If user talk about jenjang
                if entity_value_jenjang in jenjang:
                    speech = f"Baik, info apa yang anda butuhkan saat ini?"
                    # If user talk about akreditasi
                    if 'Akreditasi' in entity_value:
                        index = prodiData.index(entity_value_prodi)
                        speech = random.choice(AKREDITASI).format(
                            index=prodiData[index],
                            akreditasi=akreditasiData[index]
                        )
                    # If user talk about Animo
                    elif ('Animo' or 'Daya Tampung' or 'Kelompok Ujian') in entity_value:
                        speech = 'Ini ada di website'
                    # If user talk about Profil
                    elif 'Profil' in entity_value:
                        speech = 'Ini profil'
                    # If user talk about fakultas
                    elif 'Fakultas' in entity_value:
                        speech = f"Untuk {entity_value_prodi} {entity_value_jenjang} berada di fakultas {fakultasData[index]}."
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
                            if entity_value_prodijenjang in prodiJenjang:
                                index = prodiJenjang.index(entity_value_prodijenjang)
                                # Only for UKT 1
                                if entity_value_number == 1:
                                    speech = random.choice(UKT1).format(
                                        ukt = uktData[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = prodiJenjang[index],
                                    )
                                # Others UKT
                                else:
                                    speech = random.choice(UKT).format(
                                        ukt = uktData[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = prodiJenjang[index]
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
            # Filter list based on len of each elemen
            sheet_value_filter = []
            for elemen in sheet_entity_value_split:
                if len(elemen) == len(entity_value):
                    sheet_value_filter.append(elemen)

            # List permutation
            entity_value_permutation = permutations(entity_value)

            # Find same data
            for elemen in entity_value_permutation:
                if list(elemen) in sheet_value_filter:
                    index = sheet_entity_value_split.index(list(elemen))
                    break

            speech = random.choice(sheet_answer)[index]

        else:
            # speech = random.choice(GAGAL)
            speech = f"Respon Gagal {intent} {sheet_entity_intent}"
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

