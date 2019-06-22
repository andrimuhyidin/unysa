# def beasiswa():
#         url = requests.get('http://pmb.uny.ac.id/beasiswa')
#         soup = BeautifulSoup(url.content, 'html.parser')
#         listBeasiswa = soup.find('div',{'property':'schema:text'}).find_all('li')
#         dataBeasiswa = []
#         for tag in listBeasiswa:
#                 dataBeasiswa.append(tag.text)
#         return dataBeasiswa