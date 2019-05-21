from bs4 import BeautifulSoup
import requests
import pandas as pd
# import json
# from tabulate import tabulate

urls = []

# Define list
fakultasList = []
prodiList = []
akreditasiList = []

for i in range(1,9):
    dataUrl = f'http://pdpt.uny.ac.id/dtakreditasi?page={i}'.split(" ")
    urls = dataUrl
    for i in urls:
        url = requests.get(i)
        soup = BeautifulSoup(url.content, 'html.parser')
        table = soup.find_all('table')
        df = pd.read_html(str(table))[0]

        # Define Value
        fakultasFungsi = df['Fakultas'].tolist()
        prodiFungsi = df['Prodi'].tolist()
        akreditasiFungsi = df['Akreditasi'].tolist()

    fakultasList.append(fakultasFungsi)
    prodiList.append(prodiFungsi)
    akreditasiList.append(akreditasiFungsi)

fakultasGabung=[]
for i in fakultasList:
    for j in i:
        fakultasGabung.append(j)

prodiGabung=[]
for i in prodiList:
    for j in i:
        prodiGabung.append(j)

akreditasiGabung=[]
for i in akreditasiList:
    for j in i:
        akreditasiGabung.append(j)

# Cek
# a = 106
# b = 106
# if a == b:
#     print(f'Benar prodi {prodiGabung[a]} fakultas {fakultasGabung[a]} memiliki akreditasi {akreditasiGabung[b]}.')
# else:
#     print("Keliru")
                
