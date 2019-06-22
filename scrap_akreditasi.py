from module import *

urls = []
fakultasList = []
prodiList = []
akreditasiList = []

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
    
    fakultasList.append(fakultas)
    prodiList.append(prodi)
    akreditasiList.append(akreditasi)
    
fakultasData = []
for i in fakultasList:
    for j in i:
        fakultasData.append(j)

prodiData=[]
for i in prodiList:
    for j in i:
        prodiData.append(j)

akreditasiData=[]
for i in akreditasiList:
    for j in i:
        akreditasiData.append(j)
