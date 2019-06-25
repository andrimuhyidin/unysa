from flask import request
from scrapData import *
from answerData import (
    AKREDITASI,GAGAL,
    UKT,UKT1,UKT_PENGANTAR,UKT_INFO, UKT_PEMBAYARAN, UKT_PENURUNAN
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

    # Convert intersection between param and database
    entity_value_prodi = ''.join(set(entity_value).intersection(prodiSplit))
    entity_value_jenjang = ''.join(set(entity_value).intersection(jenjang))
    entity_value_number = ''
    for i in entity_value:
        if i in range(1,8):
            entity_value_number = i

    # Create respons for user who ask about 'akreditasi prodi'
    try:
        if intent == "Program Studi":
            if entity_value_prodi in prodiSplit:
                speech = f"Baik untuk {entity_value_prodi} jenjang apa?"
                if entity_value_jenjang in jenjang:
                    speech = f"Baik, info apa yang anda butuhkan saat ini?"
                    if 'Akreditasi' in entity_value:
                        index = prodiData.index(entity_value_prodi)
                        speech = random.choice(AKREDITASI).format(
                            index=prodiData[index],
                            akreditasi=akreditasiData[index]
                        )
                    elif 'Animo' or 'Daya Tampung' or 'Kelompok Ujian' in entity_value:
                        speech = 'Ini ada di website'
                    elif 'Profil' in entity_value:
                        speech = 'Ini profil'
                    elif 'Fakultas' in entity_value:
                        speech = f"Untuk {entity_value_prodi} {entity_value_jenjang} berada di fakultas {fakultasData[index]}."
                    elif 'UKT' in entity_value:
                        speech = "UKT Secara umum"
                        if entity_value_number in entity_value:
                            speech = random.choice(UKT_INFO)
                            if entity_value_jenjang == 'D3':
                                entity_value_jenjang = 'D4'
                            entity_value_prodijenjang = entity_value_prodi + " - " + entity_value_jenjang
                            if entity_value_prodijenjang in prodiJenjang:
                                index = prodiJenjang.index(entity_value_prodijenjang)
                                if entity_value_number == 1:
                                    speech = random.choice(UKT1).format(
                                        ukt = uktData[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = prodiJenjang[index],
                                    )
                                else:
                                    speech = random.choice(UKT).format(
                                        ukt = uktData[entity_value_number][index],
                                        uktIndex = int(entity_value_number),
                                        prodi = prodiJenjang[index]
                                    )
                            else:
                                speech = f"Untuk jenjang {entity_value_jenjang} dapat diakses di"
            elif 'UKT' in entity_value:
                speech = random.choice(UKT_INFO)
            else:
                speech = random.choice(GAGAL)
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