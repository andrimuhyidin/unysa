from bs4 import BeautifulSoup
import requests
import pandas as pd

"""
Source: PDPT UNY
"""

"""
Store temp data as List
"""
def convert_temp(tempData):
    storeData = []
    for i in tempData:
        for j in i:
            storeData.append(j)
    return storeData
    
class scrap_pdpt:
    temp_fakultas = []
    temp_prodi = []
    temp_akreditasi = []

    for i in range(1,9):
        urls = f'http://pdpt.uny.ac.id/dtakreditasi?page={i}'.split(" ")
        for i in urls:
            url = requests.get(i)
            soup = BeautifulSoup(url.content, 'html.parser')
            table = soup.find_all('table')
            df = pd.read_html(str(table))[0]

            df_fakultas = df['Fakultas'].tolist()
            df_prodi = df['Prodi'].tolist()
            df_akreditasi = df['Akreditasi'].tolist() 

        temp_fakultas.append(df_fakultas)
        temp_prodi.append(df_prodi)
        temp_akreditasi.append(df_akreditasi)
        
    fakultas = convert_temp(temp_fakultas)
    prodi = convert_temp(temp_prodi)
    akreditasi = convert_temp(temp_akreditasi)
    prodi_split = []
    jenjang = []
    for i in prodi:
        split = str(i).split(' - ')[0:]
        prodi_split.append(split[0])
        jenjang.append(split[1])

"""
Source: PMB UNY
"""
class scrap_ukt:
    temp_jenjang = []
    temp_prodi = []
    temp_ukt = {1:[],2:[],3:[],4:[],5:[],6:[],7:[]}

    urls = ['http://pmb.uny.ac.id/biaya-pendidikan/uang-kualiah-tunggal-ukt-program-studi-sarjana-terapan-ster',
        'http://pmb.uny.ac.id/biaya-pendidikan/uang-kuliah-tunggal-ukt-program-studi-s1']

    for i in urls:
        url = requests.get(i)
        soup = BeautifulSoup(url.content, 'html.parser')
        table = soup.find_all('table')
        df = pd.read_html(str(table),index_col=0, header=0)[0]

        df_jenjang = df['JENJANG'].tolist()
        temp_jenjang.append(df_jenjang)

        df_prodi = df['PROGRAM STUDI'].tolist()
        temp_prodi.append(df_prodi)

        df_ukt = {
            1:df['UKT.1'].tolist(),
            2:df['UKT. II'].tolist(),
            3:df['UKT. III'].tolist(),
            4:df['UKT. IV'].tolist(),
            5:df['UKT. V'].tolist(),
            6:df['UKT. VI'].tolist(),
            7:df['UKT. VII'].tolist()
        }
        for i in range(1,8):
            temp_ukt[i].append(df_ukt[i])

    ukt_prodi = convert_temp(temp_prodi)
    
    ukt_jenjang = []
    for i in temp_jenjang:
        for j in i:
            if j == "Sarjana Terapan (D.IV)":
                j = "D4"
                ukt_jenjang.append(j)
            else:
                ukt_jenjang.append(j)

    ukt_nilai = {1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
    for i in range(1,8):
        for j in temp_ukt[i]:
            for k in j:
                ukt_nilai[i].append(k)

    ukt_prodi_jenjang = []
    for i in range(0,len(ukt_prodi)):
        j = f"{ukt_prodi[i]} - {ukt_jenjang[i]}"
        ukt_prodi_jenjang.append(j)

# Temporary Disable
# class scrap_beasiswa:
#     url = requests.get('http://pmb.uny.ac.id/beasiswa')
#     soup = BeautifulSoup(url.content, 'html.parser')
#     listBeasiswa = soup.find('div',{'property':'schema:text'}).find_all('li')
#     dataBeasiswa = []
#     for tag in listBeasiswa:
#         dataBeasiswa.append(tag.text)