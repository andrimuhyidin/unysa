from bs4 import BeautifulSoup
import requests
import pandas as pd

urls = []
fakultasData = []
prodiData = []
prodiUKT = []
akreditasiData = []
uktData = {1:[],2:[],3:[],4:[],5:[],6:[],7:[]}

class scrapAkreditasi:
    fakultasTemp = []
    prodiTemp = []
    akreditasiTemp = []
    for i in range(1,9):
        urls = f'http://pdpt.uny.ac.id/dtakreditasi?page={i}'.split(" ")
        for i in urls:
            url = requests.get(i)
            soup = BeautifulSoup(url.content, 'html.parser')
            table = soup.find_all('table')
            df = pd.read_html(str(table))[0]
            fakultas = df['Fakultas'].tolist()
            prodi = df['Prodi'].tolist()
            akreditasi = df['Akreditasi'].tolist() 
        fakultasTemp.append(fakultas)
        prodiTemp.append(prodi)
        akreditasiTemp.append(akreditasi)  
    for i in fakultasTemp:
        for j in i:
            fakultasData.append(j)
    for i in prodiTemp:
        for j in i:
            prodiData.append(j)
    for i in akreditasiTemp:
        for j in i:
            akreditasiData.append(j)

class scrapUKT:
    urls = [
        'http://pmb.uny.ac.id/biaya-pendidikan/uang-kualiah-tunggal-ukt-program-studi-sarjana-terapan-ster',
        'http://pmb.uny.ac.id/biaya-pendidikan/uang-kuliah-tunggal-ukt-program-studi-s1'
        ]
    prodiTemp = []
    uktTemp = {1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
    for i in urls:
        url = requests.get(i)
        soup = BeautifulSoup(url.content, 'html.parser')
        table = soup.find_all('table')
        df = pd.read_html(str(table),index_col=0, header=0)[0]
        prodi = df['PROGRAM STUDI'].tolist()
        ukt = {
            1:df['UKT.1'].tolist(),
            2:df['UKT. II'].tolist(),
            3:df['UKT. III'].tolist(),
            4:df['UKT. IV'].tolist(),
            5:df['UKT. V'].tolist(),
            6:df['UKT. VI'].tolist(),
            7:df['UKT. VII'].tolist()
        }
        prodiTemp.append(prodi)
        for i in range(1,8):
                uktTemp[i].append(ukt[i])
    for i in prodiTemp:
            for j in i:
                    prodiUKT.append(j)
    for i in range(1,8):
            for j in uktTemp[i]:
                    for x in j:
                            uktData[i].append(x)

class scrapBeasiswa:
    url = requests.get('http://pmb.uny.ac.id/beasiswa')
    soup = BeautifulSoup(url.content, 'html.parser')
    listBeasiswa = soup.find('div',{'property':'schema:text'}).find_all('li')
    dataBeasiswa = []
    for tag in listBeasiswa:
        dataBeasiswa.append(tag.text)