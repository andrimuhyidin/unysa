from module import *

prodiList = []
uktList = {
        1:[],
        2:[],
        3:[],
        4:[],
        5:[],
        6:[],
        7:[]
}
urls = [
'http://pmb.uny.ac.id/biaya-pendidikan/uang-kualiah-tunggal-ukt-program-studi-sarjana-terapan-ster',
'http://pmb.uny.ac.id/biaya-pendidikan/uang-kuliah-tunggal-ukt-program-studi-s1'
]

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

    prodiList.append(prodi)
    for i in range(1,7):
            uktList[i].append(ukt[i])

prodiUKT = []
for i in prodiList:
        for j in i:
                prodiUKT.append(j)

uktData = {
        1:[],
        2:[],
        3:[],
        4:[],
        5:[],
        6:[],
        7:[]
}
for i in range(1,8):
        for j in uktList[i]:
                for x in j:
                        uktData[i].append(x)